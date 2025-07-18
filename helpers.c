#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            int red = image[i][j].rgbtRed;
            int avg = round((red + green + blue) / 3.0);
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;
        }
    }
    return;
}

void swap(RGBTRIPLE *a, RGBTRIPLE *b)
{
    RGBTRIPLE tmp = *a;
    *a = *b;
    *b = tmp;
}
// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0, n = (width / 2); j < n; j++)
        {
            swap(&image[i][j], &image[i][width - 1 - j]);
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE RGBTEMP[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float surrounding_pixels = 0;
            int total_red = 0;
            int total_green = 0;
            int total_blue = 0;

            total_red += image[i][j].rgbtRed;
            total_green += image[i][j].rgbtGreen;
            total_blue += image[i][j].rgbtBlue;
            surrounding_pixels++;

            if (i > 0) // if not top row
            {
                total_red += image[i - 1][j].rgbtRed;
                total_green += image[i - 1][j].rgbtGreen;
                total_blue += image[i - 1][j].rgbtBlue;
                surrounding_pixels++;
            }

            if (i < (height - 1)) // if not bottom row
            {
                total_red += image[i + 1][j].rgbtRed;
                total_green += image[i + 1][j].rgbtGreen;
                total_blue += image[i + 1][j].rgbtBlue;
                surrounding_pixels++;
            }

            if (j > 0) // if not left column
            {
                total_red += image[i][j - 1].rgbtRed;
                total_green += image[i][j - 1].rgbtGreen;
                total_blue += image[i][j - 1].rgbtBlue;
                surrounding_pixels++;
            }

            if (j < (width - 1)) // if not right column
            {
                total_red += image[i][j + 1].rgbtRed;
                total_green += image[i][j + 1].rgbtGreen;
                total_blue += image[i][j + 1].rgbtBlue;
                surrounding_pixels++;
            }

            if (j < (width - 1) && i > 0) // if not right column nor top row
            {
                total_red += image[i - 1][j + 1].rgbtRed;
                total_green += image[i - 1][j + 1].rgbtGreen;
                total_blue += image[i - 1][j + 1].rgbtBlue;
                surrounding_pixels++;
            }

            if (j < (width - 1) && i < (height - 1)) // if not right column nor bottom row
            {
                total_red += image[i + 1][j + 1].rgbtRed;
                total_green += image[i + 1][j + 1].rgbtGreen;
                total_blue += image[i + 1][j + 1].rgbtBlue;
                surrounding_pixels++;
            }

            if (j > 0 && i > 0) // if not left column nor top row
            {
                total_red += image[i - 1][j - 1].rgbtRed;
                total_green += image[i - 1][j - 1].rgbtGreen;
                total_blue += image[i - 1][j - 1].rgbtBlue;
                surrounding_pixels++;
            }

            if (j > 0 && i < (height - 1)) // if not left column nor bottom row
            {
                total_red += image[i + 1][j - 1].rgbtRed;
                total_green += image[i + 1][j - 1].rgbtGreen;
                total_blue += image[i + 1][j - 1].rgbtBlue;
                surrounding_pixels++;
            }

            int avg_red = round(total_red / surrounding_pixels);
            int avg_green = round(total_green / surrounding_pixels);
            int avg_blue = round(total_blue / surrounding_pixels);

            RGBTEMP[i][j].rgbtBlue = avg_blue;
            RGBTEMP[i][j].rgbtGreen = avg_green;
            RGBTEMP[i][j].rgbtRed = avg_red;
        }
    }

    for (int k = 0; k < height; k++)
    {
        for (int l = 0; l < width; l++)
        {
            image[k][l].rgbtBlue = RGBTEMP[k][l].rgbtBlue;
            image[k][l].rgbtGreen = RGBTEMP[k][l].rgbtGreen;
            image[k][l].rgbtRed = RGBTEMP[k][l].rgbtRed;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE RGBTEMP[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float Gx_red = 0;
            float Gx_green = 0;
            float Gx_blue = 0;
            float Gy_red = 0;
            float Gy_green = 0;
            float Gy_blue = 0;

            Gx_red += image[i][j].rgbtRed * 0;
            Gx_green += image[i][j].rgbtGreen * 0;
            Gx_blue += image[i][j].rgbtBlue * 0;

            Gy_red += image[i][j].rgbtRed * 0;
            Gy_green += image[i][j].rgbtGreen * 0;
            Gy_blue += image[i][j].rgbtBlue * 0;

            if (i > 0) // if not top row
            {
                Gx_red += image[i - 1][j].rgbtRed * 0;
                Gx_green += image[i - 1][j].rgbtGreen * 0;
                Gx_blue += image[i - 1][j].rgbtBlue * 0;

                Gy_red += image[i - 1][j].rgbtRed * -2;
                Gy_green += image[i - 1][j].rgbtGreen * -2;
                Gy_blue += image[i - 1][j].rgbtBlue * -2;
            }

            if (i < (height - 1)) // if not bottom row
            {
                Gx_red += image[i + 1][j].rgbtRed * 0;
                Gx_green += image[i + 1][j].rgbtGreen * 0;
                Gx_blue += image[i + 1][j].rgbtBlue * 0;

                Gy_red += image[i + 1][j].rgbtRed * 2;
                Gy_green += image[i + 1][j].rgbtGreen * 2;
                Gy_blue += image[i + 1][j].rgbtBlue * 2;
            }

            if (j > 0) // if not left column
            {
                Gx_red += image[i][j - 1].rgbtRed * -2;
                Gx_green += image[i][j - 1].rgbtGreen * -2;
                Gx_blue += image[i][j - 1].rgbtBlue * -2;

                Gy_red += image[i][j - 1].rgbtRed * 0;
                Gy_green += image[i][j - 1].rgbtGreen * 0;
                Gy_blue += image[i][j - 1].rgbtBlue * 0;
            }

            if (j < (width - 1)) // if not right column
            {
                Gx_red += image[i][j + 1].rgbtRed * 2;
                Gx_green += image[i][j + 1].rgbtGreen * 2;
                Gx_blue += image[i][j + 1].rgbtBlue * 2;

                Gy_red += image[i][j + 1].rgbtRed * 0;
                Gy_green += image[i][j + 1].rgbtGreen * 0;
                Gy_blue += image[i][j + 1].rgbtBlue * 0;
            }

            if (j < (width - 1) && i > 0) // if not right column nor top row
            {
                Gx_red += image[i - 1][j + 1].rgbtRed * 1;
                Gx_green += image[i - 1][j + 1].rgbtGreen * 1;
                Gx_blue += image[i - 1][j + 1].rgbtBlue * 1;

                Gy_red += image[i - 1][j + 1].rgbtRed * -1;
                Gy_green += image[i - 1][j + 1].rgbtGreen * -1;
                Gy_blue += image[i - 1][j + 1].rgbtBlue * -1;
            }

            if (j < (width - 1) && i < (height - 1)) // if not right column nor bottom row
            {
                Gx_red += image[i + 1][j + 1].rgbtRed * 1;
                Gx_green += image[i + 1][j + 1].rgbtGreen * 1;
                Gx_blue += image[i + 1][j + 1].rgbtBlue * 1;

                Gy_red += image[i + 1][j + 1].rgbtRed * 1;
                Gy_green += image[i + 1][j + 1].rgbtGreen * 1;
                Gy_blue += image[i + 1][j + 1].rgbtBlue * 1;
            }

            if (j > 0 && i > 0) // if not left column nor top row
            {
                Gx_red += image[i - 1][j - 1].rgbtRed * -1;
                Gx_green += image[i - 1][j - 1].rgbtGreen * -1;
                Gx_blue += image[i - 1][j - 1].rgbtBlue * -1;

                Gy_red += image[i - 1][j - 1].rgbtRed * -1;
                Gy_green += image[i - 1][j - 1].rgbtGreen * -1;
                Gy_blue += image[i - 1][j - 1].rgbtBlue * -1;
            }

            if (j > 0 && i < (height - 1)) // if not left column nor bottom row
            {
                Gx_red += image[i + 1][j - 1].rgbtRed * -1;
                Gx_green += image[i + 1][j - 1].rgbtGreen * -1;
                Gx_blue += image[i + 1][j - 1].rgbtBlue * -1;

                Gy_red += image[i + 1][j - 1].rgbtRed * 1;
                Gy_green += image[i + 1][j - 1].rgbtGreen * 1;
                Gy_blue += image[i + 1][j - 1].rgbtBlue * 1;
            }

            int val_red = round(sqrt(pow(Gx_red, 2) + pow(Gy_red, 2)));
            if (val_red > 255)
            {
                val_red = 255;
            }
            int val_green = round(sqrt(pow(Gx_green, 2) + pow(Gy_green, 2)));
            if (val_green > 255)
            {
                val_green = 255;
            }
            int val_blue = round(sqrt(pow(Gx_blue, 2) + pow(Gy_blue, 2)));
            if (val_blue > 255)
            {
                val_blue = 255;
            }

            RGBTEMP[i][j].rgbtBlue = val_blue;
            RGBTEMP[i][j].rgbtGreen = val_green;
            RGBTEMP[i][j].rgbtRed = val_red;
        }
    }

    for (int k = 0; k < height; k++)
    {
        for (int l = 0; l < width; l++)
        {
            image[k][l].rgbtBlue = RGBTEMP[k][l].rgbtBlue;
            image[k][l].rgbtGreen = RGBTEMP[k][l].rgbtGreen;
            image[k][l].rgbtRed = RGBTEMP[k][l].rgbtRed;
        }
    }
    return;
}
