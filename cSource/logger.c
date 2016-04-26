#include <stdio.h>
#include <stdlib.h>

#include "logger.h"

int main(){
    const char * name = "Name";
    const char * path = "/path/to/log";
    
    logger_info * lg = new_logger(name, path);
    printf(lg->name);
    printf("\n");
    printf(lg->file_path);

    destroy_logger(lg);
    return 0;
}