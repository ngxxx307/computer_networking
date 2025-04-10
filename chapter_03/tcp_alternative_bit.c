#include <stdio.h>
#include <stdlib.h> // For EXIT_SUCCESS and EXIT_FAILURE
#include <string.h>
#include <stdbool.h>
#include <pthread.h>

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
    bool ack;
};

struct client
{
    int seq;
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

void input(struct client *c, struct pkt *packet)
{
}

void to_layer3(struct client *receiver, struct pkt *packet)
{
}

void to_layer5()
{
}

void *init_sender()
{
}

void *init_receiver()
{
}

int main()
{
    pthread_t threadA, threadB;

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

    struct client *sender = malloc(sizeof(struct client));
    sender->ack = 0;
    sender->seq = 0;

    struct client *receiver = malloc(sizeof(struct client));
    receiver->ack = 0;
    receiver->seq = 0;

    while (fgets(lineBuffer, sizeof(lineBuffer), filePointer) != NULL)
    {
        printf("%s", lineBuffer);
        to_layer3();
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
