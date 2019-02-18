#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define BLOCK_SIZE 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        // print err
        fprintf(stderr, "Usage: ./recover -jpeg\n");
        for (int i = 0, m = argc; i < m; i++)
        {
            if (i == (argc - 1))
            {
                fprintf(stderr, "%s\n", argv[i]);
            }
            else
            {
                fprintf(stderr, "%s ", argv[i]);
            }
        }
        // exit
        return 1;
    }

    // remember file
    char *rawfile = argv[1];

    // ensure file can be opened
    FILE *raw_file = fopen(rawfile, "r");
    if (raw_file == NULL)
    {
        printf("Could not open %s.\n", rawfile);
        return 2;
    }

    // temp storage block
    BYTE buffer[512];
    
    // counter for file names
    int i = 0;
    
    // initialize outptr & name space
    char filename[8];
    FILE *img = NULL;
    
    // stream file until end
    while (true)
    {
        size_t b = fread(buffer, sizeof(BYTE), BLOCK_SIZE, raw_file);
        
        // on new img, break
        if (b == 0 && feof(raw_file))
        {
            break;
        }

        // check for jpeg header
        bool isJpeg = buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;
        
        // close out if new img
        if (isJpeg && img != NULL)
        {
            fclose(img);
            ++i;
        }
        
        // open new one for writing
        if (isJpeg)
        {
            sprintf(filename, "%03i.jpg", i);
            img = fopen(filename, "w");
        }
        
        // if there's an open file & no new start, write
        if (img != NULL)
        {
            fwrite(buffer, sizeof(BYTE), b, img);
        }
    }

    // close out files for no segfault
    fclose(img);
    // close read
    fclose(raw_file);

    // success & exit
    printf("main ran successfully :D\n");
    return 0;
}
