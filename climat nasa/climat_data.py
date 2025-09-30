# scripts/clean_data.py
import argparse, re
import numpy as np, pandas as pd

def clean_col_name(name):
    s = str(name).strip()
    s = s.replace('\n', ' ').replace('\r', ' ')
    s = re.sub(r'[\s\-]+', '_', s)
    s = re.sub(r'[^0-9a-zA-Z_]', '', s)
    s = re.sub(r'__+', '_', s)
    return s.strip('_').lower()

def main(inpath, outpath, drop_thresh=0.6):
    df = pd.read_csv(inpath, low_memory=False, encoding='utf-8')
    # normalize columns
    df.columns = [clean_col_name(c) for c in df.columns]
    # detect and parse date columns by name
    date_candidates = [c for c in df.columns if 'date' in c or 'time' in c or 'timestamp' in c]
    for c in date_candidates:
        parsed = pd.to_datetime(df[c], errors='coerce', infer_datetime_format=True)
        if parsed.notna().mean() > 0.2:
            df[c] = parsed
    # coerce object-like columns to numeric if at least half convert
    for c in df.columns:
        if df[c].dtype == object:
            coerced = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.strip(), errors='coerce')
            if coerced.notna().sum() / len(df) >= 0.5:
                df[c] = coerced
    # drop high-missing columns
    miss_frac = df.isna().mean()
    to_drop = miss_frac[miss_frac > drop_thresh].index.tolist()
    df.drop(columns=to_drop, inplace=True)
    # impute numeric -> median, categorical -> mode or 'unknown'
    num_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for c in num_cols:
        if df[c].isna().sum():
            df[c].fillna(df[c].median(), inplace=True)
    for c in cat_cols:
        if df[c].isna().sum():
            try:
                df[c].fillna(df[c].mode(dropna=True)[0], inplace=True)
            except:
                df[c].fillna('unknown', inplace=True)
    # drop exact duplicates
    df.drop_duplicates(inplace=True)
    # capping outliers (IQR) for numeric columns
    for c in num_cols:
        if df[c].nunique() > 10:
            q1 = df[c].quantile(0.25); q3 = df[c].quantile(0.75)
            iqr = q3 - q1
            lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
            df[c] = np.where(df[c] < lower, lower, np.where(df[c] > upper, upper, df[c]))
    # add date features if a date column exists
    date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c]) or pd.api.types.is_datetime64tz_dtype(df[c])]
    if date_cols:
        dcol = date_cols[0]
        df['year'] = df[dcol].dt.year
        df['month'] = df[dcol].dt.month
        df['day'] = df[dcol].dt.day
        df['weekofyear'] = df[dcol].dt.isocalendar().week.astype(int)
    df.to_csv(outpath, index=False)
    print("Saved cleaned file to:", outpath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    main(args.input, args.output)

# scripts/clean_data.py
import argparse, re
import numpy as np, pandas as pd

def clean_col_name(name):
    s = str(name).strip()
    s = s.replace('\n', ' ').replace('\r', ' ')
    s = re.sub(r'[\s\-]+', '_', s)
    s = re.sub(r'[^0-9a-zA-Z_]', '', s)
    s = re.sub(r'__+', '_', s)
    return s.strip('_').lower()

def main(inpath, outpath, drop_thresh=0.6):
    df = pd.read_csv(inpath, low_memory=False, encoding='utf-8')
    # normalize columns
    df.columns = [clean_col_name(c) for c in df.columns]

    # detect and parse date columns
    date_candidates = [c for c in df.columns if 'date' in c or 'time' in c or 'timestamp' in c]
    for c in date_candidates:
        parsed = pd.to_datetime(df[c], errors='coerce', infer_datetime_format=True)
        if parsed.notna().mean() > 0.2:
            df[c] = parsed

    # coerce numeric-like strings to numbers
    for c in df.columns:
        if df[c].dtype == object:
            coerced = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.strip(), errors='coerce')
            if coerced.notna().sum() / len(df) >= 0.5:
                df[c] = coerced

    # drop columns with too many missing values
    miss_frac = df.isna().mean()
    to_drop = miss_frac[miss_frac > drop_thresh].index.tolist()
    df.drop(columns=to_drop, inplace=True)

    # impute missing values
    num_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for c in num_cols:
        if df[c].isna().sum():
            df[c].fillna(df[c].median(), inplace=True)
    for c in cat_cols:
        if df[c].isna().sum():
            try:
                df[c].fillna(df[c].mode(dropna=True)[0], inplace=True)
            except:
                df[c].fillna('unknown', inplace=True)

    # remove duplicates
    df.drop_duplicates(inplace=True)

    # cap outliers (IQR)
    for c in num_cols:
        if df[c].nunique() > 10:
            q1 = df[c].quantile(0.25); q3 = df[c].quantile(0.75)
            iqr = q3 - q1
            lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
            df[c] = np.where(df[c] < lower, lower, np.where(df[c] > upper, upper, df[c]))

    # add date features if available
    date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    if date_cols:
        dcol = date_cols[0]
        df['year'] = df[dcol].dt.year
        df['month'] = df[dcol].dt.month
        df['day'] = df[dcol].dt.day
        df['weekofyear'] = df[dcol].dt.isocalendar().week.astype(int)

    # save cleaned file
    df.to_csv(outpath, index=False)
    print("✅ Saved cleaned file to:", outpath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    main(args.input, args.output)

