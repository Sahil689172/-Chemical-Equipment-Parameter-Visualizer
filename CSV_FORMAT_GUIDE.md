# CSV File Format Guide

## Required CSV Format

Your CSV file **must** have these exact column headers in the first row:

```
Equipment Name,Type,Flowrate,Pressure,Temperature
```

### Column Details:

1. **Equipment Name** - Name of the equipment (text)
2. **Type** - Type of equipment (text)
3. **Flowrate** - Flowrate value (number, in L/min)
4. **Pressure** - Pressure value (number, in bar)
5. **Temperature** - Temperature value (number, in °C)

### Important Notes:

- Column names are **case-sensitive** and must match exactly
- Column names must be in this exact order
- All columns are required
- Flowrate, Pressure, and Temperature must be numeric values
- Empty rows are allowed but will be skipped

---

## Example CSV File

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor R-101,Continuous Stirred Tank Reactor,450.5,8.2,125.0
Pump P-401,Centrifugal Pump,550.0,12.5,45.0
Heat Exchanger HE-301,Shell and Tube Heat Exchanger,280.75,5.8,95.0
```

---

## Sample File Location

A correctly formatted sample file is available at:
```
sample_data/sample_equipment_data.csv
```

You can use this file to test the upload functionality.

---

## Common Errors

### Error: "Missing required columns"

**Cause:** Your CSV doesn't have the required column headers.

**Solution:**
1. Open your CSV file in Excel or a text editor
2. Check the first row has these exact headers:
   - `Equipment Name`
   - `Type`
   - `Flowrate`
   - `Pressure`
   - `Temperature`
3. Make sure there are no extra spaces or typos
4. Save the file and try uploading again

### Error: "Invalid file type"

**Cause:** File doesn't have `.csv` extension.

**Solution:**
- Rename your file to end with `.csv`
- Make sure it's actually a CSV file, not Excel (.xlsx) or other format

### Error: "Data validation failed"

**Cause:** Some rows have invalid data (non-numeric values in Flowrate, Pressure, or Temperature columns).

**Solution:**
- Check that Flowrate, Pressure, and Temperature columns contain only numbers
- Remove any text or special characters from these columns
- Make sure there are no empty cells in required fields

---

## Converting Other CSV Files

If you have a CSV file with different column names, you need to:

1. **Rename columns** to match the required format:
   - Your column → Required column
   - Example: `Name` → `Equipment Name`
   - Example: `Equipment Type` → `Type`

2. **Reorder columns** if needed to match:
   - Equipment Name (first)
   - Type (second)
   - Flowrate (third)
   - Pressure (fourth)
   - Temperature (fifth)

3. **Remove extra columns** that aren't needed

4. **Ensure numeric columns** (Flowrate, Pressure, Temperature) contain only numbers

---

## Quick Test

To test if your CSV is formatted correctly:

1. Open `sample_data/sample_equipment_data.csv` in a text editor
2. Compare your CSV's first row with the sample file
3. Make sure column names match exactly
4. Try uploading the sample file first to verify the system works
5. Then modify your CSV to match the format

---

## Need Help?

If you're still having issues:

1. Check the error message - it will tell you which columns are missing
2. Compare your CSV with the sample file
3. Make sure you're using a plain CSV file (not Excel format)
4. Verify all required columns are present and spelled correctly
