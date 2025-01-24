
#include "../include/defs.h"

/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
                   G L O B A L   D A T A  S T R U C T U R E S
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

extern BitSequence	*epsilon;
extern TP			tp;
extern FILE			*stats[NUMOFTESTS+1];
extern FILE			*results[NUMOFTESTS+1];
extern FILE			*freqfp;
extern FILE			*summary;
extern int			testVector[NUMOFTESTS+1];

extern char	generatorDir[NUMOFGENERATORS][20];
extern char	testNames[NUMOFTESTS+1][32];
