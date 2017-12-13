# BMP格式



* 第一部分是BMP文件头。
	* 前2个字节是“BM”，是用于识别BMP文件的标志；
	* 第3、4、5、6字节存放的是位图文件的大小，以字节为单位；
	* 第7、8、9、10字节是保留的，必须为0；
	* 第11、12、13、14字节给出位图阵列相对于文件头的偏移，在24位真彩色图像中，这个值固定为54；
	* 19，20，21，22表示的是图像文件的宽度，以像素为单位；
	* 23，24，25，26表示的是图像文件的高度，以像素为单位。
* 第二部分是位图信息头。
  * 从第29个字节开始，第29、30字节描述的是像素的位数， 24位真彩色位图。该位的值为0x18<!---->


```c
1：BMP文件组成BMP文件由文件头、位图信息头、颜色信息和图形数据四部分组成。 2：BMP文件头（14字节）BMP文件头数据结构含有BMP文件的类型、文件大小和位图起始位置等信息。其结构定义如下： typedefstructtagBITMAPFILEHEADER{	WORDbfType;//位图文件的类型，必须为BM(1-2字节,0x424d:BM两个ASCII字符）	DWORDbfSize;//位图文件的大小，以字节为单位（3-6字节，低位在前）	WORDbfReserved1;//位图文件保留字，必须为0(7-8字节）	WORDbfReserved2;//位图文件保留字，必须为0(9-10字节）	DWORDbfOffBits;//位图数据的起始位置，以相对于位图（11-14字节，低位在前,一般为54字节:即0x36）	//文件头的偏移量表示，以字节为单位}BITMAPFILEHEADER;  3：位图信息头（40字节）BMP位图信息头数据用于说明位图的尺寸等信息。  typedefstructtagBITMAPINFOHEADER{	DWORDbiSize;//本结构所占用字节数（15-18字节.值为0x28 = 40 Byte）	LONGbiWidth;//位图的宽度，以像素为单位（19-22字节）	LONGbiHeight;//位图的高度，以像素为单位（23-26字节）	WORDbiPlanes;//目标设备的级别，必须为1(27-28字节）	WORDbiBitCount;//每个像素所需的位数，必须是1（双色），（29-30字节）	//4(16色），8(256色）16(高彩色)或24（真彩色）之一	DWORDbiCompression;//位图压缩类型，必须是0（不压缩），（31-34字节）	//1(BI_RLE8压缩类型）或2(BI_RLE4压缩类型）之一	DWORDbiSizeImage;//位图的大小(其中包含了为了补齐行数是4的倍数而添加的空字节)，以字节为单位（35-38字节）	LONGbiXPelsPerMeter;//位图水平分辨率，每米像素数（39-42字节）	LONGbiYPelsPerMeter;//位图垂直分辨率，每米像素数（43-46字节)	DWORDbiClrUsed;//位图实际使用的颜色表中的颜色数（47-50字节）	DWORDbiClrImportant;//位图显示过程中重要的颜色数（51-54字节）}BITMAPINFOHEADER;  4：颜色表 颜色表用于说明位图中的颜色，它有若干个表项，每一个表项是一个RGBQUAD类型的结构，定义一种颜色。RGBQUAD结构的定义如下：  typedefstructtagRGBQUAD{	BYTErgbBlue;//蓝色的亮度（值范围为0-255)	BYTErgbGreen;//绿色的亮度（值范围为0-255)	BYTErgbRed;//红色的亮度（值范围为0-255)	BYTErgbReserved;//保留，必须为0}RGBQUAD;  颜色表中RGBQUAD结构数据的个数有biBitCount来确定：当biBitCount = 1, 4, 8时，分别有2, 16, 256个表项；当biBitCount = 24时，没有颜色表项。位图信息头和颜色表组成位图信息，BITMAPINFO结构定义如下：   typedefstructtagBITMAPINFO{	BITMAPINFOHEADERbmiHeader;//位图信息头	RGBQUADbmiColors[1];//颜色表}BITMAPINFO;  5：位图数据 位图数据记录了位图的每一个像素值，记录顺序是在扫描行内是从左到右，扫描行之间是从下到上。位图的一个像素值所占的字节数： 当biBitCount = 1时，8个像素占1个字节；当biBitCount = 4时，2个像素占1个字节；当biBitCount = 8时，1个像素占1个字节；当biBitCount = 24时，1个像素占3个字节, 按顺序分别为B, G, R；Windows规定一个扫描行所占的字节数必须是4的倍数（即以long为单位），不足的以0填充， biSizeImage = ((((bi.biWidth * bi.biBitCount) + 31) & ~31) / 8) * bi.biHeight;具体数据举例：如某BMP文件开头： 424D 46900000 0000 0000 4600 0000 2800 0000 8000 0000 9000 0000 0100 * 1000 0300 0000 0090 0000 A00F 0000 A00F0000 0000 00000000 0000 * 00F8 E007 1F00 0000 * 02F1 84F1 04F1 84F1 84F1 06F2 84F1 06F2 04F2 86F2 06F2 86F2 86F2 .... ....    读取方法/* 功能：在图片的第50行画一条黑线 为简化代码，只支持24位色的图片 codeblocks下正确运行。VC下需要将二维数组img改为malloc动态分配。需要添加#include "stdlib.h"。 */     #include<stdio.h>#include<windows.h>typedefstruct{	BYTEb;	BYTEg;	BYTEr;}RGB;intmain(void){	BITMAPFILEHEADERfileHeader;	BITMAPINFOHEADERinfoHeader;	FILE*pfin = fopen("原始图像.bmp", "rb");	FILE*pfout = fopen("修改后的图像.bmp", "wb");	//ReadtheBitmapfileheader;	fread(&fileHeader, sizeof(BITMAPFILEHEADER), 1, pfin);	//ReadtheBitmapinfoheader;	fread(&infoHeader, sizeof(BITMAPINFOHEADER), 1, pfin);	//为简化代码，只处理24位彩色	if (infoHeader.biBitCount == 24)	{		intsize = infoHeader.biWidth*infoHeader.biHeight;		RGBimg[infoHeader.biHeight][infoHeader.biWidth];		fread(img, sizeof(RGB), size, pfin);		//把第50行染成黑色		inti = 0;		for (; i<infoHeader.biWidth; i++)		{			img[50][i].b = img[50][i].g = img[50][i].r = 0;		}		//将修改后的图片保存到文件		fwrite(&fileHeader, sizeof(fileHeader), 1, pfout);		fwrite(&infoHeader, sizeof(infoHeader), 1, pfout);		fwrite(img, sizeof(RGB), size, pfout);	}	fclose(pfin);	fclose(pfout);} 

```

