/**
 * Resizes the image by factor n
 */
       
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    { 
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }

    int n = atoi(argv[1]);
    if(n > 100 || n < 1){
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];
    
    int lengthinfile = strlen(argv[2]);
    int lengthoutfile = strlen(argv[3]);
    if(infile[lengthinfile-4] != '.' && infile[lengthinfile-3] != 'b' && infile[lengthinfile-2] != 'm' && infile[lengthinfile-1] != 'p'){
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }
    if(outfile[lengthoutfile-4] != '.' && outfile[lengthoutfile-3] != 'b' && outfile[lengthoutfile-2] != 'm' && outfile[lengthoutfile-1] != 'p'){
        fprintf(stderr, "Usage: ./resize n infile outfile\n");
        return 1;
    }
    
    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
     // Change info Header
    int biWidthold = bi.biWidth;
    bi.biWidth = bi.biWidth * n;
    // printf("%d\n",bi.biWidth);
    int biHeightold = bi.biHeight;
    bi.biHeight = bi.biHeight * n;
    // printf("%d\n",bi.biHeight);
    int paddingold = (4 - (biWidthold * sizeof(RGBTRIPLE)) % 4) % 4;
   // printf("%d\n",paddingold);
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    //printf("%d\n",padding);
    
   
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth)+padding)*abs(bi.biHeight);
    //printf("%d\n",bi.biSize);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    
    //printf("%d\n",bf.bfSize);
    
    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    
    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // determine padding for scanlines
    //int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    // iterate over infile's scanlines
    for (int i = 0; i < abs(biHeightold); i++)
    {
        RGBTRIPLE rowvalue[bi.biWidth];
        int pointertorow = 0;
        // iterate over pixels in scanline
        for (int j = 0; j < biWidthold; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            
            // Have a pixel with RGB value
            
             //printf("Heeyyy");
            // write RGB triple to array
            for(int k = 0; k < n; k++){
              //  printf("Heeyyy");
                rowvalue[pointertorow++] = triple;
                //fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                
            }
                
        }

        
        
        for(int j = 0; j < n; j++){
            
            fwrite(rowvalue, sizeof(RGBTRIPLE),bi.biWidth, outptr);
               
            for (int k = 0; k < padding; k++)
                fputc(0x00, outptr);
        }
        // skip over padding, if any
        fseek(inptr, paddingold, SEEK_CUR);
        
        
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
