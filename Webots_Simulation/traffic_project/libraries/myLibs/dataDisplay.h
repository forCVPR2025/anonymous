#pragma once
#include "myMatrices.h"
#include <webots/Display.hpp>
#include "Upper_Public.h"
using namespace webots;
USING_NAMESPACE_MM

#define DATAMAX 100.f	// 锟斤拷锟斤拷锟斤拷锟�
#define ANXISDIVID 3	// 锟斤拷锟斤拷锟结划锟街革拷锟斤拷
#define ANXISCOLOR getcolor(100,100,100)	// 锟斤拷锟斤拷锟斤拷锟斤拷色

/* 锟斤拷锟斤拷模锟斤拷锟洁：锟接达拷锟斤拷锟饺ｏ拷锟竭讹拷 */
template<uint8_t channelNum>
class dataDisplay {
private:
	myMatrices<int>* anxis;			// 锟斤拷锟斤拷系锟斤拷锟斤拷
	myMatrices<int>* currentDisp;	// 锟斤拷前要锟斤拷锟侥撅拷锟斤拷
	myMatrices<int>* lastDisp;		// 锟较次伙拷锟侥撅拷锟斤拷
	myMatrices<uint8_t>* isUpdate;	// 锟角凤拷锟斤拷要锟斤拷锟铰伙拷图
	myMatrices<int>* transfer;		// 转锟狡撅拷锟斤拷
	Display* tag;

	uint16_t width = 0;
	uint16_t height = 0;

	/* 锟斤拷锟矫讹拷应通锟斤拷锟斤拷色 */
	int getcolor(int r, int g, int b)
	{
		return (r << 16 | g << 8 | b);
	}

	/* 锟斤拷值锟斤拷锟斤拷锟斤拷锟疥（锟斤拷锟斤拷锟斤拷转锟斤拷 */
	int num2row(double _num)
	{
		double temp = _num / DATAMAX * height / 2.f;// 锟斤拷锟斤拷锟斤拷锟斤拷莸锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷位锟斤拷
		int std_temp = (int)temp;
		if (temp - std_temp > 0.5)
		{
			std_temp += 1;// 锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟�
		}
		int fact_temp = height / 2 - std_temp - 1;//锟斤拷应锟斤拷锟截碉拷锟轿伙拷锟�
		return upper::constrain(fact_temp, 0, height - 1);
	}

	/* 锟斤拷锟铰伙拷锟斤拷锟斤拷锟斤拷 */
	void currentUpdate(double _data[channelNum])
	{
		*currentDisp = (*currentDisp) * (*transfer);// 锟斤拷锟斤拷锟斤拷锟斤拷一锟斤拷
		for (int i = 0; i < channelNum; i++)
		{
			int _color;
			switch (i)
			{
			case 0: _color = getcolor(255, 0, 0); break;// 绾�
			case 1: _color = getcolor(0, 255, 0); break;// 缁�
			case 2: _color = getcolor(0, 0, 255); break;// 钃�
			case 3: _color = getcolor(0, 255, 255); break;// 钃濈豢锛堜寒钃濓級
			case 4: _color = getcolor(255, 0, 255); break;// 绱壊
			case 5: _color = getcolor(255, 255, 0); break;// 榛勮壊
			default:break;
			}
			currentDisp->setElement(num2row(_data[i]), width - 1, _color);// 锟窖革拷锟铰碉拷锟斤拷色写锟斤拷锟斤拷锟揭伙拷锟斤拷锟斤拷锟斤拷锟�
		}

		// 锟斤拷锟斤拷锟斤拷系锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷
		for (int i = 0; i < height; i++)
		{
			for (int j = 0; j < width; j++)
			{
				int dataPixel = currentDisp->getElement(i, j);
				int anxisPixel = anxis->getElement(i, j);
				if (dataPixel == 0 && anxisPixel == ANXISCOLOR)
				{
					currentDisp->setElement(i, j, ANXISCOLOR);
				}
			}
		}
	}

	/* 锟叫讹拷要锟斤拷锟铰伙拷锟狡的碉拷 */
	void drawingJudge()
	{
		for (int i = 0; i < height; i++)
		{
			for (int j = 0; j < width; j++)
			{
				if (currentDisp->getElement(i, j) != lastDisp->getElement(i, j))
				{
					isUpdate->setElement(i, j, 1);// 锟斤拷锟斤拷要锟斤拷锟侥碉拷锟斤拷锟截点赋值1
				}
				else
				{
					isUpdate->setElement(i, j, 0);
				}
			}
		}
	}

public:
	/* 锟斤拷锟届函锟斤拷 */
	dataDisplay(Display* _tag):tag(_tag){
		static_assert((channelNum > 0) && (channelNum <= 6),
			"display channel number should be in [1,6]");// 锟斤拷锟斤拷通锟斤拷锟斤拷锟斤拷锟角凤拷锟节凤拷围锟斤拷

		width = tag->getWidth();	// 锟斤拷取锟斤拷锟斤拷锟斤拷锟�
		height = tag->getHeight();	// 锟斤拷取锟斤拷锟斤拷叨锟�

		currentDisp = new myMatrices<int>(height, width);
		lastDisp = new myMatrices<int>(height, width);
		isUpdate = new myMatrices<uint8_t>(height, width);
		transfer = new myMatrices<int>(width);
		anxis = new myMatrices<int>(height, width);

		for (int i = 0; i < width -1; i++)
		{
			transfer->setElement(i + 1, i,1); // 锟斤拷锟斤拷应位锟矫革拷1
		}

		// 锟斤拷锟斤拷锟斤拷锟斤拷系锟斤拷锟斤拷
		int anxis_color = ANXISCOLOR;
		for (int i = 0; i < ANXISDIVID; i++)
		{
			for (int j = 0; j < width - 1; j++)
			{
				anxis->setElement(num2row(i * DATAMAX / (double)ANXISDIVID), j, anxis_color);
				anxis->setElement(num2row(-i * DATAMAX / (double)ANXISDIVID), j, anxis_color);
			}
		}
	}
	~dataDisplay()
	{
		// delete currentDisp;
		// delete lastDisp;
		// delete isUpdate;
		// delete transfer;
		// delete anxis;
	}

	/* 锟斤拷锟竭伙拷锟斤拷 */
	void drawPixel()
	{
		for (int i = 0; i < height; i++)
		{
			for (int j = 0; j < width; j++)
			{
				if (isUpdate->getElement(i, j) == 1)
				{
					tag->setColor(currentDisp->getElement(i,j));// 取锟斤拷锟斤拷应锟斤拷色
					tag->drawPixel(j, i);// 锟斤拷锟斤拷
				}
			}
		}
	}

	/* 锟斤拷锟矫猴拷锟斤拷 */
	void sendCtrl(double _data[channelNum])
	{
		currentUpdate(_data);
		drawingJudge();
		drawPixel();
		*lastDisp = *currentDisp;// 锟斤拷锟芥当前锟斤拷锟斤拷状态
	}

};