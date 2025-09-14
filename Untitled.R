# ──────────────────────────────────────────────────────────────
# 0.  Load packages
# ──────────────────────────────────────────────────────────────
# install.packages(c("readxl", "dplyr"))
library(readxl)
library(dplyr)

# ──────────────────────────────────────────────────────────────
# 1.  FRPM 2021-22  →  frpm_lausd (clean names)
# ──────────────────────────────────────────────────────────────
frpm_path <- "~/Downloads/frpm2122_v2.xlsx"

# If the FRPM sheet name is uncertain, take the 2nd sheet (adjust if needed)
frpm_raw <- read_excel(frpm_path, sheet = 2, skip = 1)

# Explicit column rename vector  (index order must match colnames(frpm_raw))
names(frpm_raw) <- c(
  "academic_year",
  "county_code",
  "district_code",
  "school_code",
  "county_name",
  "district_name",
  "school_name",
  "district_type",
  "school_type",
  "educational_option_type",
  "nslp_provision_status",
  "charter_school_yn",
  "charter_school_number",
  "charter_funding_type",
  "irc",
  "low_grade",
  "high_grade",
  "enrollment_k_12",
  "free_meal_count_k_12",
  "percent_eligible_free_k_12",
  "frpm_count_k_12",
  "percent_eligible_frpm_k_12",
  "enrollment_5_17",
  "free_meal_count_5_17",
  "percent_eligible_free_5_17",
  "frpm_count_5_17",
  "frpm_rate",                      # running variable
  "calpads_cert_status"
)

frpm_lausd <- frpm_raw %>%
  filter(district_name == "Los Angeles Unified") %>%
  select(school_name, school_code, frpm_rate) %>%
  mutate(
    school_name = toupper(trimws(school_name)),
    frpm_rate   = as.numeric(frpm_rate)
  )

# ──────────────────────────────────────────────────────────────
# 2.  Chronic Absenteeism TXT  →  attendance_lausd
# ──────────────────────────────────────────────────────────────
att_path <- "~/Downloads/chronicabsenteeism22-v3.txt"

att_raw <- read.delim(att_path, sep = "\t", quote = "\"", stringsAsFactors = FALSE)

# Minimal rename for needed columns
names(att_raw)[ names(att_raw) == "District.Name"            ] <- "district_name"
names(att_raw)[ names(att_raw) == "School.Name"              ] <- "school_name"
names(att_raw)[ names(att_raw) == "ChronicAbsenteeismRate"   ] <- "chronic_absenteeism"

attendance_lausd <- att_raw %>%
  filter(district_name == "Los Angeles Unified")

# ──────────────────────────────────────────────────────────────
# 3.  Merge  +  create RDD vars
# ──────────────────────────────────────────────────────────────
merged <- inner_join(frpm_lausd, attendance_lausd, by = "school_name") %>%
  mutate(
    treated = ifelse(frpm_rate >= 75, 1, 0),
    running = frpm_rate - 75
  )

# ──────────────────────────────────────────────────────────────
# 4.  Beyond-the-Bell  →  add btb_participation
# ──────────────────────────────────────────────────────────────
btb_path <- "~/Downloads/BeyondTheBellSchoolSitePrograms-20212022 copy.csv"
btb_raw  <- read.csv(btb_path, stringsAsFactors = FALSE)

# Rename the single column we need
names(btb_raw)[ names(btb_raw) == "School" ] <- "school_name"

btb_clean <- btb_raw %>%
  mutate(school_name = toupper(trimws(school_name))) %>%
  distinct(school_name) %>%
  mutate(btb_participation = 1)

merged <- merged %>%
  left_join(btb_clean, by = "school_name") %>%
  mutate(btb_participation = ifelse(is.na(btb_participation), 0, 1))

# ──────────────────────────────────────────────────────────────
# 5.  Inspect & save
# ──────────────────────────────────────────────────────────────
print(head(merged, 3))
summary(select(merged, frpm_rate, chronic_absenteeism))
table(merged$btb_participation)

write.csv(
  merged,
  "~/Downloads/lausd_rdd_dataset_2021.csv",
  row.names = FALSE
)

cat("\n✅  Final dataset saved to ~/Downloads/lausd_rdd_dataset_2021.csv\n")
