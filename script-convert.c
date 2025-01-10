#include <stdio.h>
#include <stdlib.h> // for atoi

// symmetric

int main(int argc, char *argv[])
{
    if (argc != 5)
    {
        printf("Usage: %s <og_start> <og_end> <new_start> <new_end>\n", argv[0]);
        return 1;
    }

    int og_start = atoi(argv[1]);
    int og_end = atoi(argv[2]);
    int new_start = atoi(argv[3]);
    int new_end = atoi(argv[4]);

    if (new_end == new_start)
    {
        printf("Error: Division by zero.\n");
        return 1;
    }

    int scaled_value = (og_start - og_end) / (new_start - new_end);

    printf("Scaled Value: %d\n", scaled_value);

    return 0;
}
