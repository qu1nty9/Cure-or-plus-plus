# CURE-OR Download Status v0.2

## Current State

The IEEE DataPort page is reachable and lists 18 archives for the complete
CURE-OR release. The first probe subset has been downloaded and extracted
manually under the allowed external-disk project folder.

Direct anonymous archive access is blocked:

```text
HEAD https://ieee-dataport.s3.amazonaws.com/open/708/01_no_challenge.tar.gz
HTTP 403 Forbidden
```

This is expected for IEEE DataPort. The page says Open Access files are
available to logged-in IEEE DataPort users.

## External Disk

Allowed work root:

```text
/Volumes/980PRO/CURE-OR++
```

Prepared folders:

```text
/Volumes/980PRO/CURE-OR++/archives
/Volumes/980PRO/CURE-OR++/raw/full_cure_or
/Volumes/980PRO/CURE-OR++/tmp
```

Disk status after staging the first extracted subset:

```text
/Volumes/980PRO: 931 GiB total, 656 GiB available
```

## Archive Manifest

Archive list:

```text
configs/cure_or_dataport_archives_v01.json
```

Expected compressed total:

```text
187.96 GB
```

First probe subset:

```text
01_no_challenge.tar.gz
02_resize.tar.gz
05_blur.tar.gz
09_saltpepper.tar.gz
14_grayscale_blur.tar.gz
18_grayscale_saltpepper.tar.gz
```

Expected compressed subset total:

```text
91.26 GB
```

Current extracted subset:

```text
01_no_challenge: 3.8G
02_resize: 13G
05_blur: 15G
09_saltpepper: 56G
14_grayscale_blur: 15G
18_grayscale_saltpepper: 50G
```

Total staged under `/Volumes/980PRO/CURE-OR++`:

```text
153G
```

Usable image files in the extracted subset, ignoring `._*` files:

```text
312,500
```

## Verification

Current `.tar.gz` archive verification:

```text
Present: 0 / 18
```

This is expected because the first subset is currently present as extracted
folders, not as `.tar.gz` archive files.

Report:

```text
reports/cure_or_archive_verification_v01.json
```

## First Probe Status

Completed:

- extracted-folder manifests built;
- CLIP ViT-B/16 and OpenCLIP ViT-B/32 LAION2B evaluated;
- comparison tables and figures written;
- report written to `reports/full_cure_or_probe_v01.md`.

## Next Required Action

To move beyond the first probe, either:

- download and extract the remaining official challenge folders into
  `/Volumes/980PRO/CURE-OR++/archives`; or
- increase sampling inside the currently staged six folders.

For compressed archives, run:

```bash
python3 scripts/verify_cure_or_archives.py \
  --archives-dir /Volumes/980PRO/CURE-OR++/archives \
  --subset first_probe
```
