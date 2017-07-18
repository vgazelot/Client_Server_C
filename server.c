#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <assert.h>
#include <pthread.h>
#include <sys/mman.h>
#include <stdio.h>
static int *globcd;
void connected(int sock);
char * aes_encrypt(char *text);

char * aes_encrypt(char *text) {
	FILE *f = fopen("/root/workspace/client-server/text.txt","w");
	if (f== NULL) {
		printf("Error opening text.txt\n");
		exit(1);
	}
	fprintf(f,"%s",text);
	fclose(f);
	system("python /root/workspace/client-server/aes.py -e -s");
	char * buffer = NULL;
	int string_size,read_size;
	FILE *fr = fopen("/root/workspace/client-server/textEncrypted.txt","r");
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
		fclose(fr);
	}
	else {
		printf("error when opening textEncrypted.txt\n");
	}

	return buffer;
}

char * aes_decrypt(char * text) {

	FILE * f= fopen("/root/workspace/client-server/textEncrypted.txt","w");
	if (f== NULL) {
		printf("Error opening text.txt\n");
		exit(1);
	}
	fprintf(f,"%s",text);
	fclose(f);
	system("python /root/workspace/client-server/aes.py -d -s");
	char * buffer = NULL;
	int string_size,read_size;
	FILE *fr = fopen("/root/workspace/client-server/textDecrypted.txt","r");
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
		fclose(fr);
	}
	else {
		printf("error when opening textDecrypted.txt\n");
	}
	return buffer;
}


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
int whois(int sock) {
	char login[4096];
	char mdp[4096];
	int nb = 0;
	while(nb < 3) {
		char *textEncrypted = aes_encrypt("Login :");
		send(sock,textEncrypted,strlen(textEncrypted),0);
		recv(sock,login,sizeof(login),0);
		char *login_p = aes_decrypt(login);
		char *textEncrypted2 = aes_encrypt("MDP :");
		send(sock,textEncrypted2,strlen(textEncrypted2),0);
		recv(sock,mdp,sizeof(mdp),0);
		char *mdp_p = aes_decrypt(mdp);
		if (strcmp(login_p,"admin") == 0 && strcmp(mdp_p,"1234") == 0) {
			return 1;
		}
		nb++;
	}
	return 0;
	
}
void *process(void *socket) {
	int sock = *(int*) socket;
	if(whois(sock)) {
		connected(sock);
	}
	else {
		char *textEncrypted = aes_encrypt("3 Fails: You have been kicked, Bye ;)");
		send(sock,textEncrypted,strlen(textEncrypted),0);
	}
	return 0;
}
void connected(int sock) {
	globcd = mmap(NULL,sizeof *globcd, PROT_READ | PROT_WRITE,MAP_SHARED | MAP_ANONYMOUS, -1, 0);
 	char client_message[4096], serv_message[4096];
	int read_size;
	clearCharTab(client_message,1024);	
	char welcome[] = "!********************\\ Welcome ! /********************!\n";
	char *textEncrypted = aes_encrypt(welcome);
	send(sock,textEncrypted,strlen(textEncrypted),0);
	//send(sock,welcome,sizeof(welcome),0);
	while((read_size = recv(sock, client_message , 2000 , 0)) > 0 ) {
		char *client_message_p = aes_decrypt(client_message);
		*globcd = 0;
		int link[2];
	 	pid_t pid;
	  	char foo[4096];
	
		if(pipe(link)==-1) {
	   		die("pipe");
		}	
		if ((pid = fork()) == -1){
		   	die("fork");
		}
		
		if(pid == 0) {
			dup2 (link[1], STDOUT_FILENO);
			close(link[0]);
			close(link[1]);
			if(strcmp(client_message_p,"rls") == 0) {
                                pid_t pidexec = fork();
                                if(pidexec == 0) {
					execl("/bin/ls","ls","-l",NULL);
                                }
                        }
                        else if(strcmp(client_message_p,"rpwd") == 0) {
                                pid_t pidexec = fork();
                                if(pidexec == 0) {
					execl("/bin/pwd","pwd",NULL);
                                }
                        }
                        else if(strcmp(client_message_p,"rcd") == 0) {
				*globcd = 1;
				char *textEncrypted = aes_encrypt("Où souhaitez vous aller ? ");
				send(sock,textEncrypted,strlen(textEncrypted),0);
				clearCharTab(client_message,sizeof(client_message));
				recv(sock,client_message,4096,0);
                                pid_t pidexec = fork();
                                if(pidexec == 0) {
					execl("/bin/echo","echo",aes_decrypt(client_message),NULL);
                                }
				clearCharTab(client_message,sizeof(client_message));

                        }
			exit(0);
				
		}else {
				
			close(link[1]);
			int n;
			memset(foo,0,sizeof(foo));
			clearCharTab(foo,sizeof(foo));
			n=read(link[0], foo, sizeof(foo));
			foo[n-1] = '\0';
			memset(serv_message,0,sizeof(serv_message));
			clearCharTab(serv_message,sizeof(serv_message));
			strcpy(serv_message,foo);
			if(*globcd == 1){
				if(chdir(serv_message) == 0 ) {
					char *textEncrypted2 = aes_encrypt("CDOK");
					send(sock,textEncrypted2,strlen(textEncrypted2),0);
				}
				else {
					perror("chdir");
					char *textEncrypted = aes_encrypt("CDKO");
					send(sock,textEncrypted,strlen(textEncrypted),0);
				}
			}else {
				char *textEncrypted = aes_encrypt(serv_message);
				send(sock,textEncrypted,strlen(textEncrypted),0);
			}
			memset(serv_message,0,sizeof(serv_message));
			memset(client_message,0,sizeof(client_message));
			memset(foo,0,sizeof(foo));
			clearCharTab(foo,sizeof(foo));
			clearCharTab(client_message,sizeof(client_message));	
			clearCharTab(serv_message,sizeof(serv_message));
			wait(NULL);	
		}
		if(read_size == 0) {
			puts("Client disconnected");
			fflush(stdout);
		}
		else if(read_size == -1) {
			perror("recv failed");
		}
	}
	munmap(globcd,sizeof *globcd);
}
int main(){
 	int serv_sock, client_sock;
 	struct sockaddr_in serverAddr;
 	struct sockaddr_storage serverStorage;
 	socklen_t addr_size;


 	serv_sock = socket(PF_INET, SOCK_STREAM, 0);
 	 
 	serverAddr.sin_family = AF_INET;
  	serverAddr.sin_port = htons(7891);
  	serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
  	memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);  

  	bind(serv_sock, (struct sockaddr *) &serverAddr, sizeof(serverAddr));

  	if(listen(serv_sock,5)==0)
   		printf("Listening\n");
	else
		printf("Error\n");

	addr_size = sizeof serverStorage;
	while(1) {
	
	  	client_sock = accept(serv_sock, (struct sockaddr *) &serverStorage, &addr_size);
		if (client_sock < 0) {
         		perror("ERROR on accept");
         		exit(1);
      		}
		pthread_t  thread;
		int *new_sock = malloc(1);
		*new_sock = client_sock;
     		if(pthread_create(&thread, NULL, process, (void*)new_sock) < 0) {
			perror("could not creat thread");
			return 1;
		}
	}
	return 0;
}
