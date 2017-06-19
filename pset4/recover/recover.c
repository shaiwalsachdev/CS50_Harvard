/**
 * Recover the data from card
 */
       
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[1];
    

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }
    
    BYTE buffer[512];
    
    int numberofimages = -1;
    FILE *outptr = NULL;
   
    char* imgname = malloc(8*sizeof(char));
    while(fread(buffer, 512, 1, inptr) == 1){ 
        // Check the JPEG
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0){
          
            if(outptr != NULL){
                fclose(outptr);
            }
            numberofimages++;
            //Make image name
            sprintf(imgname,"%03i.jpg",numberofimages);
            outptr = fopen(imgname, "wb");
            if (outptr == NULL)
            {
                fprintf(stderr, "Could not open %s.\n", infile);
                return 1;
            }
            
        }
        // Write into new file
        if(outptr != NULL){
            fwrite(&buffer,  512, 1, outptr);
        }
            
    }
    
   
    
    // close infile
    fclose(inptr);
     free(imgname);
    fclose(outptr);

    // success
    return 0;
}
