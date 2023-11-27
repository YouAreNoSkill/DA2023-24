// im c Verzeichnis jedes mal nachdem der neue Code 
// sudo make clean // 
// sudo make -j4 EPD=epd7in5V2
//
//


#include "EPD_Test.h"
#include "EPD_7in5_V2.h"
#include <time.h> 

int EPD_7in5_V2_test(void)
{
    if(DEV_Module_Init()!=0){
        return -1;
    }

    printf("e-Paper Init and Clear...\r\n");
    EPD_7IN5_V2_Init();

    //Clock
    struct timespec start={0,0}, finish={0,0}; 
    clock_gettime(CLOCK_REALTIME,&start);
    EPD_7IN5_V2_Clear();
    clock_gettime(CLOCK_REALTIME,&finish);
    printf("%ld S\r\n",finish.tv_sec-start.tv_sec);
    DEV_Delay_ms(500);
	
    //Image Cache erstellen --> Achtung Heat Pipe
    UBYTE *BlackImage;
    UWORD Imagesize = ((EPD_7IN5_V2_WIDTH % 8 == 0)? (EPD_7IN5_V2_WIDTH / 8 ): (EPD_7IN5_V2_WIDTH / 8 + 1)) * EPD_7IN5_V2_HEIGHT;
    if((BlackImage = (UBYTE *)malloc(Imagesize)) == NULL) {
        printf("Black Memory ERROR\r\n");
        return -1;
    }
    printf("Paint_NewImage\r\n");
    Paint_NewImage(BlackImage, EPD_7IN5_V2_WIDTH, EPD_7IN5_V2_HEIGHT, 0, WHITE);

#if 1  // .bmp Bild anzeigen und loopen
    while (1) {
    printf("BMP Loading\r\n");
    Paint_SelectImage(BlackImage);
    Paint_Clear(WHITE);
    GUI_ReadBmp("./pic/800x480.bmp", 0, 0);
    EPD_7IN5_V2_Display(BlackImage);
    DEV_Delay_ms(10000);
    

    }
#endif        

    printf("Clearing...\r\n");
    EPD_7IN5_V2_Clear();

    printf("Schlafmodus\r\n");
    EPD_7IN5_V2_Sleep();
    free(BlackImage);
    BlackImage = NULL;
    DEV_Delay_ms(2000); //notwendig für sauberen shutdown
    printf("close 5V, Module enters 0 power consumption ...\r\n");
    DEV_Module_Exit();
    
    return 0;
}

