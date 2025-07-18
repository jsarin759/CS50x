#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    long num = get_long("Number: "); // change to get_long
    long digits = 0;
    long on_digits = 0;
    long off_digits = 0;
    long start = 0;
    while (num > 0)
    {
        long digit = num % 10;
        digits++;

        if (digits % 2 == 0)
        {
            digit = digit * 2;
            if (digit >= 10)
            {
                while (digit > 0)
                {
                    long placeholder = digit % 10;
                    digit = digit / 10;
                    digit = floor(digit);
                    on_digits += placeholder;
                }
            }
            on_digits += digit;
        }
        else
        {
            off_digits += digit;
        }
        num = num / 10;
        num = floor(num);

        if (num == 4 || num == 34 || num == 37 || num == 51 || num == 52 || num == 53 ||
            num == 54 || num == 55)
        {
            start = num;
        }
    }

    long checksum = on_digits + off_digits;

    if (checksum % 10 == 0)
    {
        if ((digits == 13 || digits == 16) && start == 4)
        {
            printf("VISA\n");
        }
        else if ((start == 34 || start == 37) && digits == 15)
        {
            printf("AMEX\n");
        }
        else if ((start == 51 || start == 52 || start == 53 || start == 54 || start == 55) &&
                 digits == 16)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
