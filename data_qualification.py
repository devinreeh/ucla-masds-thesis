{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# -----------------------------------------------------------\n",
    "# 🧪 Causal Inference Data Validation Notebook\n",
    "# For Master's Thesis on CA School Interventions\n",
    "#\n",
    "# Goal: Validate datasets for use in RDD and DiD designs\n",
    "# Checks: Density near FRPM cutoff, panel structure, treatment variation\n",
    "# Datasets: frpm.csv, ases_funding.csv, cep_meals.csv, caaspp_scores.csv, absenteeism.csv\n",
    "# -----------------------------------------------------------"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "ename": "ValueError",
     "evalue": "You are trying to merge on object and float64 columns for key 'CDSCode'. If you wish to proceed you should use pd.concat",
     "output_type": "error",
     "traceback": [
      "\u001b[31m---------------------------------------------------------------------------\u001b[39m",
      "\u001b[31mValueError\u001b[39m                                Traceback (most recent call last)",
      "\u001b[36mCell\u001b[39m\u001b[36m \u001b[39m\u001b[32mIn[12]\u001b[39m\u001b[32m, line 39\u001b[39m\n\u001b[32m     36\u001b[39m frpm_2324[\u001b[33m\"\u001b[39m\u001b[33mSchool Name (Normalized)\u001b[39m\u001b[33m\"\u001b[39m] = frpm_2324[\u001b[33m\"\u001b[39m\u001b[33mSchool Name\u001b[39m\u001b[33m\"\u001b[39m].str.strip().str.upper()\n\u001b[32m     38\u001b[39m \u001b[38;5;66;03m# Merge FRPM 2021–2022 with BTB 2021–2022 on CDSCode\u001b[39;00m\n\u001b[32m---> \u001b[39m\u001b[32m39\u001b[39m merged_2122 = \u001b[43mpd\u001b[49m\u001b[43m.\u001b[49m\u001b[43mmerge\u001b[49m\u001b[43m(\u001b[49m\u001b[43mfrpm_2122\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mbtb_2122\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mon\u001b[49m\u001b[43m=\u001b[49m\u001b[33;43m\"\u001b[39;49m\u001b[33;43mCDSCode\u001b[39;49m\u001b[33;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mhow\u001b[49m\u001b[43m=\u001b[49m\u001b[33;43m\"\u001b[39;49m\u001b[33;43mleft\u001b[39;49m\u001b[33;43m\"\u001b[39;49m\u001b[43m)\u001b[49m\n\u001b[32m     41\u001b[39m \u001b[38;5;66;03m# Merge FRPM 2023–2024 with BTB 2023–2024 on normalized School Name\u001b[39;00m\n\u001b[32m     42\u001b[39m merged_2324 = pd.merge(frpm_2324, btb_2324, left_on=\u001b[33m\"\u001b[39m\u001b[33mSchool Name (Normalized)\u001b[39m\u001b[33m\"\u001b[39m, right_on=\u001b[33m\"\u001b[39m\u001b[33mSchool Name\u001b[39m\u001b[33m\"\u001b[39m, how=\u001b[33m\"\u001b[39m\u001b[33mleft\u001b[39m\u001b[33m\"\u001b[39m)\n",
      "\u001b[36mFile \u001b[39m\u001b[32m~/personal-projects/ucla-masds-thesis/venv/lib/python3.13/site-packages/pandas/core/reshape/merge.py:170\u001b[39m, in \u001b[36mmerge\u001b[39m\u001b[34m(left, right, how, on, left_on, right_on, left_index, right_index, sort, suffixes, copy, indicator, validate)\u001b[39m\n\u001b[32m    155\u001b[39m     \u001b[38;5;28;01mreturn\u001b[39;00m _cross_merge(\n\u001b[32m    156\u001b[39m         left_df,\n\u001b[32m    157\u001b[39m         right_df,\n\u001b[32m   (...)\u001b[39m\u001b[32m    167\u001b[39m         copy=copy,\n\u001b[32m    168\u001b[39m     )\n\u001b[32m    169\u001b[39m \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[32m--> \u001b[39m\u001b[32m170\u001b[39m     op = \u001b[43m_MergeOperation\u001b[49m\u001b[43m(\u001b[49m\n\u001b[32m    171\u001b[39m \u001b[43m        \u001b[49m\u001b[43mleft_df\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    172\u001b[39m \u001b[43m        \u001b[49m\u001b[43mright_df\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    173\u001b[39m \u001b[43m        \u001b[49m\u001b[43mhow\u001b[49m\u001b[43m=\u001b[49m\u001b[43mhow\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    174\u001b[39m \u001b[43m        \u001b[49m\u001b[43mon\u001b[49m\u001b[43m=\u001b[49m\u001b[43mon\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    175\u001b[39m \u001b[43m        \u001b[49m\u001b[43mleft_on\u001b[49m\u001b[43m=\u001b[49m\u001b[43mleft_on\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    176\u001b[39m \u001b[43m        \u001b[49m\u001b[43mright_on\u001b[49m\u001b[43m=\u001b[49m\u001b[43mright_on\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    177\u001b[39m \u001b[43m        \u001b[49m\u001b[43mleft_index\u001b[49m\u001b[43m=\u001b[49m\u001b[43mleft_index\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    178\u001b[39m \u001b[43m        \u001b[49m\u001b[43mright_index\u001b[49m\u001b[43m=\u001b[49m\u001b[43mright_index\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    179\u001b[39m \u001b[43m        \u001b[49m\u001b[43msort\u001b[49m\u001b[43m=\u001b[49m\u001b[43msort\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    180\u001b[39m \u001b[43m        \u001b[49m\u001b[43msuffixes\u001b[49m\u001b[43m=\u001b[49m\u001b[43msuffixes\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    181\u001b[39m \u001b[43m        \u001b[49m\u001b[43mindicator\u001b[49m\u001b[43m=\u001b[49m\u001b[43mindicator\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    182\u001b[39m \u001b[43m        \u001b[49m\u001b[43mvalidate\u001b[49m\u001b[43m=\u001b[49m\u001b[43mvalidate\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    183\u001b[39m \u001b[43m    \u001b[49m\u001b[43m)\u001b[49m\n\u001b[32m    184\u001b[39m     \u001b[38;5;28;01mreturn\u001b[39;00m op.get_result(copy=copy)\n",
      "\u001b[36mFile \u001b[39m\u001b[32m~/personal-projects/ucla-masds-thesis/venv/lib/python3.13/site-packages/pandas/core/reshape/merge.py:807\u001b[39m, in \u001b[36m_MergeOperation.__init__\u001b[39m\u001b[34m(self, left, right, how, on, left_on, right_on, left_index, right_index, sort, suffixes, indicator, validate)\u001b[39m\n\u001b[32m    803\u001b[39m \u001b[38;5;28mself\u001b[39m._validate_tolerance(\u001b[38;5;28mself\u001b[39m.left_join_keys)\n\u001b[32m    805\u001b[39m \u001b[38;5;66;03m# validate the merge keys dtypes. We may need to coerce\u001b[39;00m\n\u001b[32m    806\u001b[39m \u001b[38;5;66;03m# to avoid incompatible dtypes\u001b[39;00m\n\u001b[32m--> \u001b[39m\u001b[32m807\u001b[39m \u001b[38;5;28;43mself\u001b[39;49m\u001b[43m.\u001b[49m\u001b[43m_maybe_coerce_merge_keys\u001b[49m\u001b[43m(\u001b[49m\u001b[43m)\u001b[49m\n\u001b[32m    809\u001b[39m \u001b[38;5;66;03m# If argument passed to validate,\u001b[39;00m\n\u001b[32m    810\u001b[39m \u001b[38;5;66;03m# check if columns specified as unique\u001b[39;00m\n\u001b[32m    811\u001b[39m \u001b[38;5;66;03m# are in fact unique.\u001b[39;00m\n\u001b[32m    812\u001b[39m \u001b[38;5;28;01mif\u001b[39;00m validate \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m:\n",
      "\u001b[36mFile \u001b[39m\u001b[32m~/personal-projects/ucla-masds-thesis/venv/lib/python3.13/site-packages/pandas/core/reshape/merge.py:1508\u001b[39m, in \u001b[36m_MergeOperation._maybe_coerce_merge_keys\u001b[39m\u001b[34m(self)\u001b[39m\n\u001b[32m   1502\u001b[39m     \u001b[38;5;66;03m# unless we are merging non-string-like with string-like\u001b[39;00m\n\u001b[32m   1503\u001b[39m     \u001b[38;5;28;01melif\u001b[39;00m (\n\u001b[32m   1504\u001b[39m         inferred_left \u001b[38;5;129;01min\u001b[39;00m string_types \u001b[38;5;129;01mand\u001b[39;00m inferred_right \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;129;01min\u001b[39;00m string_types\n\u001b[32m   1505\u001b[39m     ) \u001b[38;5;129;01mor\u001b[39;00m (\n\u001b[32m   1506\u001b[39m         inferred_right \u001b[38;5;129;01min\u001b[39;00m string_types \u001b[38;5;129;01mand\u001b[39;00m inferred_left \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;129;01min\u001b[39;00m string_types\n\u001b[32m   1507\u001b[39m     ):\n\u001b[32m-> \u001b[39m\u001b[32m1508\u001b[39m         \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mValueError\u001b[39;00m(msg)\n\u001b[32m   1510\u001b[39m \u001b[38;5;66;03m# datetimelikes must match exactly\u001b[39;00m\n\u001b[32m   1511\u001b[39m \u001b[38;5;28;01melif\u001b[39;00m needs_i8_conversion(lk.dtype) \u001b[38;5;129;01mand\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m needs_i8_conversion(rk.dtype):\n",
      "\u001b[31mValueError\u001b[39m: You are trying to merge on object and float64 columns for key 'CDSCode'. If you wish to proceed you should use pd.concat"
     ]
    }
   ],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "ename": "FileNotFoundError",
     "evalue": "[Errno 2] No such file or directory: '/Users/devinreeh/personal-projects/ucla-masds-thesis/data/BeyondTheBellSchoolSitePrograms-20212022 copy.csv'",
     "output_type": "error",
     "traceback": [
      "\u001b[31m---------------------------------------------------------------------------\u001b[39m",
      "\u001b[31mFileNotFoundError\u001b[39m                         Traceback (most recent call last)",
      "\u001b[36mCell\u001b[39m\u001b[36m \u001b[39m\u001b[32mIn[7]\u001b[39m\u001b[32m, line 33\u001b[39m\n\u001b[32m     31\u001b[39m \u001b[38;5;66;03m# Load BTB program files\u001b[39;00m\n\u001b[32m     32\u001b[39m btb_2324 = pd.read_csv(btb_2324_file)\n\u001b[32m---> \u001b[39m\u001b[32m33\u001b[39m btb_2122 = \u001b[43mpd\u001b[49m\u001b[43m.\u001b[49m\u001b[43mread_csv\u001b[49m\u001b[43m(\u001b[49m\u001b[43mbtb_2122_file\u001b[49m\u001b[43m)\u001b[49m\n\u001b[32m     35\u001b[39m \u001b[38;5;66;03m# Normalize school names for 2023–2024 join\u001b[39;00m\n\u001b[32m     36\u001b[39m btb_2324[\u001b[33m\"\u001b[39m\u001b[33mSchool Name\u001b[39m\u001b[33m\"\u001b[39m] = btb_2324[\u001b[33m\"\u001b[39m\u001b[33mSchool Name\u001b[39m\u001b[33m\"\u001b[39m].str.strip().str.upper()\n",
      "\u001b[36mFile \u001b[39m\u001b[32m~/personal-projects/ucla-masds-thesis/venv/lib/python3.13/site-packages/pandas/io/parsers/readers.py:1026\u001b[39m, in \u001b[36mread_csv\u001b[39m\u001b[34m(filepath_or_buffer, sep, delimiter, header, names, index_col, usecols, dtype, engine, converters, true_values, false_values, skipinitialspace, skiprows, skipfooter, nrows, na_values, keep_default_na, na_filter, verbose, skip_blank_lines, parse_dates, infer_datetime_format, keep_date_col, date_parser, date_format, dayfirst, cache_dates, iterator, chunksize, compression, thousands, decimal, lineterminator, quotechar, quoting, doublequote, escapechar, comment, encoding, encoding_errors, dialect, on_bad_lines, delim_whitespace, low_memory, memory_map, float_precision, storage_options, dtype_backend)\u001b[39m\n\u001b[32m   1013\u001b[39m kwds_defaults = _refine_defaults_read(\n\u001b[32m   1014\u001b[39m     dialect,\n\u001b[32m   1015\u001b[39m     delimiter,\n\u001b[32m   (...)\u001b[39m\u001b[32m   1022\u001b[39m     dtype_backend=dtype_backend,\n\u001b[32m   1023\u001b[39m )\n\u001b[32m   1024\u001b[39m kwds.update(kwds_defaults)\n\u001b[32m-> \u001b[39m\u001b[32m1026\u001b[39m \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[43m_read\u001b[49m\u001b[43m(\u001b[49m\u001b[43mfilepath_or_buffer\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mkwds\u001b[49m\u001b[43m)\u001b[49m\n",
      "\u001b[36mFile \u001b[39m\u001b[32m~/personal-projects/ucla-masds-thesis/venv/lib/python3.13/site-packages/pandas/io/parsers/readers.py:620\u001b[39m, in \u001b[36m_read\u001b[39m\u001b[34m(filepath_or_buffer, kwds)\u001b[39m\n\u001b[32m    617\u001b[39m _validate_names(kwds.get(\u001b[33m\"\u001b[39m\u001b[33mnames\u001b[39m\u001b[33m\"\u001b[39m, \u001b[38;5;28;01mNone\u001b[39;00m))\n\u001b[32m    619\u001b[39m \u001b[38;5;66;03m# Create the parser.\u001b[39;00m\n\u001b[32m--> \u001b[39m\u001b[32m620\u001b[39m parser = \u001b[43mTextFileReader\u001b[49m\u001b[43m(\u001b[49m\u001b[43mfilepath_or_buffer\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43m*\u001b[49m\u001b[43m*\u001b[49m\u001b[43mkwds\u001b[49m\u001b[43m)\u001b[49m\n\u001b[32m    622\u001b[39m \u001b[38;5;28;01mif\u001b[39;00m chunksize \u001b[38;5;129;01mor\u001b[39;00m iterator:\n\u001b[32m    623\u001b[39m     \u001b[38;5;28;01mreturn\u001b[39;00m parser\n",
      "\u001b[36mFile \u001b[39m\u001b[32m~/personal-projects/ucla-masds-thesis/venv/lib/python3.13/site-packages/pandas/io/parsers/readers.py:1620\u001b[39m, in \u001b[36mTextFileReader.__init__\u001b[39m\u001b[34m(self, f, engine, **kwds)\u001b[39m\n\u001b[32m   1617\u001b[39m     \u001b[38;5;28mself\u001b[39m.options[\u001b[33m\"\u001b[39m\u001b[33mhas_index_names\u001b[39m\u001b[33m\"\u001b[39m] = kwds[\u001b[33m\"\u001b[39m\u001b[33mhas_index_names\u001b[39m\u001b[33m\"\u001b[39m]\n\u001b[32m   1619\u001b[39m \u001b[38;5;28mself\u001b[39m.handles: IOHandles | \u001b[38;5;28;01mNone\u001b[39;00m = \u001b[38;5;28;01mNone\u001b[39;00m\n\u001b[32m-> \u001b[39m\u001b[32m1620\u001b[39m \u001b[38;5;28mself\u001b[39m._engine = \u001b[38;5;28;43mself\u001b[39;49m\u001b[43m.\u001b[49m\u001b[43m_make_engine\u001b[49m\u001b[43m(\u001b[49m\u001b[43mf\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;28;43mself\u001b[39;49m\u001b[43m.\u001b[49m\u001b[43mengine\u001b[49m\u001b[43m)\u001b[49m\n",
      "\u001b[36mFile \u001b[39m\u001b[32m~/personal-projects/ucla-masds-thesis/venv/lib/python3.13/site-packages/pandas/io/parsers/readers.py:1880\u001b[39m, in \u001b[36mTextFileReader._make_engine\u001b[39m\u001b[34m(self, f, engine)\u001b[39m\n\u001b[32m   1878\u001b[39m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[33m\"\u001b[39m\u001b[33mb\u001b[39m\u001b[33m\"\u001b[39m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;129;01min\u001b[39;00m mode:\n\u001b[32m   1879\u001b[39m         mode += \u001b[33m\"\u001b[39m\u001b[33mb\u001b[39m\u001b[33m\"\u001b[39m\n\u001b[32m-> \u001b[39m\u001b[32m1880\u001b[39m \u001b[38;5;28mself\u001b[39m.handles = \u001b[43mget_handle\u001b[49m\u001b[43m(\u001b[49m\n\u001b[32m   1881\u001b[39m \u001b[43m    \u001b[49m\u001b[43mf\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m   1882\u001b[39m \u001b[43m    \u001b[49m\u001b[43mmode\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m   1883\u001b[39m \u001b[43m    \u001b[49m\u001b[43mencoding\u001b[49m\u001b[43m=\u001b[49m\u001b[38;5;28;43mself\u001b[39;49m\u001b[43m.\u001b[49m\u001b[43moptions\u001b[49m\u001b[43m.\u001b[49m\u001b[43mget\u001b[49m\u001b[43m(\u001b[49m\u001b[33;43m\"\u001b[39;49m\u001b[33;43mencoding\u001b[39;49m\u001b[33;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;28;43;01mNone\u001b[39;49;00m\u001b[43m)\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m   1884\u001b[39m \u001b[43m    \u001b[49m\u001b[43mcompression\u001b[49m\u001b[43m=\u001b[49m\u001b[38;5;28;43mself\u001b[39;49m\u001b[43m.\u001b[49m\u001b[43moptions\u001b[49m\u001b[43m.\u001b[49m\u001b[43mget\u001b[49m\u001b[43m(\u001b[49m\u001b[33;43m\"\u001b[39;49m\u001b[33;43mcompression\u001b[39;49m\u001b[33;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;28;43;01mNone\u001b[39;49;00m\u001b[43m)\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m   1885\u001b[39m \u001b[43m    \u001b[49m\u001b[43mmemory_map\u001b[49m\u001b[43m=\u001b[49m\u001b[38;5;28;43mself\u001b[39;49m\u001b[43m.\u001b[49m\u001b[43moptions\u001b[49m\u001b[43m.\u001b[49m\u001b[43mget\u001b[49m\u001b[43m(\u001b[49m\u001b[33;43m\"\u001b[39;49m\u001b[33;43mmemory_map\u001b[39;49m\u001b[33;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;28;43;01mFalse\u001b[39;49;00m\u001b[43m)\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m   1886\u001b[39m \u001b[43m    \u001b[49m\u001b[43mis_text\u001b[49m\u001b[43m=\u001b[49m\u001b[43mis_text\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m   1887\u001b[39m \u001b[43m    \u001b[49m\u001b[43merrors\u001b[49m\u001b[43m=\u001b[49m\u001b[38;5;28;43mself\u001b[39;49m\u001b[43m.\u001b[49m\u001b[43moptions\u001b[49m\u001b[43m.\u001b[49m\u001b[43mget\u001b[49m\u001b[43m(\u001b[49m\u001b[33;43m\"\u001b[39;49m\u001b[33;43mencoding_errors\u001b[39;49m\u001b[33;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[33;43m\"\u001b[39;49m\u001b[33;43mstrict\u001b[39;49m\u001b[33;43m\"\u001b[39;49m\u001b[43m)\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m   1888\u001b[39m \u001b[43m    \u001b[49m\u001b[43mstorage_options\u001b[49m\u001b[43m=\u001b[49m\u001b[38;5;28;43mself\u001b[39;49m\u001b[43m.\u001b[49m\u001b[43moptions\u001b[49m\u001b[43m.\u001b[49m\u001b[43mget\u001b[49m\u001b[43m(\u001b[49m\u001b[33;43m\"\u001b[39;49m\u001b[33;43mstorage_options\u001b[39;49m\u001b[33;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;28;43;01mNone\u001b[39;49;00m\u001b[43m)\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m   1889\u001b[39m \u001b[43m\u001b[49m\u001b[43m)\u001b[49m\n\u001b[32m   1890\u001b[39m \u001b[38;5;28;01massert\u001b[39;00m \u001b[38;5;28mself\u001b[39m.handles \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m\n\u001b[32m   1891\u001b[39m f = \u001b[38;5;28mself\u001b[39m.handles.handle\n",
      "\u001b[36mFile \u001b[39m\u001b[32m~/personal-projects/ucla-masds-thesis/venv/lib/python3.13/site-packages/pandas/io/common.py:873\u001b[39m, in \u001b[36mget_handle\u001b[39m\u001b[34m(path_or_buf, mode, encoding, compression, memory_map, is_text, errors, storage_options)\u001b[39m\n\u001b[32m    868\u001b[39m \u001b[38;5;28;01melif\u001b[39;00m \u001b[38;5;28misinstance\u001b[39m(handle, \u001b[38;5;28mstr\u001b[39m):\n\u001b[32m    869\u001b[39m     \u001b[38;5;66;03m# Check whether the filename is to be opened in binary mode.\u001b[39;00m\n\u001b[32m    870\u001b[39m     \u001b[38;5;66;03m# Binary mode does not support 'encoding' and 'newline'.\u001b[39;00m\n\u001b[32m    871\u001b[39m     \u001b[38;5;28;01mif\u001b[39;00m ioargs.encoding \u001b[38;5;129;01mand\u001b[39;00m \u001b[33m\"\u001b[39m\u001b[33mb\u001b[39m\u001b[33m\"\u001b[39m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;129;01min\u001b[39;00m ioargs.mode:\n\u001b[32m    872\u001b[39m         \u001b[38;5;66;03m# Encoding\u001b[39;00m\n\u001b[32m--> \u001b[39m\u001b[32m873\u001b[39m         handle = \u001b[38;5;28;43mopen\u001b[39;49m\u001b[43m(\u001b[49m\n\u001b[32m    874\u001b[39m \u001b[43m            \u001b[49m\u001b[43mhandle\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    875\u001b[39m \u001b[43m            \u001b[49m\u001b[43mioargs\u001b[49m\u001b[43m.\u001b[49m\u001b[43mmode\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    876\u001b[39m \u001b[43m            \u001b[49m\u001b[43mencoding\u001b[49m\u001b[43m=\u001b[49m\u001b[43mioargs\u001b[49m\u001b[43m.\u001b[49m\u001b[43mencoding\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    877\u001b[39m \u001b[43m            \u001b[49m\u001b[43merrors\u001b[49m\u001b[43m=\u001b[49m\u001b[43merrors\u001b[49m\u001b[43m,\u001b[49m\n\u001b[32m    878\u001b[39m \u001b[43m            \u001b[49m\u001b[43mnewline\u001b[49m\u001b[43m=\u001b[49m\u001b[33;43m\"\u001b[39;49m\u001b[33;43m\"\u001b[39;49m\u001b[43m,\u001b[49m\n\u001b[32m    879\u001b[39m \u001b[43m        \u001b[49m\u001b[43m)\u001b[49m\n\u001b[32m    880\u001b[39m     \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[32m    881\u001b[39m         \u001b[38;5;66;03m# Binary mode\u001b[39;00m\n\u001b[32m    882\u001b[39m         handle = \u001b[38;5;28mopen\u001b[39m(handle, ioargs.mode)\n",
      "\u001b[31mFileNotFoundError\u001b[39m: [Errno 2] No such file or directory: '/Users/devinreeh/personal-projects/ucla-masds-thesis/data/BeyondTheBellSchoolSitePrograms-20212022 copy.csv'"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "\n",
    "# Read each file's FRPM School-Level Data sheet manually\n",
    "print(\"Reading data/frpm/frpm1718.xlsx...\")\n",
    "df_1718 = pd.read_excel('data/frpm/frpm1718.xlsx', sheet_name=\"FRPM School-Level Data \", header=1)\n",
    "df_1718.columns = df_1718.columns.str.replace('\\n', '')\n",
    "df_1718['year'] = \"2017\"\n",
    "\n",
    "print(\"Reading data/frpm/frpm1819.xlsx...\")\n",
    "df_1819 = pd.read_excel('data/frpm/frpm1819.xlsx', sheet_name=\"FRPM School-Level Data \", header=1)\n",
    "df_1819.columns = df_1819.columns.str.replace('\\n', '')\n",
    "df_1819['year'] = \"2018\"\n",
    "\n",
    "print(\"Reading data/frpm/frpm1920.xlsx...\")\n",
    "df_1920 = pd.read_excel('data/frpm/frpm1920.xlsx', sheet_name=\"FRPM School-Level Data \", header=1)\n",
    "df_1920.columns = df_1920.columns.str.replace('\\n', '')\n",
    "df_1920['year'] = \"2019\"\n",
    "\n",
    "print(\"Reading data/frpm/frpm2021.xlsx...\")\n",
    "df_2021 = pd.read_excel('data/frpm/frpm2021.xlsx', sheet_name=\"FRPM School-Level Data \", header=1)\n",
    "df_2021.columns = df_2021.columns.str.replace('\\n', '')\n",
    "df_2021['year'] = \"2020\"\n",
    "\n",
    "print(\"Reading data/frpm/frpm2122_v2.xlsx...\")\n",
    "df_2122 = pd.read_excel('data/frpm/frpm2122_v2.xlsx', sheet_name=\"FRPM School-Level Data \", header=1)\n",
    "df_2122.columns = df_2122.columns.str.replace('\\n', '')\n",
    "df_2122['year'] = \"2021\"\n",
    "\n",
    "print(\"Reading data/frpm/frpm2223.xlsx...\")\n",
    "df_2223 = pd.read_excel('data/frpm/frpm2223.xlsx', sheet_name=\"FRPM School-Level Data\", header=1)\n",
    "df_2223.columns = df_2223.columns.str.replace('\\n', '')\n",
    "df_2223['year'] = \"2022\"\n",
    "\n",
    "print(\"Reading data/frpm/frpm2324.xlsx...\")\n",
    "df_2324 = pd.read_excel('data/frpm/frpm2324.xlsx', sheet_name=\"FRPM School-Level Data\", header=1)\n",
    "df_2324.columns = df_2324.columns.str.replace('\\n', '')\n",
    "df_2324['year'] = \"2023\"\n",
    "\n",
    "# Combine all dataframes\n",
    "combined_df = pd.concat([df_1718, df_1819, df_1920, df_2021, df_2122, df_2223, df_2324], \n",
    "                       axis=0, \n",
    "                       ignore_index=True)\n",
    "\n",
    "# Save combined data\n",
    "output_file = 'data/frpm/combined_frpm.csv'\n",
    "combined_df.to_csv(output_file, index=False)\n",
    "print(f\"\\nCombined data saved to {output_file}\")\n",
    "print(f\"Total rows: {len(combined_df)}\")\n",
    "print(f\"Total files processed: 7\")\n",
    "\n",
    "# Display first few rows of combined data\n",
    "print(\"\\nFirst few rows of combined data:\")\n",
    "print(combined_df.head())\n",
    "\n",
    "# Display column names\n",
    "print(\"\\nColumns in the dataset:\")\n",
    "print(combined_df.columns.tolist()) \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "venv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
