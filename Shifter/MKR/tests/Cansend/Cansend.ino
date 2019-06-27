// demo: CAN-BUS Shield, send data
// loovee@seeed.cc

#include <mcp_can.h>
#include <SPI.h>

// the cs pin of the version after v1.1 is default to D9
// v0.9b and v1.0 is default D10
const int SPI_CS_PIN = 9;

MCP_CAN CAN(SPI_CS_PIN);                                    // Set CS pin

void setup()
{
    Serial.begin(115200);

    while (CAN_OK != CAN.begin(CAN_1000KBPS))              // init can bus : baudrate = 500k
    {
        Serial.println("CAN BUS Shield init fail");
        Serial.println(" Init CAN BUS Shield again");
        delay(100);
    }
    Serial.println("CAN BUS Shield init ok!");
}

uint16_t stmp[8] = {0x5fc, 0x5fd, 0x5fe, 0x600, 0x604, 0x666, 0x66f, 0x555};
const byte msg[8][8] = {{10, 1, 2, 0, 0, 0, 0, 1},
                           {11, 1, 2, 0, 0, 0, 0, 2},
                           {12, 1, 2, 0, 0, 0, 0, 3},
                           {13, 1, 2, 0, 0, 0, 0, 4},
                           {19, 100, 2, 0, 0, 0, 0, 0},
                           {15, 1, 2, 0, 0, 0, 4, 0},
                           {16, 1, 2, 0, 0, 0, 0, 7},
                           {17, 1, 2, 0, 0, 0, 0, 8}};
void loop()
{

   for(int i=0; i<8; i++) {
      CAN.sendMsgBuf(stmp[i], 0, 8, msg[i]);
      delay(100);                       // send data per 100ms
   }
}

// END FILE
