#include <stdio.h>
#include <stdlib.h> // For EXIT_SUCCESS and EXIT_FAILURE
#include <string.h>

#define DATA_LENGTH 20 // Maximum characters to read per line (including newline and null terminator)

struct msg
{
    char data[DATA_LENGTH];
};

struct pkt
{
    unsigned int seqnum;
    unsigned int acknum;
    unsigned int checksum;
    char payload[DATA_LENGTH];
};

struct sender
{
    int seq;
};

struct receiver
{
    int ack;
};

u_int16_t get_checksum(struct pkt *packet)
{
    u_int16_t sum = 0;
    size_t size = sizeof(struct pkt);
    u_int16_t *ptr = (u_int16_t *)packet;
    while (size >= 2) // Because of alignment requirement, size will always be multiple of 4
    {
        sum += *ptr;
        size -= 2;
        ptr += 1;
    };
    return sum ^ 0xFF;
};

void to_layer3() {
};

int main()
{
    FILE *filePointer;                  // Declare a file pointer
    char lineBuffer[DATA_LENGTH];       // Buffer to store each line read
    const char *filename = "alice.txt"; // The name of the file to read

    // --- Step 1: Open the file for reading ("r") ---
    filePointer = fopen(filename, "r");

    // --- Step 2: Check if the file was opened successfully ---
    if (filePointer == NULL)
    {
        perror("Error opening file");                           // Print the system error message (e.g., "No such file or directory")
        fprintf(stderr, "Could not open file: %s\n", filename); // Print our own message to standard error
        return EXIT_FAILURE;                                    // Exit the program indicating failure
    }

    struct pkt *Packet = malloc(sizeof(struct pkt));

    Packet->acknum = 0;
    Packet->seqnum = 0;
    strncpy(Packet->payload, "This is an example payload for the packet.", DATA_LENGTH - 1);

    get_checksum(Packet);

    free(Packet);
    fclose(filePointer);

    return EXIT_SUCCESS; // Exit the program indicating success
};
