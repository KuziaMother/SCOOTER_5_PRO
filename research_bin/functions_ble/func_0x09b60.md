# func_0x09b60

| | |
|---|---|
| offset в файле | `0x09b60` |
| vaddr (база 0x01800000) | `0x01809b60` |
 | размер кода | 74 Б |
| регион | flash-драйвер / OTA-код (PLAIN) |

## Строки (ссылки через literal-пулы / movw+movt)

- (нет)

## Литералы и адреса

- 0x00200164 — RAM (r4)
- 0x00200964 — RAM (r1)
- 0x00201e14 — RAM (r1)
- 0x00201e20 — RAM (r1)

## Вызовы (callees)

- 0x01809ba2 (b, вне списка функций)

## Кто вызывает (callers / xrefs)

- (не найден в открытых регионах)

## Дизассембляция

```asm
  01809b60:  push {r4, lr}                     
  01809b62:  ldr r1, [pc, #0x3a4]              (RAM)
  01809b64:  ldr r4, [pc, #0x394]              (RAM)
  01809b66:  ldr r1, [r1]                      
  01809b68:  ldrb.w r0, [r4, #0x345]           
  01809b6c:  blx r1                            
  01809b6e:  ldr r1, [pc, #0x39c]              (RAM)
  01809b70:  ldrb.w r3, [r4, #0x345]           
  01809b74:  uxth r0, r0                       
  01809b76:  ldrb r2, [r1, #4]                 
  01809b78:  subs r2, r2, r3                   
  01809b7a:  muls r2, r0, r2                   
  01809b7c:  ldrsb.w r0, [r1, #0xa]            
  01809b80:  ldr r1, [pc, #0x38c]              (RAM)
  01809b82:  ldrb r1, [r1]                     
  01809b84:  subs r0, r0, r1                   
  01809b86:  add.w r1, r0, r0, lsl #3          
  01809b8a:  add.w r0, r1, r0, lsl #4          
  01809b8e:  adds.w r0, r2, r0, lsl #2         
  01809b92:  mov.w r1, #0x3e8                  
  01809b96:  bmi #0x1809b9e                    
  01809b98:  add.w r0, r0, #0x1f4              
  01809b9c:  b #0x1809ba2                      -> 0x09ba2 (вне списка функций)
  01809b9e:  sub.w r0, r0, #0x1f4              
  01809ba2:  sdiv r0, r0, r1                   
  01809ba6:  sxtb r0, r0                       
  01809ba8:  pop {r4, pc}                      
  ; --- literal-пул @0x09efc (1 слов) — ВНЕ границ функции ---
  09efc:  .word 0x00200164  ; RAM
  ; --- literal-пул @0x09f08 (3 слов) — ВНЕ границ функции ---
  09f08:  .word 0x00200964  ; RAM
  09f0c:  .word 0x00201e14  ; RAM
  09f10:  .word 0x00201e20  ; RAM
```
