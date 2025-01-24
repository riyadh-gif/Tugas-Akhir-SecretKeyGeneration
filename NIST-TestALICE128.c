#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include "include/externs.h"
#include "include/utilities.h"
#include "include/cephes.h"

#include <errno.h>
#include "csvparser.h"

double cephes_igamc(double a, double x);
double cephes_igam(double a, double x);
double cephes_lgam(double x);
double cephes_polevl(double x, double *coef, int N);
double cephes_p1evl(double x, double *coef, int N);
double cephes_erfc(double x);


static const double	rel_error = 1E-12;

double MACHEP = 1.11022302462515654042E-16;
double MAXLOG = 7.09782712893383996732224E2;
double MAXNUM = 1.7976931348623158E308;
double PI     = 3.14159265358979323846;

static double big = 4.503599627370496e15;
static double biginv =  2.22044604925031308085e-16;

static unsigned short A[] = {
	0x6661,0x2733,0x9850,0x3f4a,
	0xe943,0xb580,0x7fbd,0xbf43,
	0x5ebb,0x20dc,0x019f,0x3f4a,
	0xa5a1,0x16b0,0xc16c,0xbf66,
	0x554b,0x5555,0x5555,0x3fb5
};
static unsigned short B[] = {
	0x6761,0x8ff3,0x8901,0xc095,
	0xb93e,0x355b,0xf234,0xc0e2,
	0x89e5,0xf890,0x3d73,0xc114,
	0xdb51,0xf994,0xbc82,0xc131,
	0xf20b,0x0219,0x4589,0xc13a,
	0x055e,0x5418,0x0c67,0xc12a
};
static unsigned short C[] = {
	/*0x0000,0x0000,0x0000,0x3ff0,*/
	0x12b2,0x1cf3,0xfd0d,0xc075,
	0xd757,0x7b89,0xaa0d,0xc0d0,
	0x4c9b,0xb974,0xeb84,0xc10a,
	0x0043,0x7195,0x6286,0xc131,
	0xf34c,0x892f,0x5255,0xc143,
	0xe14a,0x6a11,0xce4b,0xc13e
};



int sgngam = 0;
#define MAXLGM 2.556348e305

main()
{

	int				i, j, k, r, blockSize, seqLength, powLen, index, blockSum,S, sup, inf, z, zrev;
	double			sum, numOfBlocks, ApEn[2], apen, chi_squared, p_value,pi,v,sum1, sum2, V, erfc_arg;
	unsigned int	*P;
	double	f, s_obs, sqrt2 = 1.41421356237309504880;
	double sum3,sum4,sum5,sum6,sum7,sum8,sum9,sum10,sum11,sum12,sum13,sum14,sum15,sum16,sum17,sum18,sum19,sum20;
	double f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20;
	double s_obs1,s_obs2,s_obs3,s_obs4,s_obs5,s_obs6,s_obs7,s_obs8,s_obs9,s_obs10,s_obs11,s_obs12,s_obs13,s_obs14,s_obs15,s_obs16,s_obs17,s_obs18,s_obs19,s_obs20;


	int epsilon[128];
	int m=3;
	int n=128;
	int N;
	int M=3;

	seqLength = n;
	r = 0;


	// ========================================================================================================================
	int caca[12800],epsilonlen[12800],maks,abc,isieps,totali,c,d,jj,indeks[10];
    //                                   file, delimiter, first_line_is_header?

    CsvParser *csvparser = CsvParser_new("E:\\PENS\\Semester 7\\Progress PA\\codingan\\Program\\univhash_Alice_doss1.csv", ",", 0);
    CsvRow *row;
    i=0;
    while ((row = CsvParser_getRow(csvparser)) ) {
	    const char **rowFields = CsvParser_getFields(row);
		//printf("epsilon %d: %s\n", i,rowFields[0]);
		epsilonlen[i]=rowFields[0];
		caca[i]=atoi(epsilonlen[i]);
	    CsvParser_destroy_row(row);
	    i++;
    }
    totali=i;
    //CsvParser_destroy(csvparser);
    // ========================================================================================================================
	float ppp[10],pvalapen[10],pvalfreq[10],pvalblockfreq[10],pvalcusumf[10],pvalcusumr[10],pvalruns[10],pvallongruns[10],swap,maksapen;
    maks=totali/128;
    //printf("coba print %d, len = %d\n",maks,totali);

    for(abc=0;abc<maks;abc++){
    	printf("=========== KUNCI KE %d ===========\n",abc+1);
		for(isieps=0;isieps<128;isieps++){
			epsilon[isieps]=caca[isieps+(abc*128)];
			//printf("epsilon=%d, epsilonlen=%d\n",isieps,(isieps+(abc*128)));
			//printf("epsilon-%d %d: %d\n", abc+1,isieps,epsilon[isieps]);
		}
		/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
		                A P P R O X I M A T E  E N T R O P Y   T E S T
		 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

			printf("APPROXIMATE ENTROPY TEST [%d]\t\t",abc+1);
		//	printf( "\t\t--------------------------------------------\n");
		//	printf( "\t\tCOMPUTATIONAL INFORMATION:\n");
		//	printf( "\t\t--------------------------------------------\n");
		//	printf( "\t\t(a) m (block length)    = %d\n", m);

			seqLength = n;
			r = 0;

			for ( blockSize=m; blockSize<=m+1; blockSize++ ) {
				if ( blockSize == 0 ) {
					ApEn[0] = 0.00;
					r++;
				}
				else {
					numOfBlocks = (double)seqLength;
					powLen = (int)pow(2, blockSize+1)-1;
					if ( (P = (unsigned int*)calloc(powLen,sizeof(unsigned int)))== NULL ) {
						printf( "ApEn:  Insufficient memory available.\n");
						return;
					}
					for ( i=1; i<powLen-1; i++ )
						P[i] = 0;
					for ( i=0; i<numOfBlocks; i++ ) { /* COMPUTE FREQUENCY */
						k = 1;
						for ( j=0; j<blockSize; j++ ) {
							k <<= 1;
							if ( epsilon[(i+j) % seqLength] == 1 )
								k++;
						}
						P[k-1]++;
					}
					/* DISPLAY FREQUENCY */
					sum = 0.0;
					index = (int)pow(2, blockSize)-1;
					for ( i=0; i<(int)pow(2, blockSize); i++ ) {
						if ( P[index] > 0 )
							sum += P[index]*log(P[index]/numOfBlocks);
						index++;
					}
					sum /= numOfBlocks;
					ApEn[r] = sum;
					r++;
					free(P);
				}
			}
			apen = ApEn[0] - ApEn[1];

			chi_squared = 2.0*seqLength*(log(2) - apen);
			p_value = cephes_igamc(pow(2, m-1), chi_squared/2.0);

		//	printf( "\t\t(b) n (sequence length) = %d\n", seqLength);
		//	printf( "\t\t(c) Chi^2               = %f\n", chi_squared);
		//	printf( "\t\t(d) Phi(m)	       = %f\n", ApEn[0]);
		//	printf( "\t\t(e) Phi(m+1)	       = %f\n", ApEn[1]);
		//	printf( "\t\t(f) ApEn                = %f\n", apen);
		//	printf( "\t\t(g) Log(2)              = %f\n", log(2.0));
		//	printf( "\t\t--------------------------------------------\n");

			if ( m > (int)(log(seqLength)/log(2)-5) ) {
				printf( "\t\tNote: The blockSize = %d exceeds recommended value of %d\n", m,
					MAX(1, (int)(log(seqLength)/log(2)-5)));
				printf( "\t\tResults are inaccurate!\n");
				printf( "\t\t--------------------------------------------\n");
			}

		//	printf("nilai apen %f\n",ApEn[0]);
		//    printf("nilai apen %f\n",ApEn[1]);
		//	printf("nilai apen %f\n",apen);
			printf("= %f\n",p_value);
			//printf( "--------------------------------------------\n\n");
			pvalapen[abc]=p_value;

		/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
		                          F R E Q U E N C Y  T E S T
		 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
		sum1	=	0.0;

			for ( i=0; i<n; i++ )
				sum1 += 2*(int)epsilon[i]-1;
			s_obs = fabs(sum1)/sqrt(n);
			f = s_obs/sqrt2;
			p_value = erfc(f);

			printf( "FREQUENCY TEST [%d]\t\t\t",(abc+1));
		//	printf( "\t\t---------------------------------------------\n");
		//	printf( "\t\tCOMPUTATIONAL INFORMATION:\n");
		//	printf( "\t\t---------------------------------------------\n");
		//	printf( "\t\t(a) The nth partial sum = %d\n", (int)sum1);
		//	printf( "\t\t(b) S_n/n               = %f\n", sum1/n);
		//	printf( "\t\t(b) F               = %f\n", f);
		//	printf( "\t\t---------------------------------------------\n");

			printf( "= %f\n", p_value );
			//printf( "---------------------------------------------\n\n");
			pvalfreq[abc]=p_value;

		/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
		                    B L O C K  F R E Q U E N C Y  T E S T
		 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

		N = n/M; 		/* # OF SUBSTRING BLOCKS      */
			sum = 0.0;

			for ( i=0; i<N; i++ ) {
				blockSum = 0;
				for ( j=0; j<M; j++ )
					blockSum += epsilon[j+i*M];
				pi = (double)blockSum/(double)M;
				v = pi - 0.5;
				sum += v*v;
			}
			chi_squared = 4.0 * M * sum;
			p_value = cephes_igamc(N/2.0, chi_squared/2.0);

			printf("BLOCK FREQUENCY TEST [%d]\t\t",(abc+1));
		//	printf("\t\t---------------------------------------------\n");
		//	printf("\t\tCOMPUTATIONAL INFORMATION:\n");
		//	printf("\t\t---------------------------------------------\n");
		//	printf("\t\t(a) Chi^2           = %f\n", chi_squared);
		//	printf("\t\t(b) # of substrings = %d\n", N);
		//	printf("\t\t(c) block length    = %d\n", M);
		//	printf("\t\t(d) Note: %d bits were discarded.\n", n % M);
		//	printf("\t\t---------------------------------------------\n");

			printf("= %f\n", p_value);
			//printf("---------------------------------------------\n\n");
			pvalblockfreq[abc]=p_value;

		/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
		                  C U M U L A T I V E   S U M S   T E S T
		 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

			S = 0;
			sup = 0;
			inf = 0;
			for ( k=0; k<n; k++ ) {
				epsilon[k] ? S++ : S--;
				if ( S > sup )
					sup++;
				if ( S < inf )
					inf--;
				z = (sup > -inf) ? sup : -inf;
				zrev = (sup-S > S-inf) ? sup-S : S-inf;
			}

			// forward
			sum1 = 0.0;
			for ( k=(-n/z+1)/4; k<=(n/z-1)/4; k++ ) {
				sum1 += cephes_normal(((4*k+1)*z)/sqrt(n));
				sum1 -= cephes_normal(((4*k-1)*z)/sqrt(n));
			}
			sum2 = 0.0;
			for ( k=(-n/z-3)/4; k<=(n/z-1)/4; k++ ) {
				sum2 += cephes_normal(((4*k+3)*z)/sqrt(n));
				sum2 -= cephes_normal(((4*k+1)*z)/sqrt(n));
			}

			p_value = 1.0 - sum1 + sum2;
		    printf("CUMULATIVE SUMS (FORWARD) TEST [%d]\t",(abc+1));
		//	printf("\t\t-------------------------------------------\n");
		//	printf("\t\tCOMPUTATIONAL INFORMATION:\n");
		//	printf("\t\t-------------------------------------------\n");
		//	printf("\t\t(a) The maximum partial sum = %d\n", z);
		//	printf("\t\t-------------------------------------------\n");

			//if ( isNegative(p_value) || isGreaterThanOne(p_value) )
				//printf("\t\tWARNING:  P_VALUE IS OUT OF RANGE\n");

			printf("= %f\n", p_value);
			pvalcusumf[abc]=p_value;
		//	printf("-------------------------------------------\n\n");
			//printf(results[TEST_CUSUM], "%f\n", p_value);

			// backwards
			sum1 = 0.0;
			for ( k=(-n/zrev+1)/4; k<=(n/zrev-1)/4; k++ ) {
				sum1 += cephes_normal(((4*k+1)*zrev)/sqrt(n));
				sum1 -= cephes_normal(((4*k-1)*zrev)/sqrt(n));
			}
			sum2 = 0.0;
			for ( k=(-n/zrev-3)/4; k<=(n/zrev-1)/4; k++ ) {
				sum2 += cephes_normal(((4*k+3)*zrev)/sqrt(n));
				sum2 -= cephes_normal(((4*k+1)*zrev)/sqrt(n));
			}
			p_value = 1.0 - sum1 + sum2;

			printf("CUMULATIVE SUMS (REVERSE) TEST [%d]\t",(abc+1));
		//	printf("\t\t-------------------------------------------\n");
		//	printf("\t\tCOMPUTATIONAL INFORMATION:\n");
		//	printf("\t\t-------------------------------------------\n");
		//	printf("\t\t(a) The maximum partial sum = %d\n", zrev);
		//	printf("\t\t-------------------------------------------\n");

			//if ( isNegative(p_value) || isGreaterThanOne(p_value) )
				//printf("\t\tWARNING:  P_VALUE IS OUT OF RANGE\n");

			printf("= %f\n", p_value);
			//printf("-------------------------------------------\n\n");
			pvalcusumr[abc]=p_value;

		/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
		                            R U N S   T E S T
		 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
			S = 0;
			for ( k=0; k<n; k++ )
				if ( epsilon[k] )
					S++;
			pi = (double)S / (double)n;

			if ( fabs(pi - 0.5) > (2.0 / sqrt(n)) ) {
				printf("\t\t\t\tRUNS TEST %d\n",(abc+1));
				printf("\t\t------------------------------------------\n");
				printf("\t\tPI ESTIMATOR CRITERIA NOT MET! PI = %f\n", pi);
				p_value = 0.0;
			}
			else {

				V = 1;
				for ( k=1; k<n; k++ )
					if ( epsilon[k] != epsilon[k-1] )
						V++;

				erfc_arg = fabs(V - 2.0 * n * pi * (1-pi)) / (2.0 * pi * (1-pi) * sqrt(2*n));
				p_value = erfc(erfc_arg);

				printf("RUNS TEST [%d]\t\t\t\t",abc+1);
		//		printf("\t\t------------------------------------------\n");
		//		printf("\t\tCOMPUTATIONAL INFORMATION:\n");
		//		printf("\t\t------------------------------------------\n");
		//		printf("\t\t(a) Pi                        = %f\n", pi);
		//		printf("\t\t(b) V_n_obs (Total # of runs) = %d\n", (int)V);
		//		printf("\t\t(c) V_n_obs - 2 n pi (1-pi)\n");
		//		printf("\t\t    -----------------------   = %f\n", erfc_arg);
		//		printf("\t\t      2 sqrt(2n) pi (1-pi)\n");
		//		printf("\t\t------------------------------------------\n");
				//if ( isNegative(p_value) || isGreaterThanOne(p_value) )
					//printf("WARNING:  P_VALUE IS OUT OF RANGE.\n");


			}
		    printf("= %f\n", p_value);
		    //printf("------------------------------------------\n\n");
		    pvalruns[abc]=p_value;

		    /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
		                      L O N G E S T   R U N S   T E S T
		 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

		    double			pval, chi2, pii[7];
			int				run, v_n_obs, K, Vi[7];
			unsigned int	nu[7] = { 0, 0, 0, 0, 0, 0, 0 };

			if ( n < 128 ) {
				printf("longest runs to short");
			}
			if ( n < 6272 ) {
				K = 3;
				M = 8;
				Vi[0] = 1; Vi[1] = 2; Vi[2] = 3; Vi[3] = 4;
				pii[0] = 0.21484375;
				pii[1] = 0.3671875;
				pii[2] = 0.23046875;
				pii[3] = 0.1875;
		//		printf("n < 6272\n");
			}
			else if ( n < 750000 ) {
				K = 5;
				M = 128;
				Vi[0] = 4; Vi[1] = 5; Vi[2] = 6; Vi[3] = 7; Vi[4] = 8; Vi[5] = 9;
				pii[0] = 0.1174035788;
				pii[1] = 0.242955959;
				pii[2] = 0.249363483;
				pii[3] = 0.17517706;
				pii[4] = 0.102701071;
				pii[5] = 0.112398847;
				printf("n < 750000\n");
			}
			else {
				K = 6;
				M = 10000;
					Vi[0] = 10; Vi[1] = 11; Vi[2] = 12; Vi[3] = 13; Vi[4] = 14; Vi[5] = 15; Vi[6] = 16;
				pii[0] = 0.0882;
				pii[1] = 0.2092;
				pii[2] = 0.2483;
				pii[3] = 0.1933;
				pii[4] = 0.1208;
				pii[5] = 0.0675;
				pii[6] = 0.0727;
				printf("n > 750000");
			}

			N = n/M;
			for ( i=0; i<N; i++ ) {
				v_n_obs = 0;
				run = 0;
				for ( j=0; j<M; j++ ) {
					if ( epsilon[i*M+j] == 1 ) {
						run++;
						if ( run > v_n_obs )
							v_n_obs = run;
					}

					else
						run = 0;
				}
				if ( v_n_obs < Vi[0] )
					nu[0]++;
				for ( j=0; j<=K; j++ ) {
					if ( v_n_obs == Vi[j] )
						nu[j]++;
				}
				if ( v_n_obs > Vi[K] )
					nu[K]++;
			}

			chi2 = 0.0;
			for ( i=0; i<=K; i++ )
		    {
		        chi2 += ((nu[i] - N * pii[i]) * (nu[i] - N * pii[i])) / (N * pii[i]);
		//        printf("nilai %f\n",chi2);
		    }


			pval = cephes_igamc((double)(K/2.0), chi2 / 2.0);


		    printf( "LONGEST RUNS OF ONES TEST [%d]\t\t",(abc+1));
		//	printf( "\t\t---------------------------------------------\n");
		//	printf( "\t\tCOMPUTATIONAL INFORMATION:\n");
		//	printf( "\t\t---------------------------------------------\n");
		//	printf( "\t\t(a) N (# of substrings)  = %d\n", N);
		//	printf( "\t\t(b) M (Substring Length) = %d\n", M);
		//	printf( "\t\t(c) Chi^2                = %f\n", chi2);
		//	printf( "\t\t---------------------------------------------\n");
		//	printf( "\t\t      F R E Q U E N C Y\n");
		//	printf( "\t\t---------------------------------------------\n");

		//	if ( K == 3 ) {
		//		printf( "\t\t  <=1     2     3    >=4   P-value  Assignment");
		//		printf( "\n\t\t %3d %3d %3d  %3d ", nu[0], nu[1], nu[2], nu[3]);
		//	}
		//	else if ( K == 5 ) {
		//		printf( "\t\t<=4  5  6  7  8  >=9 P-value  Assignment");
		//		printf( "\n\t\t %3d %3d %3d %3d %3d  %3d ", nu[0], nu[1], nu[2],
		//				nu[3], nu[4], nu[5]);
		//	}
		//	else {
		//		printf("\t\t<=10  11  12  13  14  15 >=16 P-value  Assignment");
		//		printf("\n\t\t %3d %3d %3d %3d %3d %3d  %3d ", nu[0], nu[1], nu[2],
		//				nu[3], nu[4], nu[5], nu[6]);
		//	}


			printf("= %f\n", pval);
			pvallongruns[abc]=pval;
			printf( "---------------------------------------------\n\n");

		}
		/*for(i=0;i<abc;i++){
			printf("pvalapen-%d=%f\n",i+1,pvalapen[i]);
			printf("pvalfreq-%d=%f\n",i+1,pvalfreq[i]);
			printf("pvalblockfreq-%d=%f\n",i+1,pvalblockfreq[i]);
			printf("pvalcusumf-%d=%f\n",i+1,pvalcusumf[i]);
			printf("pvalcusumr-%d=%f\n",i+1,pvalcusumr[i]);
			printf("pvalruns-%d=%f\n",i+1,pvalruns[i]);
			printf("pvallongruns-%d=%f\n",i+1,pvallongruns[i]);
			printf("\n");
		}
		*/
		for (jj=0;jj<abc;jj++){
			ppp[jj]=pvalapen[jj];
		}
		printf("Before Sorting list in descending order:\n");
		for ( c = 0 ; c < abc ; c++ )
		    printf("%f\n", ppp[c]);

		for (j=0 ; j<(abc-1) ; j++)
		{
			for (i=0 ; i<(abc-1) ; i++)
			{
				if (pvalapen[i+1] > pvalapen[i])
				{
					swap = pvalapen[i];
					pvalapen[i] = pvalapen[i + 1];
					pvalapen[i + 1] = swap;
				}
			}
		}

		printf("\nSorted list in descending order:\n");
		for ( c = 0 ; c < abc ; c++ )
		    printf("%f\n", pvalapen[c]);
		maksapen=pvalapen[0];
		for(i=0;i<abc;i++){
			for(j=0;j<abc;j++){
				if(pvalapen[i]==ppp[j]){
					indeks[i]=j;
				}
			}
		}
		printf("\nIndex of Sorted list in descending order:\n");
		for ( c = 0 ; c < abc ; c++ )
		    printf("Prioritas ke %d yaitu Kunci ke %d\n", c+1,indeks[c]+1);

		char str[]="sudahujinist_Alice";
		create_marks_csv(str,indeks,abc);
		getchar();
	}
void create_marks_csv(char *filename, int index[10],int m){
	filename=strcat(filename,".csv");
	//printf("\n Creating file");
	FILE *fp;
	int i,j;
	fp=fopen(filename,"w+");
	for(i=0;i<m;i++)
	    fprintf(fp,"%d\n",index[i]);
	fclose(fp);
	printf("\n %s file created",filename);

}

double cephes_igamc(double a, double x)
{
	double ans, ax, c, yc, r, t, y, z;
	double pk, pkm1, pkm2, qk, qkm1, qkm2;

	if ( (x <= 0) || ( a <= 0) )
		return( 1.0 );

	if ( (x < 1.0) || (x < a) )
		return( 1.e0 - cephes_igam(a,x) );

	ax = a * log(x) - x - cephes_lgam(a);

	if ( ax < -MAXLOG ) {
		printf("igamc: UNDERFLOW\n");
		return 0.0;
	}
	ax = exp(ax);

	/* continued fraction */
	y = 1.0 - a;
	z = x + y + 1.0;
	c = 0.0;
	pkm2 = 1.0;
	qkm2 = x;
	pkm1 = x + 1.0;
	qkm1 = z * x;
	ans = pkm1/qkm1;

	do {
		c += 1.0;
		y += 1.0;
		z += 2.0;
		yc = y * c;
		pk = pkm1 * z  -  pkm2 * yc;
		qk = qkm1 * z  -  qkm2 * yc;
		if ( qk != 0 ) {
			r = pk/qk;
			t = fabs( (ans - r)/r );
			ans = r;
		}
		else
			t = 1.0;
		pkm2 = pkm1;
		pkm1 = pk;
		qkm2 = qkm1;
		qkm1 = qk;
		if ( fabs(pk) > big ) {
			pkm2 *= biginv;
			pkm1 *= biginv;
			qkm2 *= biginv;
			qkm1 *= biginv;
		}
	} while ( t > MACHEP );

	return ans*ax;
}

double cephes_igam(double a, double x)
{
	double ans, ax, c, r;

	if ( (x <= 0) || ( a <= 0) )
		return 0.0;

	if ( (x > 1.0) && (x > a ) )
		return 1.e0 - cephes_igamc(a,x);

	/* Compute  x**a * exp(-x) / gamma(a)  */
	ax = a * log(x) - x - cephes_lgam(a);
	if ( ax < -MAXLOG ) {
		printf("igam: UNDERFLOW\n");
		return 0.0;
	}
	ax = exp(ax);

	/* power series */
	r = a;
	c = 1.0;
	ans = 1.0;

	do {
		r += 1.0;
		c *= x/r;
		ans += c;
	} while ( c/ans > MACHEP );

	return ans * ax/a;
}


/* Logarithm of gamma function */
double cephes_lgam(double x)
{
	double	p, q, u, w, z;
	int		i;

	sgngam = 1;

	if ( x < -34.0 ) {
		q = -x;
		w = cephes_lgam(q); /* note this modifies sgngam! */
		p = floor(q);
		if ( p == q ) {
lgsing:
			goto loverf;
		}
		i = (int)p;
		if ( (i & 1) == 0 )
			sgngam = -1;
		else
			sgngam = 1;
		z = q - p;
		if ( z > 0.5 ) {
			p += 1.0;
			z = p - q;
		}
		z = q * sin( PI * z );
		if ( z == 0.0 )
			goto lgsing;
		/*      z = log(PI) - log( z ) - w;*/
		z = log(PI) - log( z ) - w;
		return z;
	}

	if ( x < 13.0 ) {
		z = 1.0;
		p = 0.0;
		u = x;
		while ( u >= 3.0 ) {
			p -= 1.0;
			u = x + p;
			z *= u;
		}
		while ( u < 2.0 ) {
			if ( u == 0.0 )
				goto lgsing;
			z /= u;
			p += 1.0;
			u = x + p;
		}
		if ( z < 0.0 ) {
			sgngam = -1;
			z = -z;
		}
		else
			sgngam = 1;
		if ( u == 2.0 )
			return( log(z) );
		p -= 2.0;
		x = x + p;
		p = x * cephes_polevl( x, (double *)B, 5 ) / cephes_p1evl( x, (double *)C, 6);

		return log(z) + p;
	}

	if ( x > MAXLGM ) {
loverf:
		printf("lgam: OVERFLOW\n");

		return sgngam * MAXNUM;
	}

	q = ( x - 0.5 ) * log(x) - x + log( sqrt( 2*PI ) );
	if ( x > 1.0e8 )
		return q;

	p = 1.0/(x*x);
	if ( x >= 1000.0 )
		q += ((   7.9365079365079365079365e-4 * p
		        - 2.7777777777777777777778e-3) *p
				+ 0.0833333333333333333333) / x;
	else
		q += cephes_polevl( p, (double *)A, 4 ) / x;

	return q;
}

double cephes_polevl(double x, double *coef, int N)
{
	double	ans;
	int		i;
	double	*p;

	p = coef;
	ans = *p++;
	i = N;

	do
		ans = ans * x  +  *p++;
	while ( --i );

	return ans;
}

double cephes_p1evl(double x, double *coef, int N)
{
	double	ans;
	double	*p;
	int		i;

	p = coef;
	ans = x + *p++;
	i = N-1;

	do
		ans = ans * x  + *p++;
	while ( --i );

	return ans;
}

double cephes_erf(double x)
{
	static const double two_sqrtpi = 1.128379167095512574;
	double	sum = x, term = x, xsqr = x * x;
	int		j = 1;

	if ( fabs(x) > 2.2 )
		return 1.0 - cephes_erfc(x);

	do {
		term *= xsqr/j;
		sum -= term/(2*j+1);
		j++;
		term *= xsqr/j;
		sum += term/(2*j+1);
		j++;
	} while ( fabs(term)/sum > rel_error );

	return two_sqrtpi*sum;
}

double cephes_erfc(double x)
{
	static const double one_sqrtpi = 0.564189583547756287;
	double	a = 1, b = x, c = x, d = x*x + 0.5;
	double	q1, q2 = b/d, n = 1.0, t;

	if ( fabs(x) < 2.2 )
		return 1.0 - cephes_erf(x);
	if ( x < 0 )
		return 2.0 - cephes_erfc(-x);

	do {
		t = a*n + b*x;
		a = b;
		b = t;
		t = c*n + d*x;
		c = d;
		d = t;
		n += 0.5;
		q1 = q2;
		q2 = b/d;
	} while ( fabs(q1-q2)/q2 > rel_error );

	return one_sqrtpi*exp(-x*x)*q2;
}


double cephes_normal(double x)
{
	double arg, result, sqrt2=1.414213562373095048801688724209698078569672;

	if (x > 0) {
		arg = x/sqrt2;
		result = 0.5 * ( 1 + erf(arg) );
	}
	else {
		arg = -x/sqrt2;
		result = 0.5 * ( 1 - erf(arg) );
	}

	return( result);
}

//=========================================================== PROGRAM AMBIL DATA CSV ======================================================================
#ifdef __cplusplus
extern "C" {
#endif

CsvParser *CsvParser_new(const char *filePath, const char *delimiter, int firstLineIsHeader) {
    CsvParser *csvParser = (CsvParser*)malloc(sizeof(CsvParser));
    if (filePath == NULL) {
        csvParser->filePath_ = NULL;
    } else {
        int filePathLen = strlen(filePath);
        csvParser->filePath_ = (char*)malloc((filePathLen + 1));
        strcpy(csvParser->filePath_, filePath);
    }
    csvParser->firstLineIsHeader_ = firstLineIsHeader;
    csvParser->errMsg_ = NULL;
    if (delimiter == NULL) {
        csvParser->delimiter_ = ',';
    } else if (_CsvParser_delimiterIsAccepted(delimiter)) {
        csvParser->delimiter_ = *delimiter;
    } else {
        csvParser->delimiter_ = '\0';
    }
    csvParser->header_ = NULL;
    csvParser->fileHandler_ = NULL;
	csvParser->fromString_ = 0;
	csvParser->csvString_ = NULL;
	csvParser->csvStringIter_ = 0;

    return csvParser;
}

CsvParser *CsvParser_new_from_string(const char *csvString, const char *delimiter, int firstLineIsHeader) {
	CsvParser *csvParser = CsvParser_new(NULL, delimiter, firstLineIsHeader);
	csvParser->fromString_ = 1;
	if (csvString != NULL) {
		int csvStringLen = strlen(csvString);
		csvParser->csvString_ = (char*)malloc(csvStringLen + 1);
		strcpy(csvParser->csvString_, csvString);
	}
	return csvParser;
}

void CsvParser_destroy(CsvParser *csvParser) {
    if (csvParser == NULL) {
        return;
    }
    if (csvParser->filePath_ != NULL) {
        free(csvParser->filePath_);
    }
    if (csvParser->errMsg_ != NULL) {
        free(csvParser->errMsg_);
    }
    if (csvParser->fileHandler_ != NULL) {
        fclose(csvParser->fileHandler_);
    }
    if (csvParser->header_ != NULL) {
        CsvParser_destroy_row(csvParser->header_);
    }
	if (csvParser->csvString_ != NULL) {
		free(csvParser->csvString_);
	}
    free(csvParser);
}

void CsvParser_destroy_row(CsvRow *csvRow) {
    int i;
    for (i = 0 ; i < csvRow->numOfFields_ ; i++) {
        free(csvRow->fields_[i]);
    }
	free(csvRow->fields_);
    free(csvRow);
}

const CsvRow *CsvParser_getHeader(CsvParser *csvParser) {
    if (! csvParser->firstLineIsHeader_) {
        _CsvParser_setErrorMessage(csvParser, "Cannot supply header, as current CsvParser object does not support header");
        return NULL;
    }
    if (csvParser->header_ == NULL) {
        csvParser->header_ = _CsvParser_getRow(csvParser);
    }
    return csvParser->header_;
}

CsvRow *CsvParser_getRow(CsvParser *csvParser) {
    if (csvParser->firstLineIsHeader_ && csvParser->header_ == NULL) {
        csvParser->header_ = _CsvParser_getRow(csvParser);
    }
    return _CsvParser_getRow(csvParser);
}

int CsvParser_getNumFields(const CsvRow *csvRow) {
    return csvRow->numOfFields_;
}

const char **CsvParser_getFields(const CsvRow *csvRow) {
    return (const char**)csvRow->fields_;
}

CsvRow *_CsvParser_getRow(CsvParser *csvParser) {
    int numRowRealloc = 0;
    int acceptedFields = 64;
    int acceptedCharsInField = 64;
    if (csvParser->filePath_ == NULL && (! csvParser->fromString_)) {
        _CsvParser_setErrorMessage(csvParser, "Supplied CSV file path is NULL");
        return NULL;
    }
    if (csvParser->csvString_ == NULL && csvParser->fromString_) {
        _CsvParser_setErrorMessage(csvParser, "Supplied CSV string is NULL");
        return NULL;
    }
    if (csvParser->delimiter_ == '\0') {
        _CsvParser_setErrorMessage(csvParser, "Supplied delimiter is not supported");
        return NULL;
    }
    if (! csvParser->fromString_) {
        if (csvParser->fileHandler_ == NULL) {
            csvParser->fileHandler_ = fopen(csvParser->filePath_, "r");
            if (csvParser->fileHandler_ == NULL) {
                int errorNum = errno;
                const char *errStr = strerror(errorNum);
                char *errMsg = (char*)malloc(1024 + strlen(errStr));
                strcpy(errMsg, "");
                sprintf(errMsg, "Error opening CSV file for reading: %s : %s", csvParser->filePath_, errStr);
                _CsvParser_setErrorMessage(csvParser, errMsg);
                free(errMsg);
                return NULL;
            }
        }
    }
    CsvRow *csvRow = (CsvRow*)malloc(sizeof(CsvRow));
    csvRow->fields_ = (char**)malloc(acceptedFields * sizeof(char*));
    csvRow->numOfFields_ = 0;
    int fieldIter = 0;
    char *currField = (char*)malloc(acceptedCharsInField);
    int inside_complex_field = 0;
    int currFieldCharIter = 0;
    int seriesOfQuotesLength = 0;
    int lastCharIsQuote = 0;
    int isEndOfFile = 0;
    while (1) {
        char currChar = (csvParser->fromString_) ? csvParser->csvString_[csvParser->csvStringIter_] : fgetc(csvParser->fileHandler_);
        csvParser->csvStringIter_++;
        int endOfFileIndicator;
        if (csvParser->fromString_) {
            endOfFileIndicator = (currChar == '\0');
        } else {
            endOfFileIndicator = feof(csvParser->fileHandler_);
        }
        if (endOfFileIndicator) {
            if (currFieldCharIter == 0 && fieldIter == 0) {
                _CsvParser_setErrorMessage(csvParser, "Reached EOF");
				free(currField);
				CsvParser_destroy_row(csvRow);
                return NULL;
            }
            currChar = '\n';
            isEndOfFile = 1;
        }
        if (currChar == '\r') {
            continue;
        }
        if (currFieldCharIter == 0  && ! lastCharIsQuote) {
            if (currChar == '\"') {
                inside_complex_field = 1;
                lastCharIsQuote = 1;
                continue;
            }
        } else if (currChar == '\"') {
            seriesOfQuotesLength++;
            inside_complex_field = (seriesOfQuotesLength % 2 == 0);
            if (inside_complex_field) {
                currFieldCharIter--;
            }
        } else {
            seriesOfQuotesLength = 0;
        }
        if (isEndOfFile || ((currChar == csvParser->delimiter_ || currChar == '\n') && ! inside_complex_field) ){
            currField[lastCharIsQuote ? currFieldCharIter - 1 : currFieldCharIter] = '\0';
            csvRow->fields_[fieldIter] = (char*)malloc(currFieldCharIter + 1);
            strcpy(csvRow->fields_[fieldIter], currField);
            free(currField);
            csvRow->numOfFields_++;
            if (currChar == '\n') {
                return csvRow;
            }
            if (csvRow->numOfFields_ != 0 && csvRow->numOfFields_ % acceptedFields == 0) {
                csvRow->fields_ = (char**)realloc(csvRow->fields_, ((numRowRealloc + 2) * acceptedFields) * sizeof(char*));
                numRowRealloc++;
            }
            acceptedCharsInField = 64;
            currField = (char*)malloc(acceptedCharsInField);
            currFieldCharIter = 0;
            fieldIter++;
            inside_complex_field = 0;
        } else {
            currField[currFieldCharIter] = currChar;
            currFieldCharIter++;
            if (currFieldCharIter == acceptedCharsInField - 1) {
                acceptedCharsInField *= 2;
                currField = (char*)realloc(currField, acceptedCharsInField);
            }
        }
        lastCharIsQuote = (currChar == '\"') ? 1 : 0;
    }
}

int _CsvParser_delimiterIsAccepted(const char *delimiter) {
    char actualDelimiter = *delimiter;
    if (actualDelimiter == '\n' || actualDelimiter == '\r' || actualDelimiter == '\0' ||
            actualDelimiter == '\"') {
        return 0;
    }
    return 1;
}

void _CsvParser_setErrorMessage(CsvParser *csvParser, const char *errorMessage) {
    if (csvParser->errMsg_ != NULL) {
        free(csvParser->errMsg_);
    }
    int errMsgLen = strlen(errorMessage);
    csvParser->errMsg_ = (char*)malloc(errMsgLen + 1);
    strcpy(csvParser->errMsg_, errorMessage);
}

const char *CsvParser_getErrorMessage(CsvParser *csvParser) {
    return csvParser->errMsg_;
}

#ifdef __cplusplus
}
#endif
