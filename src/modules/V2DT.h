#ifndef V2DT_H_
#define V2DT_H_

volatile struct to_struct
{
	uint8_t speed1;
	uint8_t speed2;
	uint8_t status;
} to_struct;

volatile struct from_struct
{
	char output[16];
} from_struct;

#endif /* V2DT_H_ */