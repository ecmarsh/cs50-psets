// Resizes bmp files: ./resize -i -o

#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        printf("Usage: (n) infile outfile\n");
        // echo $
        for (int i = 0, m = argc; i < m; i++)
        {
            if (i == (argc - 1))
            {
                printf("%s\n", argv[i]);
            }
            else
            {
                printf("%s ", argv[i]);
            }
        }
        // exit
        return 1;
    }

    // validate resize factor
    char *v = argv[1];
    for (int i = 0, vlen = strlen(v); i < vlen; i++)
    {
        // if any keys aren't digits, break
        if (!isdigit(v[i]))
        {
            printf("%s is not an intenger\n", v);
            return 2;
        }
    }

    // convert factor to integer
    int n = atoi(v);

    // check range
    if (n > 100 || n < 1)
    {
        printf("%i is not between 0 and 100.\n", n);
        return 3;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 4;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        printf("Could not create %s.\n", outfile);
        return 5;
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
        printf("Unsupported file format.\n");
        return 7;
    }

    // remember padding of infile
    int inPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // update BITMAPINFOHEEADER info
    bi.biWidth *= n;
    bi.biHeight *= n;
    // define new padding
    int outPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    // use new padding to update the image size
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + outPadding) * abs(bi.biHeight);
   
    // update BITMAPFILEHEADER size
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    
    // write headers
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);


   

    // iterate over infile's scanline and resize width
    for (int i = 0, biHeight = abs(bi.biHeight / n); i < biHeight; i++)
    {
        for (int l = 0; l < n; l++)
        {
            // iterate over pixels in row (scanline)
            for (int j = 0; j < bi.biWidth / n; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple pixel n times
                for (int f = 0; f < n; f++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // write outfile padding
            for (int k = 0; k < outPadding; k++)
            {
                fputc(0x00, outptr);
            }

            // move infile cursor back
            fseek(inptr, (sizeof(RGBTRIPLE) * bi.biWidth) / n * -1, SEEK_CUR);
        }

        // after arr filled, move forward again and skip over padding
        fseek(inptr, (sizeof(RGBTRIPLE) * bi.biWidth) / n  + inPadding, SEEK_CUR);
    }


    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);
    

    // success
    //printf("main ran correctly :)\n");
    return 0;
}

