default: baseline tracer1a tracer1b tracer2 tracer3

baseline: baseline.c
	gcc -m32 -g -o baseline baseline.c

tracer1a: tracer1a.c
	gcc -m32 -g -o tracer1a tracer1a.c

tracer1b: tracer1b.c
	gcc -m32 -g -o tracer1b tracer1b.c

tracer2: tracer2.c
	gcc -m32 -g -o tracer2 tracer2.c

tracer3: tracer3.c
	gcc -m32 -g -o tracer3 tracer3.c

clean: 
	rm -f baseline tracer1a tracer1b tracer2 tracer3
