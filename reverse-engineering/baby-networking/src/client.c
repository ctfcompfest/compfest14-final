#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

char ip[16];
char port[6];
char name[16];
char host[16];
char public_key[50];
char finalMsg[50];

void encrypt(char* str, char* key){
    int str_size = strlen(str);
    int key_size = strlen(key);
    int i = 0;
    while (i < str_size && i < key_size){
        int newCharOffset = ((str[i]-'a')+(key[i]-'.'))%26;
        str[i] = newCharOffset + 'a';
        i++;
    }
}

char* generateKey(){
    puts("Enter name");
    scanf("%15s", name);
    puts("Enter host");
    scanf("%15s", host);
    puts("Enter ip");
    scanf("%15s", ip);
    puts("Enter port");
    scanf("%5s", port);

    memset(public_key, 0, 50);
    encrypt(name, ip);
    encrypt(host, ip);

    strcat(public_key, name);
    strcat(public_key, host);
    strcat(public_key, port);

    return public_key;
}

char* generateMessage(char* key, char* message){
    memset(finalMsg, 0, 50);
    finalMsg[0] = 'f';
    finalMsg[1] = 'l';
    finalMsg[2] = 'a';
    finalMsg[3] = 'g';
    strcat(finalMsg, key);

    return finalMsg;
}

void connectServer(char* key, char* message){
    char *ip = "127.0.0.1";
    int port = 5566;
    puts("TODO: private key parser");

    int sock;
    struct sockaddr_in addr;
    socklen_t addr_size;
    char buffer[1024];
    int n;
    
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0){
        perror("[-]Socket error");
        exit(1);
    }
    printf("[+]TCP server socket created.\n");
    
    memset(&addr, '\0', sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = port;
    addr.sin_addr.s_addr = inet_addr(ip);
    
    connect(sock, (struct sockaddr*)&addr, sizeof(addr));
    printf("Connected to the server.\n");

    bzero(buffer, 1024);
    strcpy(buffer, generateMessage(key, message));
    send(sock, buffer, strlen(buffer), 0);
    
    bzero(buffer, 1024);
    recv(sock, buffer, sizeof(buffer), 0);
    printf("Server: %s\n", buffer);
    
    close(sock);
    printf("Disconnected from the server.\n");
}

int main(){
    char* public_key;

    puts("Welcome to baby networking apps");
    puts("What do you want to do?");
    puts("1. Create public key");
    puts("2. Connect with private key (format: <name>_<host>_<ip>_<port>) (on maintenance)");
    int inp;
    scanf("%d", &inp);

    if (inp == 1){
        public_key = generateKey();
        printf("%s\n", public_key);
    }
    else{
        puts("No");
        exit(0);
    }

    exit(0);
}