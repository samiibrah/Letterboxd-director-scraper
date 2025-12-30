# Letterboxd Director Scraper

A Python script that enriches your Letterboxd export data by scraping director information for each film you've watched.

## What It Does

This script takes your Letterboxd `watched.csv` export file and adds a `Directors` column by scraping director information from each film's Letterboxd page. The enhanced data is saved to a new CSV file.

## Prerequisites

- Python 3.6+
- Required packages:
  ```bash
  pip install pandas requests beautifulsoup4
  ```

## Setup

1. **Export your Letterboxd data:**
   - Go to Letterboxd Settings → Import & Export → Export Your Data
   - Download and extract the ZIP file

2. **Configure the script:**
   - Open the script and update `EXPORT_DIR` to point to your extracted Letterboxd export folder:
     ```python
     EXPORT_DIR = Path("/path/to/your/letterboxd-export")
     ```

## Usage

Run the script:
```bash
python letterboxd_director_scraper.py
```

The script will:
- Read your `watched.csv` file
- Scrape director information from each film's Letterboxd page
- Save the results to `watched_with_directors.csv` in the same directory

Progress updates are printed every 25 films.

## Features

- **Smart Column Detection**: Automatically finds the URL column (looks for "Letterboxd URI", "URL", or "Link")
- **Error Handling**: Continues processing even if individual films fail
- **Rate Limiting**: Includes a 0.5-second delay between requests to be respectful to Letterboxd's servers
- **Multiple Directors**: Handles films with multiple directors (comma-separated)

## Output

The output CSV file contains all original columns plus a new `Directors` column with comma-separated director names.

## Notes

- **Processing Time**: Expect ~0.5 seconds per film due to rate limiting
- **Network Required**: Active internet connection needed to scrape Letterboxd
- **Respectful Scraping**: Built-in delays prevent overloading Letterboxd's servers
- **Error Resilience**: Failed requests leave the Directors field empty and continue processing

## Troubleshooting

**"Could not find a URL column" error:**
- Check that your `watched.csv` contains a column with film URLs
- The script looks for columns named "Letterboxd URI", "URL", or "Link" (case-insensitive)

**Empty Directors fields:**
- May indicate network issues or changes to Letterboxd's page structure
- Check console output for specific error messages

## License

Free to use and modify as needed.
