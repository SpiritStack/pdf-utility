#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
from PyPDF2 import PdfReader, PdfWriter
import img2pdf
from PIL import Image
import tempfile
import shutil
import math

class PDFProcessor:
    def __init__(self):
        self.quality_settings = {
            'low': {'quality': 30, 'dpi': 72},
            'medium': {'quality': 60, 'dpi': 150},
            'high': {'quality': 90, 'dpi': 300}
        }
    
    def compress_pdf(self, input_path, output_path, quality='medium'):
        """Compress PDF with specified quality level"""
        if quality not in self.quality_settings:
            raise ValueError(f"Invalid quality level. Choose from {list(self.quality_settings.keys())}")
        
        settings = self.quality_settings[quality]
        temp_dir = tempfile.mkdtemp()
        
        try:
            with open(input_path, "rb") as f:
                pdf = PdfReader(f)
                writer = PdfWriter()
                
                for page in pdf.pages:
                    writer.add_page(page)
                
                temp_pdf = os.path.join(temp_dir, "temp.pdf")
                with open(temp_pdf, "wb") as f_out:
                    writer.write(f_out)
                
                self._run_ghostscript(
                    temp_pdf,
                    output_path,
                    dpi=settings['dpi'],
                    quality=settings['quality']
                )
                
        finally:
            shutil.rmtree(temp_dir)
    
    def split_pdf(self, input_path, max_size_mb=25, output_prefix=None):
        """Split PDF into parts of specified max size (in MB)"""
        max_size_bytes = max_size_mb * 1024 * 1024
        
        # Determine output prefix from input filename if not provided
        if output_prefix is None:
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_prefix = os.path.join(os.path.dirname(input_path), base_name)
        
        with open(input_path, "rb") as f:
            input_size = os.path.getsize(input_path)
            if input_size <= max_size_bytes:
                print("Input PDF is smaller than specified size. No splitting needed.")
                return [input_path]
            
            pdf = PdfReader(f)
            parts = []
            current_part = 1
            current_writer = PdfWriter()
            current_size_estimate = 0
            
            for page in pdf.pages:
                # Estimate size of current page
                temp_writer = PdfWriter()
                temp_writer.add_page(page)
                with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                    temp_writer.write(temp_file)
                    temp_file.seek(0)
                    temp_size = os.path.getsize(temp_file.name)
                
                # Check if we need to start a new part
                if (current_size_estimate + temp_size > max_size_bytes and 
                    len(current_writer.pages) > 0):
                    # Save current part
                    part_path = f"{output_prefix}_part{current_part}.pdf"
                    with open(part_path, "wb") as f_out:
                        current_writer.write(f_out)
                    parts.append(part_path)
                    
                    # Start new part
                    current_part += 1
                    current_writer = PdfWriter()
                    current_size_estimate = 0
                
                current_writer.add_page(page)
                current_size_estimate += temp_size
            
            # Save the final part
            if len(current_writer.pages) > 0:
                part_path = f"{output_prefix}_part{current_part}.pdf"
                with open(part_path, "wb") as f_out:
                    current_writer.write(f_out)
                parts.append(part_path)
            
            return parts
    
    def _run_ghostscript(self, input_path, output_path, dpi=150, quality=75):
        """Use Ghostscript for PDF compression"""
        if not shutil.which("gs"):
            raise RuntimeError("Ghostscript (gs) not found. Please install it first.")
        
        cmd = [
            "gs",
            "-sFONTPATH=/tmp",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS=/{self._get_gs_preset(dpi, quality)}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_path}",
            input_path
        ]
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Ghostscript compression failed: {e}")
    
    def _get_gs_preset(self, dpi, quality):
        """Map quality settings to Ghostscript presets"""
        if dpi <= 72:
            return "screen"
        elif dpi <= 150:
            return "ebook"
        elif dpi <= 300:
            return "printer"
        else:
            return "prepress"

def main():
    parser = argparse.ArgumentParser(
        description="PDF Compression and Splitting Utility",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("-o", "--output", help="Output PDF file path (for compression)")
    parser.add_argument("-q", "--quality", choices=["low", "medium", "high"], 
                       default="medium", help="Compression quality level")
    parser.add_argument("-s", "--split", type=int, 
                       help="Split PDF into parts of this size (in MB)")
    parser.add_argument("-p", "--prefix", 
                       help="Prefix for split files (default: input filename)")
    parser.add_argument("-v", "--verbose", action="store_true", 
                       help="Show detailed processing information")
    
    args = parser.parse_args()
    processor = PDFProcessor()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.split:
            if args.verbose:
                print(f"Splitting PDF into parts of {args.split}MB each...")
            
            parts = processor.split_pdf(args.input, args.split, args.prefix)
            
            if args.verbose:
                print(f"Created {len(parts)} parts:")
                for part in parts:
                    size_mb = os.path.getsize(part) / (1024 * 1024)
                    print(f" - {part} ({size_mb:.1f} MB)")
        else:
            if not args.output:
                print("Error: Output path required for compression.", file=sys.stderr)
                sys.exit(1)
            
            if args.verbose:
                print(f"Compressing PDF with {args.quality} quality...")
                original_size = os.path.getsize(args.input) / (1024 * 1024)
                print(f"Original size: {original_size:.2f} MB")
            
            processor.compress_pdf(args.input, args.output, args.quality)
            
            if args.verbose:
                new_size = os.path.getsize(args.output) / (1024 * 1024)
                print(f"Compressed size: {new_size:.2f} MB")
                print(f"Reduction: {((original_size - new_size) / original_size) * 100:.1f}%")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
