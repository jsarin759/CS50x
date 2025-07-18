#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.");
        return 1;
    }

    // The idea to use the jpg_found variable was influenced by this youtube video: https://www.youtube.com/watch?v=AJiDIxGEszs.
    // The boolean variable is set to false initially because no jpg has been found yet.
    bool jpg_found = false;
    int num_jpg = 0;
    uint8_t buffer[BLOCK_SIZE];
    char filename[8];
    FILE *img = NULL;

    // While there is still data left to read from the memory card
    while (fread(buffer, 1, BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If a jpg has already been found (jpg_found == true) and this isn't the first one found, the preceding image will close.
            if (jpg_found)
            {
                fclose(img);
            }
            // If this is the first jpg found (jpg_found == false), jpg_found is set to true.
            else
            {
                jpg_found = true;
            }
            sprintf(filename, "%03d.jpg", num_jpg);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                fclose(card);
                return 3;
            }
            num_jpg++;
        }
        // If jpgs have been found (jpg_found == true), then it will write the 512 byte block from the card into the image.
        // This only runs if jpg_found == true to prevent the code from writing to the image if no image has been found yet.
        if (jpg_found)
        {
            fwrite(buffer, 1, BLOCK_SIZE, img);
        }
    }

    fclose(img);
    fclose(card);
}
