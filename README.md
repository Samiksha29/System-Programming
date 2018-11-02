<h1>Implemented an Assembler for i386 architecture </h1>


<h3>How to run</h3>

<h1>Pass 1 and Pass 2 Assembler</h1>

Method 1)</br>
pucsd -$ python3 symbol_table.py filename         =>display symbol table</br>
pucsd -$ python3 literal_table.py filename	  => display literal table</br>
pucsd -$ python3 intermediate.py filename	  => display Intermediate code</br>
pucsd -$ python3 lst.py filename		  => display lst file code</br>

Method 2)</br>
pucsd -$ python3 main.py filename [options] </br>   

<h3>COMMAND LINE OPTIONS</h3>
	
	-s     =>Display symbol table</br>
	-l     =>Display literal table</br>
	-i     =>Display intermediate code</br>
	-lst   =>Disply lst code</br>
	-a     =>Display output of all tables</br>



<h4>ONE PASS</h4>

<h5>file name: symbol_table.py</h5>
 - error handaling</br>
 - find all symbols</br>
 - find symbol address 	</br>
 

<h5>file name: literal_table.py</h5>
 - find all literal and its convert hex</br>
 

<h5>file name: intermediate.py</h5>
 - handaling symbol and literal using symbol table and literal table</br>
 - handaling all instrction in opcode table</br>
 - replacing all opcode in opcode table</br>
 

<h5>file name: error_table.py</h5>
 - Contains error text</br>
 
<h4>TWO PASS</h4>


<h5>file name: lst.py</h5>
 - Finding  and handaling all data section addressing</br>
 - Finding  and handaling all bss section addressing </br>
 - Finding  and handaling all text section addressing in (ModRM AND Opcode Instructions)</br>


<h5>file name: opcode.txt</h5>
 - Contains Opcode instruction</br>
 


<h1> Macro Assembler </h1>
 
 picsd-$python3 macro.py macro.asm</br>
 
 
 
