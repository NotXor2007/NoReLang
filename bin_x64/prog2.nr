i;created by adam naanaa;
;example1;

BeginDirective	;directives are flags for compiler;
{include lowlevel}
{include vamd64_abi}
{dump writeckrnl}
EndDirective

BeginGlobal
{byte char <- 72,101,108,108,111,44,32,119,111,114,108,100,33} ;byte-word-dword-qword;
{byte char2 <- 10}
EndGlobal

BeginProgram
;curly brackets are used to separate instructions;
{writeckrnl(char:13),1,3,5}	;format: {ins,ln0,ln1,ln2,...};		;needs a memory address;
{writeckrnl(char2:1),2,4,6}
EndProgram

