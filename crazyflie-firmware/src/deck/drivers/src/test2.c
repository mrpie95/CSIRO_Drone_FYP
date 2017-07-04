#define DEBUG_MODULE "TESTDECK"
#include <stdint.h>
#include <stdlib.h>
#include "stm32fxxx.h"

#include "log.h"
#include "debug.h"
#include "deck.h"

static float TEST = 1;

static void testInit(DeckInfo *info)
{
	DEBUG_PRINT("THIS IS A TEST PRINT!\n");
	TEST++;
	pinMode(DECK_GPIO_IO1, OUTPUT);
	digitalWrite(DECK_GPIO_IO1, HIGH);


}

static bool testTest(){
	DEBUG_PRINT("TEST PASSED#############################################\n");
	return true;
}

static const DeckDriver test_deck = {
  .vid = 0,
  .pid = 0,
  .name = "test",

  .usedGpio = DECK_USING_IO_1,

  .init = testInit,
  .test = testTest,

};

DECK_DRIVER(test_deck);

//test logigng
LOG_GROUP_START(test)
LOG_ADD(LOG_FLOAT, TESTVARIABLE, &TEST)
LOG_GROUP_STOP(test)
