#ifndef _LOGGER_H_
#define _LOGGER_H_

#ifdef _WIN32
    #define SEP_CHAR '\\'
    #define SEP "\\"
#else 
    #define SEP_CHAR '/'
    #define SEP "/"
#endif

#include <string.h>
#include <stdlib.h>

#define MAX_NAME 512
#define MAX_PATH 523

typedef struct logger_info {
    char name[MAX_NAME];
    char file_path[MAX_PATH];
}logger_info;

struct file_path {

};

logger_info * new_logger(const char *name, const char *path) {
    logger_info * temp;
    temp = (logger_info *)malloc(sizeof(logger_info));

    strcpy(temp->name, name);

    char * temp_path;
    int path_length = strlen(path) + strlen(name);
    if (path[strlen(path)-1] != SEP_CHAR)
        path_length++;

    temp_path = (char *)malloc(path_length);
    strcat(temp_path, path);
    if (path[strlen(path)-1] != SEP_CHAR)
        strcat(temp_path, SEP);
    strcat(temp_path, name);

    strcpy(temp->file_path, temp_path);

    return temp;
}

void destroy_logger(logger_info *logger){
    free(logger);
}

void write_message(logger_info logger, const char* msg){
    return;
}

#endif