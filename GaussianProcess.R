# ──────────────────────────────────────────────────────────────
# 0.  Load packages for gausian processes, then data manipulation
# ──────────────────────────────────────────────────────────────
# install.packages("devtools")
devtools::install_github('doeun-kim/gpss')
# install.packages(c("readxl", "dplyr"))
library(gpss)
library(readxl)
library(dplyr)
library(stringr)
library(dplyr)
library(ggplot2)

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
    frpm_rate   = as.numeric(frpm_rate),
    schoolcode = as.character(school_code)
  )

# ──────────────────────────────────────────────────────────────
# 2.  Chronic Absenteeism TXT  →  attendance_lausd
# ──────────────────────────────────────────────────────────────
att_path <- "~/Downloads/chronicabsenteeism22-v3.txt"

att_raw <- read.delim(att_path, sep = "\t", quote = "\"", stringsAsFactors = FALSE)

# Minimal rename for needed columns
names(att_raw)[ names(att_raw) == "District.Name"            ] <- "district_name"
names(att_raw)[ names(att_raw) == "School.Name"              ] <- "school_name"
names(att_raw)[ names(att_raw) == "School.Code"              ] <- "school_code"
names(att_raw)[ names(att_raw) == "ChronicAbsenteeismRate"   ] <- "chronic_absenteeism"


attendance_lausd <- att_raw %>%
  filter(district_name == "Los Angeles Unified") %>%
  mutate(
    school_code = as.character(school_code),
    chronic_absenteeism  = as.numeric(na_if(chronic_absenteeism, '*')),
    ChronicAbsenteeismEligibleCumulativeEnrollment = as.numeric(na_if(ChronicAbsenteeismEligibleCumulativeEnrollment, '*')),
    ChronicAbsenteeismCount = as.numeric(na_if(ChronicAbsenteeismCount, '*')),
  )

# ──────────────────────────────────────────────────────────────
# 3.  Merge  +  create RDD vars
# ──────────────────────────────────────────────────────────────
merged <- inner_join(frpm_lausd, attendance_lausd, by = "school_code") %>%
  mutate(
    treated = ifelse(frpm_rate >= 0.75, 1, 0),
    running = frpm_rate - 0.75
  )

# ──────────────────────────────────────────────────────────────
# 4.  Beyond-the-Bell  →  add btb_participation
# ──────────────────────────────────────────────────────────────
btb_path <- "~/Downloads/BeyondTheBellSchoolSitePrograms-20212022 copy.csv"
btb_raw  <- read.csv(btb_path, stringsAsFactors = FALSE)

# Rename the single column we need
names(btb_raw)[ names(btb_raw) == "School" ] <- "school_name"


btb_clean <- btb_raw %>%
  mutate(
    btb_am = ifelse(is.na(BeforeSchoolGrantProgram), 0, 1),
    btb_pm = ifelse(is.na(AfterSchoolGeneralFundedPrograms) | is.na(AfterSchoolGrantProgram), 0, 1),
    CDSCode = as.character(CDSCode),
    school_code = str_sub(CDSCode, -7)
  )

btb_unique <- btb_clean %>%
  group_by(school_code) %>%
  summarise(
    SchoolYear = first(SchoolYear),  # or customize how you want to handle it
    BeforeSchoolGrantProgram = as.integer(any(!is.na(BeforeSchoolGrantProgram))),
    AfterSchoolGeneralFundedPrograms = as.integer(any(!is.na(AfterSchoolGeneralFundedPrograms))),
    btb_participation = ifelse(BeforeSchoolGrantProgram || AfterSchoolGeneralFundedPrograms, 1, 0)
  )

merged <- merged %>%
  left_join(btb_unique, by = "school_code")

names(merged)
head(merged)



df_clean <- merged %>%
  filter(!is.na(chronic_absenteeism)) %>%  # remove rows with missing outcome
  mutate(
    frpm_percent = frpm_rate * 100,
    food_eligible = if_else(frpm_percent >= 60, 1, 0),  # CEP cutoff
    btb = if_else(is.na(btb_participation), 0L, as.integer(btb_participation > 0)),
    county = as.factor(County.Code),
    district = as.factor(District.Code)
  )

mod_food_eligible <- gpss(
  chronic_absenteeism ~ food_eligible,
  data = df_clean
)


######################################################
# GP RDD
# chronic_abseentism ~ FRPM % - 40 cut off
######################################################
rdd_res_absenteeism_frpm_40_cutoff <- gp_rdd(
  df_clean$frpm_percent,
  df_clean$chronic_absenteeism,
  40
)
rdd_res_absenteeism_frpm_40_cutoff$tau     # estimated effect
rdd_res_absenteeism_frpm_40_cutoff$se      # standard error
rdd_res_absenteeism_frpm_40_cutoff$ci      # confidence interval
rdd_result_plot_1 <- gp_rdd_plot(rdd_res_absenteeism_frpm_40_cutoff) +
  geom_vline(xintercept = 40, linetype = "dashed") +
  coord_cartesian(xlim = c(20, 60)) +
  labs(title = "Zoomed-In View Around the Cutoff")

######################################################
# GP RDD
# chronic_abseentism ~ FRPM % - 75 cut off
######################################################
# Example using formula interface:
rdd_res_absenteeism_frpm_75_cutoff <- gp_rdd(
  df_clean$frpm_percent,
  df_clean$chronic_absenteeism,
  75
)
rdd_res_absenteeism_frpm_75_cutoff$tau     # estimated effect
rdd_res_absenteeism_frpm_75_cutoff$se      # standard error
rdd_res_absenteeism_frpm_75_cutoff$ci      # confidence interval
rdd_result_plot_2 <- gp_rdd_plot(rdd_res_absenteeism_frpm_75_cutoff) +
  geom_vline(xintercept = 40, linetype = "dashed") +
  coord_cartesian(xlim = c(20, 60)) +
  labs(title = "Zoomed-In View Around the Cutoff")


######################################################
# GP RDD
# BTB ~ FRPM % - 40 cut off
######################################################
rdd_res_absenteeism_BTB_40_cutoff <- gp_rdd(
  df_clean$frpm_percent,
  df_clean$btb,
  40
)
rdd_res_absenteeism_BTB_40_cutoff$tau     # estimated effect
rdd_res_absenteeism_BTB_40_cutoff$se      # standard error
rdd_res_absenteeism_BTB_40_cutoff$ci      # confidence interval
rdd_result_plot_3 <- gp_rdd_plot(rdd_res_absenteeism_BTB_40_cutoff) +
  geom_vline(xintercept = 40, linetype = "dashed") +
  coord_cartesian(xlim = c(20, 60)) +
  labs(title = "Zoomed-In View Around the Cutoff")


######################################################
# GP RDD
# BTB ~ FRPM % - 75 cut off
######################################################
rdd_res_absenteeism_BTB_75_cutoff <- gp_rdd(
  df_clean$frpm_percent,
  df_clean$btb,
  75
)
rdd_res_absenteeism_BTB_75_cutoff$tau     # estimated effect
rdd_res_absenteeism_BTB_75_cutoff$se      # standard error
rdd_res_absenteeism_BTB_75_cutoff$ci      # confidence interval
rdd_result_plot_4 <- gp_rdd_plot(rdd_res_absenteeism_BTB_75_cutoff) +
                      geom_vline(xintercept = 40, linetype = "dashed") +
                      coord_cartesian(xlim = c(20, 60)) +
                      labs(title = "Zoomed-In View Around the Cutoff")

