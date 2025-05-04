# PDF Processor Utility

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

A powerful command-line tool for compressing and splitting PDF files with customizable quality settings. Perfect for handling large PDFs, optimizing document sizes, and preparing files for sharing.

## Features

- **Smart PDF Compression** with three quality presets:
  - Low (smallest size)
  - Medium (balanced quality/size)
  - High (best quality)
  
- **Intelligent PDF Splitting**:
  - Split by exact file size (MB)
  - Automatic part numbering
  - Preserves original filename structure

- **Cross-Platform**:
  - Works on macOS and Linux
  - Lightweight with minimal dependencies

- **Additional Features**:
  - Verbose mode for detailed processing info
  - Ghostscript integration for professional-grade compression
  - Progress reporting

## Installation

### Prerequisites
- Python 3.7+
- Ghostscript (for compression features)

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/SpiritStack/pdf-utility.git
cd pdf-utility

# Install dependencies
pip install -r requirements.txt

# Install Ghostscript
# macOS:
brew install ghostscript

# Linux (Debian/Ubuntu):
sudo apt-get install ghostscript
```

## Usage

### Basic Commands

**Compress a PDF:**
```bash
./pdf_processor.py input.pdf -o compressed.pdf -q [low|medium|high]
```

**Split a PDF by size:**
```bash
# Split into 25MB parts (auto-named as input_part1.pdf, input_part2.pdf, etc.)
./pdf_processor.py large.pdf -s 25

# Split with custom prefix
./pdf_processor.py large.pdf -s 25 -p myprefix
```

### Advanced Options

| Flag | Description | Example |
|------|-------------|---------|
| `-o` | Output file (compression) | `-o output.pdf` |
| `-q` | Quality level | `-q high` |
| `-s` | Split size in MB | `-s 50` |
| `-p` | Custom prefix for split files | `-p document_` |
| `-v` | Verbose mode (show details) | `-v` |

### Examples

**1. Compress with high quality:**
```bash
./pdf_processor.py presentation.pdf -o presentation_compressed.pdf -q high -v
```

**2. Split a 100MB PDF into 30MB parts:**
```bash
./pdf_processor.py thesis.pdf -s 30 -v
```
*Outputs:* `thesis_part1.pdf`, `thesis_part2.pdf`, etc.

**3. Compress and see size reduction:**
```bash
./pdf_processor.py scan.pdf -o scan_small.pdf -q medium -v
```
*Sample output:*
```
Compressing PDF with medium quality...
Original size: 45.2 MB
Compressed size: 12.7 MB
Reduction: 71.9%
```

## Technical Details

### Dependencies
- [PyPDF2](https://pypi.org/project/PyPDF2/) - PDF manipulation
- [img2pdf](https://pypi.org/project/img2pdf/) - Image handling
- [Pillow](https://pypi.org/project/Pillow/) - Image processing
- Ghostscript - Professional PDF compression

### How It Works
1. **Compression**:
   - Analyzes PDF structure
   - Optimizes images and fonts
   - Uses Ghostscript for final compression

2. **Splitting**:
   - Calculates optimal page breaks
   - Preserves document integrity
   - Accurate size estimation

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues or feature requests, please [open an issue](https://github.com/SpiritStack/pdf-utility/issues).

---

**Pro Tip**: For best compression results, use the `high` quality setting first, then try `medium` if file size needs to be smaller.
