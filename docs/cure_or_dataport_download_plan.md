# CURE-OR IEEE DataPort Download Plan v0.1

## Access Status

The IEEE DataPort page is open access, but the archive URLs are not
anonymously downloadable. A direct HEAD request to
`https://ieee-dataport.s3.amazonaws.com/open/708/01_no_challenge.tar.gz`
returned `403 Forbidden`.

This means one of these is required:

- browser login to IEEE DataPort and manual download; or
- IEEE DataPort AWS security credentials from the `View AWS Security
  Credentials` button on the dataset page.

Do not paste access keys into chat. If AWS credentials are used, configure them
locally in a terminal session or a temporary AWS profile.

## Allowed Local Target

All Full-CURE-OR files must stay under:

```text
/Volumes/980PRO/CURE-OR++
```

Recommended layout:

```text
/Volumes/980PRO/CURE-OR++/
  archives/
  raw/
    full_cure_or/
  tmp/
```

## Archive Manifest

The expected archive list is pinned in:

```text
configs/cure_or_dataport_archives_v01.json
```

Expected compressed total from IEEE DataPort file sizes:

```text
187.96 GB
```

The largest archives are:

- `09_saltpepper.tar.gz`: 44.22 GB;
- `18_grayscale_saltpepper.tar.gz`: 37.86 GB;
- `07_dirtylens1.tar.gz`: 16.04 GB;
- `08_dirtylens2.tar.gz`: 15.64 GB;
- `16_grayscale_dirtylens1.tar.gz`: 15.27 GB.

## Manual Download Route

1. Log in to IEEE DataPort in the browser.
2. Open the dataset page:
   `https://ieee-dataport.org/open-access/cure-or-challenging-unreal-and-real-environment-object-recognition`.
3. Download archive files into:
   `/Volumes/980PRO/CURE-OR++/archives`.
4. Run:

```bash
python3 scripts/verify_cure_or_archives.py \
  --archives-dir /Volumes/980PRO/CURE-OR++/archives
```

## AWS Route

If IEEE DataPort provides temporary AWS credentials, use the S3 URIs listed on
the page under `Access on AWS`. Keep credentials outside the repo and outside
chat.

After download, run the same verification command:

```bash
python3 scripts/verify_cure_or_archives.py \
  --archives-dir /Volumes/980PRO/CURE-OR++/archives
```

## First Subset To Download

For the first Full-CURE-OR probe, download only these archives first:

- `01_no_challenge.tar.gz`
- `02_resize.tar.gz`
- `05_blur.tar.gz`
- `09_saltpepper.tar.gz`
- `14_grayscale_blur.tar.gz`
- `18_grayscale_saltpepper.tar.gz`

This compressed subset is about 91.26 GB by IEEE DataPort file sizes and is
enough for the planned OpenCLIP probe.

Verify only the first probe subset:

```bash
python3 scripts/verify_cure_or_archives.py \
  --archives-dir /Volumes/980PRO/CURE-OR++/archives \
  --subset first_probe
```

## Current Local Status

Prepared directories:

```text
/Volumes/980PRO/CURE-OR++/archives
/Volumes/980PRO/CURE-OR++/raw/full_cure_or
/Volumes/980PRO/CURE-OR++/tmp
```

Current verification:

```text
Present archives: 0 / 18
```

Verification report:

```text
reports/cure_or_archive_verification_v01.json
```
