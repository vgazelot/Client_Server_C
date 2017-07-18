#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <sys/wait.h>
void die(char * mess) {
	perror(mess);
	exit(1);
}
void clearCharTab(char buffer[],int size) {
	int i;
	for(i=0;i<size;i++) {
		buffer[i] = '\0';
	}
}

char * aes_encrypt(char *text) {
        FILE *f = fopen("/root/workspace/client-server/textC.txt","w");
        if (f== NULL) {
                printf("Error opening text.txt\n");
                exit(1);
        }
        fprintf(f,"%s",text);
        fclose(f);
        system("python /root/workspace/client-server/aes.py -e -c");
        char * buffer = NULL;
        int string_size,read_size;
        FILE *fr = fopen("/root/workspace/client-server/textEncryptedC.txt","r");
        if (fr) {
                fseek(fr,0,SEEK_END);
                string_size = ftell(fr);
                rewind(fr);
                buffer = (char *) malloc(sizeof(char) * (string_size +1));
                read_size = fread(buffer,sizeof(char),string_size,fr);
                buffer[string_size] = '\0';
                if(string_size != read_size) {
                        //ERROR
                        printf("Error when reading textEncrypted\n");
                        free(buffer);
                        buffer = NULL;
                }
        }
        else {
                printf("error when opening textEncrypted.txt\n");
        }
        return buffer;
}

char * aes_decrypt(char * text) {
        FILE * f= fopen("/root/workspace/client-server/textEncryptedC.txt","w");
        if (f== NULL) {
                printf("Error opening tex.txt\n");
                exit(1);
        }
        fprintf(f,"%s",text);
        fclose(f);
        system("python /root/workspace/client-server/aes.py -d -c");
        char * buffer = NULL;
        int string_size,read_size;
        FILE *fr = fopen("/root/workspace/client-server/textDecryptedC.txt","r");
        if (fr) {
                fseek(fr,0,SEEK_END);
                string_size = ftell(fr);
                rewind(fr);
                buffer = (char *) malloc(sizeof(char) * (string_size +1));
                read_size = fread(buffer,sizeof(char),string_size,fr);
                buffer[string_size] = '\0';
                if(string_size != read_size) {
                        //ERROR
                        printf("Error when reading textDecrypted\n");
                        free(buffer);
                        buffer = NULL;
                }
        }
        else {
                printf("error when opening textDecrypted.txt\n");
        }
        return buffer;
}

int main(){
  	int sock;
  	char message[1024], server_reply[8096];
  	struct sockaddr_in serverAddr;
  	socklen_t addr_size;

  	sock = socket(PF_INET, SOCK_STREAM, 0);
  	serverAddr.sin_family = AF_INET;
  	serverAddr.sin_port = htons(7891);
  	serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
  	memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);  

  	addr_size = sizeof serverAddr;
  	connect(sock, (struct sockaddr *) &serverAddr, addr_size);
	pid_t pid = fork();
	if(pid == 0) {
  		while((recv(sock, server_reply, 8096,0))>0) {
			printf("%s\n",aes_decrypt(server_reply));
			clearCharTab(server_reply,sizeof(server_reply));
			fflush(stdout);
  		}
		exit(0);
	}
	else {
		do{
			system("sleep 0.1");
			clearCharTab(message,sizeof(message));
			printf("\n>");
  	      		scanf("%s",message);
			//printf("%s\n",message);
			if(strcmp(message,"ls") == 0) {
				pid_t pidexec = fork();
				if(pidexec == 0) {
					execl("/bin/ls","ls",NULL);
				}
			}
			else if(strcmp(message,"pwd") == 0) {
				pid_t pidexec = fork();
				if(pidexec == 0) {
					execl("/bin/pwd","pwd",NULL);
				}
			}
			else if(strcmp(message,"cd") == 0) {
				char rep[100];
				printf("Où voulez vous vous déplacer ? \n");
				scanf("%s",rep);
				
				chdir(rep);
			}
			else if(strcmp(message,"quit") == 0) {
				exit(1);
			}
  	      		else {
				char *textEncrypted = aes_encrypt(message);
                		send(sock,textEncrypted,strlen(textEncrypted),0);
  	      		}
		}while(strcmp(message,"quit") != 0);
	}
  	close(sock);
  	return 0;
}
