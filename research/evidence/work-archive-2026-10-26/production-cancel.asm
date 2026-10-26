            0x00b2c410      sub   esp, 0x14
            0x00b2c413      push  ebx
            0x00b2c414      mov   ebx, ecx
            0x00b2c416      lea   ecx, dword [esp+0x08]
            0x00b2c41a      push  esi
            0x00b2c41b      push  edi
            0x00b2c41c      mov   eax, dword [ebx+0x04]
            0x00b2c41f      mov   esi, dword [ebx+0x1c]
            0x00b2c422      mov   edi, dword [ebx+0x18]
            0x00b2c425      mov   dword [esp+0x0c], eax
            0x00b2c429      lea   eax, dword [ebx+0x08]
            0x00b2c42c      push  eax
            0x00b2c42d      call  0x4f70d0
            0x00b2c432      mov   eax, dword [esp+0x0c]
            0x00b2c436      sub   esp, 0x14
            0x00b2c439      mov   ecx, esp
            0x00b2c43b      mov   dword [ecx], eax
            0x00b2c43d      lea   eax, dword [esp+0x24]
            0x00b2c441      push  eax
            0x00b2c442      add   ecx, 0x04
            0x00b2c445      call  0x4f70d0
            0x00b2c44a      push  dword [esp+0x3c]
            0x00b2c44e      push  dword [esp+0x3c]
            0x00b2c452      call  0xb28a70
            0x00b2c457      add   esp, 0x1c
            0x00b2c45a      mov   ecx, ebx
            0x00b2c45c      push  esi
            0x00b2c45d      push  edi
            0x00b2c45e      push  eax
            0x00b2c45f      call  0xb246b0
            0x00b2c464      pop   edi
            0x00b2c465      pop   esi
            0x00b2c466      pop   ebx
            0x00b2c467      add   esp, 0x14
            0x00b2c46a      ret   0x08
            0x00b2c46d      int3
            0x00b2c46e      int3
            0x00b2c46f      int3
            0x00b2c470      push  ebp
            0x00b2c471      mov   ebp, esp
            0x00b2c473      push  0xffffffff                           ; 255
            0x00b2c475      push  0x1868ec8
            0x00b2c47a      mov   eax, dword fs:[0x0]
            0x00b2c480      push  eax
            0x00b2c481      sub   esp, 0x10
            0x00b2c484      push  esi
            0x00b2c485      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2c48a      xor   eax, ebp
            0x00b2c48c      push  eax
            0x00b2c48d      lea   eax, dword [ebp-0x0c]
            0x00b2c490      mov   dword fs:[0x0], eax
            0x00b2c496      mov   esi, ecx
            0x00b2c498      lea   eax, dword [esi+0x08]
            0x00b2c49b      push  eax
            0x00b2c49c      push  dword [ebp+0x0c]
            0x00b2c49f      lea   eax, dword [ebp-0x1c]
            0x00b2c4a2      push  dword [ebp+0x08]
            0x00b2c4a5      push  eax
            0x00b2c4a6      call  0xb2e270
            0x00b2c4ab      add   esp, 0x10
            0x00b2c4ae      push  eax
            0x00b2c4af      push  dword [esi+0x04]
            0x00b2c4b2      mov   ecx, esi
            0x00b2c4b4      mov   dword [ebp-0x04], 0x00
            0x00b2c4bb      call  0xcdf490
            0x00b2c4c0      cmp   dword [ebp-0x1c], 0x00
            0x00b2c4c4      mov   dword [ebp-0x04], 0x01
            0x00b2c4cb      mov   dword [ebp-0x10], 0x00
        ,=< 0x00b2c4d2      jz    0xb2c4e1
        |   0x00b2c4d4      push  dword [ebp-0x14]
        |   0x00b2c4d7      push  0x00
        |   0x00b2c4d9      call  0x5291c0
        |   0x00b2c4de      add   esp, 0x08
        `-> 0x00b2c4e1      mov   ecx, dword [ebp-0x0c]
            0x00b2c4e4      mov   dword fs:[0x0], ecx
            0x00b2c4eb      pop   ecx
            0x00b2c4ec      pop   esi
            0x00b2c4ed      mov   esp, ebp
            0x00b2c4ef      pop   ebp
            0x00b2c4f0      ret   0x08
            0x00b2c4f3      int3
            0x00b2c4f4      int3
            0x00b2c4f5      int3
            0x00b2c4f6      int3
            0x00b2c4f7      int3
            0x00b2c4f8      int3
            0x00b2c4f9      int3
            0x00b2c4fa      int3
            0x00b2c4fb      int3
            0x00b2c4fc      int3
            0x00b2c4fd      int3
            0x00b2c4fe      int3
            0x00b2c4ff      int3
            0x00b2c500      push  ebp
            0x00b2c501      mov   ebp, esp
            0x00b2c503      push  0xffffffff                           ; 255
            0x00b2c505      push  0x184efb8
            0x00b2c50a      mov   eax, dword fs:[0x0]
            0x00b2e870      push  ebp
            0x00b2e871      mov   ebp, esp
            0x00b2e873      push  0xffffffff                           ; 255
            0x00b2e875      push  0x186932b
            0x00b2e87a      mov   eax, dword fs:[0x0]
            0x00b2e880      push  eax
            0x00b2e881      push  ecx
            0x00b2e882      push  ebx
            0x00b2e883      push  esi
            0x00b2e884      push  edi
            0x00b2e885      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2e88a      xor   eax, ebp
            0x00b2e88c      push  eax
            0x00b2e88d      lea   eax, dword [ebp-0x0c]
            0x00b2e890      mov   dword fs:[0x0], eax
            0x00b2e896      push  dword [0x1d6c084]
            0x00b2e89c      push  0x01                                 ; 1
            0x00b2e89e      push  0x20                                 ; 32
            0x00b2e8a0      push  0x01                                 ; 1
            0x00b2e8a2      call  0x529280
            0x00b2e8a7      mov   esi, eax
            0x00b2e8a9      add   esp, 0x10
            0x00b2e8ac      mov   dword [ebp-0x10], esi
            0x00b2e8af      mov   dword [ebp-0x04], 0x00
            0x00b2e8b6      test  esi, esi
        ,=< 0x00b2e8b8      jz    0xb2e8dc
        |   0x00b2e8ba      mov   ecx, esi
        |   0x00b2e8bc      call  0xb21f60
        |   0x00b2e8c1      mov   dword [esi], 0x19a18f4               ; [0x19a18f4:4]=0x561c50
        |   0x00b2e8c7      lea   ecx, dword [esi+0x08]
        |   0x00b2e8ca      mov   byte [ebp-0x04], 0x01
        |   0x00b2e8ce      mov   dword [esi+0x04], 0x00
        |   0x00b2e8d5      call  0x4f71f0
       ,==< 0x00b2e8da      jmp   0xb2e8de
       |`-> 0x00b2e8dc      xor   esi, esi
       `--> 0x00b2e8de      mov   edi, dword [ebp+0x08]
            0x00b2e8e1      lea   ebx, dword [esi+0x04]
            0x00b2e8e4      push  0x04                                 ; 4
            0x00b2e8e6      push  ebx
            0x00b2e8e7      mov   ecx, edi
            0x00b2e8e9      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b2e8f0      mov   eax, dword [edi]
            0x00b2e8f2      mov   eax, dword [eax+0x04]
            0x00b2e8f5      call  eax
            0x00b2e8f7      test  al, al
        ,=< 0x00b2e8f9      jz    0xb2e953
        |   0x00b2e8fb      mov   eax, dword [edi]
        |   0x00b2e8fd      mov   ecx, edi
        |   0x00b2e8ff      push  0x10                                 ; 16
        |   0x00b2e901      mov   edx, dword [eax+0x04]
        |   0x00b2e904      lea   eax, dword [ebx+0x04]
        |   0x00b2e907      push  eax
        |   0x00b2e908      call  edx
        |   0x00b2e90a      test  al, al
       ,==< 0x00b2e90c      jz    0xb2e953
       ||   0x00b2e90e      mov   eax, dword [edi]
       ||   0x00b2e910      lea   ecx, dword [ebp+0x08]
       ||   0x00b2e913      push  0x04                                 ; 4
       ||   0x00b2e915      push  ecx
       ||   0x00b2e916      mov   ecx, edi
       ||   0x00b2e918      mov   eax, dword [eax+0x04]
       ||   0x00b2e91b      call  eax
       ||   0x00b2e91d      test  al, al
      ,===< 0x00b2e91f      jz    0xb2e953
      |||   0x00b2e921      mov   eax, dword [ebp+0x08]
      |||   0x00b2e924      cmp   eax, 0x0e                            ; 0xe ; 14
     ,====< 0x00b2e927      jnbe  0xb2e953
     ||||   0x00b2e929      mov   dword [esi+0x18], eax
     ||||   0x00b2e92c      mov   ecx, edi
     ||||   0x00b2e92e      mov   eax, dword [edi]
     ||||   0x00b2e930      push  0x04                                 ; 4
     ||||   0x00b2e932      mov   edx, dword [eax+0x04]
     ||||   0x00b2e935      lea   eax, dword [esi+0x1c]
     ||||   0x00b2e938      push  eax
     ||||   0x00b2e939      call  edx
     ||||   0x00b2e93b      test  al, al
    ,=====< 0x00b2e93d      jz    0xb2e957
    |||||   0x00b2e93f      mov   eax, esi
    |||||   0x00b2e941      mov   ecx, dword [ebp-0x0c]
    |||||   0x00b2e944      mov   dword fs:[0x0], ecx
    |||||   0x00b2e94b      pop   ecx
    |||||   0x00b2e94c      pop   edi
    |||||   0x00b2e94d      pop   esi
    |||||   0x00b2e94e      pop   ebx
    |||||   0x00b2e94f      mov   esp, ebp
    |||||   0x00b2e951      pop   ebp
    |||||   0x00b2e952      ret
    |````-> 0x00b2e953      test  esi, esi
    |   ,=< 0x00b2e955      jz    0xb2e960
    `-----> 0x00b2e957      mov   eax, dword [esi]
        |   0x00b2e959      mov   ecx, esi
        |   0x00b2e95b      push  0x01                                 ; 1
        |   0x00b2e95d      call  dword [eax+0x08]                     ; 8
        `-> 0x00b2e960      xor   eax, eax
            0x00b2e962      mov   ecx, dword [ebp-0x0c]
            0x00b2e965      mov   dword fs:[0x0], ecx
            0x00b2e96c      pop   ecx
            0x00b2e96d      pop   edi
            0x00b2e96e      pop   esi
            0x00b2e96f      pop   ebx
            0x00b2e970      mov   esp, ebp
            0x00b2e972      pop   ebp
            0x00b2e973      ret
            0x00b2e974      int3
            0x00b2e975      int3
            0x00b2e976      int3
            0x00b2e977      int3
            0x00b2e978      int3
            0x00b2e979      int3
            0x00b2e97a      int3
            0x00b2e97b      int3
            0x00b2e97c      int3
            0x00b2e97d      int3
            0x00b2e97e      int3
            0x00b2e97f      int3
            0x00b2e980      push  ebp
            0x00b2e981      mov   ebp, esp
            0x00b2e983      push  0xffffffff                           ; 255
            0x00b2e985      push  0x1848d23
            0x00b2e98a      mov   eax, dword fs:[0x0]
            0x00b2e990      push  eax
            0x00b2e991      push  ecx
            0x00b2e992      push  esi
            0x00b2e993      push  edi
            0x00b2e994      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2e999      xor   eax, ebp
            0x00b2e99b      push  eax
            0x00b2e99c      lea   eax, dword [ebp-0x0c]
            0x00b2e99f      mov   dword fs:[0x0], eax
            0x00b2e9a5      push  dword [0x1d6c084]
            0x00b2e9ab      push  0x01                                 ; 1
            0x00b2e9ad      push  0x18                                 ; 24
            0x00b2e9af      push  0x01                                 ; 1
            0x00b2e9b1      call  0x529280
            0x00b2e9b6      mov   esi, eax
            0x00b2e9b8      add   esp, 0x10
            0x00b2e9bb      mov   dword [ebp-0x10], esi
            0x00b2e9be      mov   dword [ebp-0x04], 0x00
            0x00b2e9c5      test  esi, esi
        ,=< 0x00b2e9c7      jz    0xb2e9ed
        |   0x00b2e9c9      mov   ecx, esi
        |   0x00b2e9cb      call  0xb21f60
        |   0x00b2e9d0      mov   dword [esi], 0x19a1a34               ; [0x19a1a34:4]=0x5127a0
        |   0x00b2e9d6      mov   dword [esi+0x08], 0x00
        |   0x00b2e9dd      mov   dword [esi+0x10], 0x00
        |   0x00b2e9e4      mov   dword [esi+0x14], 0x00
       ,==< 0x00b2e9eb      jmp   0xb2e9ef
       |`-> 0x00b2e9ed      xor   esi, esi
       `--> 0x00b2e9ef      mov   edi, dword [ebp+0x08]
            0x00b2e9f2      mov   ecx, edi
            0x00b2e9f4      push  0x04                                 ; 4
            0x00b2e9f6      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b2e9fd      mov   eax, dword [edi]
            0x00b2e9ff      mov   edx, dword [eax+0x04]
            0x00b2ea02      lea   eax, dword [esi+0x04]
            0x00b2ea05      push  eax
            0x00b2ea06      call  edx
            0x00b2ea08      test  al, al
        ,=< 0x00b2ea0a      jnz   0xb2ea2c
        |   0x00b2ea0c      test  esi, esi
       ,==< 0x00b2ea0e      jz    0xb2ea19
       ||   0x00b2ea10      mov   eax, dword [esi]
       ||   0x00b2ea12      mov   ecx, esi
       ||   0x00b2ea14      push  0x01                                 ; 1
       ||   0x00b2ea16      call  dword [eax+0x08]                     ; 8
       `--> 0x00b2ea19      xor   eax, eax
        |   0x00b2ea1b      mov   ecx, dword [ebp-0x0c]
        |   0x00b2ea1e      mov   dword fs:[0x0], ecx
        |   0x00b2ea25      pop   ecx
        |   0x00b2ea26      pop   edi
        |   0x00b2ea27      pop   esi
        |   0x00b2ea28      mov   esp, ebp
        |   0x00b2ea2a      pop   ebp
        |   0x00b2ea2b      ret
        `-> 0x00b2ea2c      lea   eax, dword [esi+0x08]
            0x00b2ea2f      invalid
            0x00b240c7      push  esi
            0x00b240c8      call  0xb2fbc0
            0x00b240cd      add   esp, 0x04
            0x00b240d0      pop   esi
            0x00b240d1      ret
            0x00b240d2      push  esi
            0x00b240d3      call  0xb2edc0
            0x00b240d8      add   esp, 0x04
            0x00b240db      pop   esi
            0x00b240dc      ret
            0x00b240dd      push  esi
            0x00b240de      call  0xb2e870
            0x00b240e3      add   esp, 0x04
            0x00b240e6      pop   esi
            0x00b240e7      ret
            0x00b240e8      push  esi
            0x00b240e9      call  0xb2e760
            0x00b240ee      add   esp, 0x04
            0x00b240f1      pop   esi
            0x00b240f2      ret
            0x00b240f3      push  esi
            0x00b240f4      call  0xb2eeb0
            0x00b240f9      add   esp, 0x04
            0x00b240fc      pop   esi
            0x00b240fd      ret
            0x00b240fe      push  esi
            0x00b240ff      call  0xb2fea0
            0x00b24104      add   esp, 0x04
            0x00b24107      pop   esi
            0x00b24108      ret
            0x00b24109      push  esi
            0x00b2410a      call  0xb2f9e0
            0x00b2410f      add   esp, 0x04
            0x00b24112      pop   esi
            0x00b24113      ret
            0x00b24114      push  esi
            0x00b24115      call  0xb2fad0
            0x00b2411a      add   esp, 0x04
            0x00b2411d      pop   esi
            0x00b2411e      ret
            0x00b2411f      push  esi
            0x00b24120      call  0xb2e670
            0x00b24125      add   esp, 0x04
            0x00b24128      pop   esi
            0x00b24129      ret
            0x00b2412a      push  esi
            0x00b2412b      call  0xb30290
            0x00b24130      add   esp, 0x04
            0x00b24133      pop   esi
            0x00b24134      ret
            0x00b24135      push  esi
            0x00b24136      call  0xb303a0
            0x00b2413b      add   esp, 0x04
            0x00b2413e      pop   esi
            0x00b2413f      ret
            0x00b24140      push  esi
            0x00b24141      call  0xb2fdd0
            0x00b24146      add   esp, 0x04
            0x00b24149      pop   esi
            0x00b2414a      ret
            0x00b2414b      push  esi
            0x00b2414c      call  0xb301a0
            0x00b24151      add   esp, 0x04
            0x00b24154      pop   esi
            0x00b24155      ret
            0x00b24156      push  esi
            0x00b24157      call  0xb30570
            0x00b2415c      add   esp, 0x04
            0x00b2415f      pop   esi
            0x00b24160      ret
            0x00b24161      push  esi
            0x00b24162      call  0xb2f580
            0x00b24167      add   esp, 0x04
            0x00b2416a      pop   esi
            0x00b2416b      ret
            0x00b2416c      push  esi
            0x00b2416d      call  0xb2f3b0
            0x00b24172      add   esp, 0x04
            0x00b24175      pop   esi
            0x00b24176      ret
            0x00b24177      push  esi
            0x00b24178      call  0xb2f2e0
            0x00b2417d      add   esp, 0x04
            0x00b24180      pop   esi
            0x00b24181      ret
            0x00b24182      push  esi
            0x00b24183      invalid
            0x00b24184      cwde
            0x00b24185      mov   ch, 0x00
        :   0x00b2eae0      push  0x01                                 ; 1
        :   0x00b2eae2      call  dword [eax+0x08]                     ; 8
        :   0x00b2eae5      xor   eax, eax
        :   0x00b2eae7      mov   ecx, dword [ebp-0x0c]
        :   0x00b2eaea      mov   dword fs:[0x0], ecx
        :   0x00b2eaf1      pop   ecx
        :   0x00b2eaf2      pop   edi
        :   0x00b2eaf3      pop   esi
        :   0x00b2eaf4      mov   esp, ebp
        :   0x00b2eaf6      pop   ebp
        :   0x00b2eaf7      ret
        :   0x00b2eaf8      mov   eax, dword [edi]
        :   0x00b2eafa      mov   ecx, edi
        :   0x00b2eafc      push  0x04                                 ; 4
        :   0x00b2eafe      mov   edx, dword [eax+0x04]
        :   0x00b2eb01      lea   eax, dword [esi+0x14]
        :   0x00b2eb04      push  eax
        :   0x00b2eb05      call  edx
        :   0x00b2eb07      test  al, al
        `=< 0x00b2eb09      jz    0xb2ead8
            0x00b2eb0b      mov   eax, esi
            0x00b2eb0d      mov   ecx, dword [ebp-0x0c]
            0x00b2eb10      mov   dword fs:[0x0], ecx
            0x00b2eb17      pop   ecx
            0x00b2eb18      pop   edi
            0x00b2eb19      pop   esi
            0x00b2eb1a      mov   esp, ebp
            0x00b2eb1c      pop   ebp
            0x00b2eb1d      ret
            0x00b2eb1e      int3
            0x00b2eb1f      int3
            0x00b2eb20      push  ebp
            0x00b2eb21      mov   ebp, esp
            0x00b2eb23      push  0xffffffff                           ; 255
            0x00b2eb25      push  0x186932b
            0x00b2eb2a      mov   eax, dword fs:[0x0]
            0x00b2eb30      push  eax
            0x00b2eb31      push  ecx
            0x00b2eb32      push  ebx
            0x00b2eb33      push  esi
            0x00b2eb34      push  edi
            0x00b2eb35      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2eb3a      xor   eax, ebp
            0x00b2eb3c      push  eax
            0x00b2eb3d      lea   eax, dword [ebp-0x0c]
            0x00b2eb40      mov   dword fs:[0x0], eax
            0x00b2eb46      push  dword [0x1d6c084]
            0x00b2eb4c      push  0x01                                 ; 1
            0x00b2eb4e      push  0x28                                 ; '(' ; 40
            0x00b2eb50      push  0x01                                 ; 1
            0x00b2eb52      call  0x529280
            0x00b2eb57      mov   esi, eax
            0x00b2eb59      add   esp, 0x10
            0x00b2eb5c      mov   dword [ebp-0x10], esi
            0x00b2eb5f      mov   dword [ebp-0x04], 0x00
            0x00b2eb66      test  esi, esi
        ,=< 0x00b2eb68      jz    0xb2eb8c
        |   0x00b2eb6a      mov   ecx, esi
        |   0x00b2eb6c      call  0xb21f60
        |   0x00b2eb71      mov   dword [esi], 0x19a1a84               ; [0x19a1a84:4]=0x5127a0
        |   0x00b2eb77      lea   ecx, dword [esi+0x10]
        |   0x00b2eb7a      mov   byte [ebp-0x04], 0x01
        |   0x00b2eb7e      mov   dword [esi+0x0c], 0x00
        |   0x00b2eb85      call  0x4f71f0
       ,==< 0x00b2eb8a      jmp   0xb2eb8e
       |`-> 0x00b2eb8c      xor   esi, esi
       `--> 0x00b2eb8e      mov   edi, dword [ebp+0x08]
            0x00b2eb91      mov   ecx, edi
            0x00b2eb93      push  0x04                                 ; 4
            0x00b2eb95      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b2eb9c      mov   eax, dword [edi]
            0x00b2eb9e      mov   edx, dword [eax+0x04]
            0x00b2eba1      lea   eax, dword [esi+0x04]
            0x00b2eba4      push  eax
            0x00b2eba5      call  edx
            0x00b2eba7      test  al, al
        ,=< 0x00b2eba9      jz    0xb2ec35
        |   0x00b2ebaf      mov   eax, dword [edi]
        |   0x00b2ebb1      mov   ecx, edi
        |   0x00b2ebb3      push  0x04                                 ; 4
        |   0x00b2ebb5      mov   edx, dword [eax+0x04]
        |   0x00b2ebb8      lea   eax, dword [esi+0x08]
        |   0x00b2ebbb      push  eax
        |   0x00b2ebbc      call  edx
        |   0x00b2ebbe      test  al, al
       ,==< 0x00b2ebc0      jz    0xb2ec35
       ||   0x00b2ebc2      mov   eax, dword [edi]
       ||   0x00b2ebc4      lea   ebx, dword [esi+0x0c]
       ||   0x00b2ebc7      push  0x04                                 ; 4
       ||   0x00b2ebc9      push  ebx
       ||   0x00b2ebca      mov   ecx, edi
       ||   0x00b2ebcc      mov   eax, dword [eax+0x04]
       ||   0x00b2ebcf      call  eax
       ||   0x00b2ebd1      test  al, al
      ,===< 0x00b2ebd3      jz    0xb2ec35
      |||   0x00b2ebd5      mov   eax, dword [edi]
      |||   0x00b2ebd7      mov   ecx, edi
      |||   0x00b2ebd9      push  0x10                                 ; 16
      |||   0x00b2ebdb      mov   edx, dword [eax+0x04]
      |||   0x00b2ebde      lea   eax, dword [ebx+0x04]
      |||   0x00b2ebe1      push  eax
      |||   0x00b2ebe2      call  edx
      |||   0x00b2ebe4      test  al, al
     ,====< 0x00b2ebe6      jz    0xb2ec35
     ||||   0x00b2ebe8      mov   eax, dword [edi]
     ||||   0x00b2ebea      mov   ecx, edi
     ||||   0x00b2ebec      push  0x04                                 ; 4
     ||||   0x00b2ebee      mov   edx, dword [eax+0x04]
     ||||   0x00b2ebf1      lea   eax, dword [esi+0x20]
     ||||   0x00b2ebf4      push  eax
     ||||   0x00b2ebf5      call  edx
     ||||   0x00b2ebf7      test  al, al
    ,=====< 0x00b2ebf9      jz    0xb2ec35
    |||||   0x00b2ebfb      mov   eax, dword [edi]
    |||||   0x00b2ebfd      mov   ecx, edi
    |||||   0x00b2ebff      push  0x01                                 ; 1
    |||||   0x00b2ec01      mov   edx, dword [eax+0x04]
    |||||   0x00b2ec04      lea   eax, dword [esi+0x24]
    |||||   0x00b2ec07      push  eax
    |||||   0x00b2ec08      call  edx
    |||||   0x00b2ec0a      test  al, al
   ,======< 0x00b2ec0c      jz    0xb2ec35
   ||||||   0x00b2ec0e      mov   eax, dword [edi]
   ||||||   0x00b2ec10      mov   ecx, edi
   ||||||   0x00b2ec12      push  0x01                                 ; 1
   ||||||   0x00b2ec14      mov   edx, dword [eax+0x04]
   ||||||   0x00b2ec17      lea   eax, dword [esi+0x25]
   ||||||   0x00b2ec1a      push  eax
   ||||||   0x00b2ec1b      call  edx
   ||||||   0x00b2ec1d      test  al, al
  ,=======< 0x00b2ec1f      jz    0xb2ec35
  |||||||   0x00b2ec21      mov   eax, esi
  |||||||   0x00b2ec23      mov   ecx, dword [ebp-0x0c]
  |||||||   0x00b2ec26      mov   dword fs:[0x0], ecx
  |||||||   0x00b2ec2d      pop   ecx
  |||||||   0x00b2ec2e      pop   edi
  |||||||   0x00b2ec2f      pop   esi
  |||||||   0x00b2ec30      pop   ebx
  |||||||   0x00b2ec31      mov   esp, ebp
  |||||||   0x00b2ec33      pop   ebp
  |||||||   0x00b2ec34      ret
  ```````-> 0x00b2ec35      test  esi, esi
        ,=< 0x00b2ec37      jz    0xb2ec42
        |   0x00b2ec39      mov   eax, dword [esi]
        |   0x00b2ec3b      mov   ecx, esi
        |   0x00b2ec3d      push  0x01                                 ; 1
        |   0x00b2ec3f      call  dword [eax+0x08]                     ; 8
        `-> 0x00b2ec42      xor   eax, eax
            0x00b2ec44      mov   ecx, dword [ebp-0x0c]
            0x00b2ec47      mov   dword fs:[0x0], ecx
            0x00b2ec4e      pop   ecx
            0x00b2ec4f      pop   edi
            0x00b2ec50      pop   esi
            0x00b2ec51      pop   ebx
            0x00b2ec52      mov   esp, ebp
            0x00b2ec54      pop   ebp
            0x00b2ec55      ret
            0x00b2ec56      int3
            0x00b2ec57      int3
            0x00b2ec58      int3
            0x00b2ec59      int3
            0x00b2ec5a      int3
            0x00b2ec5b      int3
            0x00b2ec5c      int3
            0x00b2ec5d      int3
            0x00b2ec5e      int3
            0x00b2ec5f      int3
            0x00b2ec60      push  ebp
            0x00b2ec61      mov   ebp, esp
            0x00b2ec63      push  0xffffffff                           ; 255
            0x00b2ec65      push  0x1810693
            0x00b2ec6a      mov   eax, dword fs:[0x0]
            0x00b2ec70      push  eax
            0x00b2ec71      push  ecx
            0x00b2ec72      push  esi
            0x00b2ec73      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2ec78      xor   eax, ebp
            0x00b2ec7a      push  eax
            0x00b2ec7b      lea   eax, dword [ebp-0x0c]
            0x00b2ec7e      mov   dword fs:[0x0], eax
            0x00b2ec84      push  dword [0x1d6c084]
            0x00b2ec8a      push  0x01                                 ; 1
            0x00b2ec8c      push  0x08                                 ; 8
            0x00b2ec8e      push  0x01                                 ; 1
            0x00b2ec90      call  0x529280
            0x00b2ec95      mov   esi, eax
            0x00b2ec97      add   esp, 0x10
            0x00b2ec9a      mov   dword [ebp-0x10], esi
            0x00b2ec9d      mov   dword [ebp-0x04], 0x00
            0x00b2eca4      test  esi, esi
        ,=< 0x00b2eca6      jz    0xb2ecb7
        |   0x00b2eca8      mov   ecx, esi
        |   0x00b2ecaa      call  0xb21f60
        |   0x00b2ecaf      mov   dword [esi], 0x19a1a5c               ; [0x19a1a5c:4]=0x5127a0
       ,==< 0x00b2ecb5      jmp   0xb2ecb9
       |`-> 0x00b2ecb7      xor   esi, esi
       `--> 0x00b2ecb9      mov   ecx, dword [ebp+0x08]
            0x00b2ecbc      push  0x04                                 ; 4
            0x00b2ecbe      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b2ecc5      mov   eax, dword [ecx]
            0x00b2ecc7      mov   edx, dword [eax+0x04]
            0x00b2ecca      lea   eax, dword [esi+0x04]
            0x00b2eccd      push  eax
            0x00b2ecce      call  edx
            0x00b2ecd0      test  al, al
        ,=< 0x00b2ecd2      jnz   0xb2ecf3
        |   0x00b2ecd4      test  esi, esi
       ,==< 0x00b2ecd6      jz    0xb2ece1
       ||   0x00b2ecd8      mov   eax, dword [esi]
       ||   0x00b2ecda      mov   ecx, esi
       ||   0x00b2ecdc      push  0x01                                 ; 1
       ||   0x00b2ecde      invalid
       ||   0x00b2ecdf      push  eax
            0x00ba90a0      mov   eax, dword [ecx+0x1c]
            0x00ba90a3      push  esi
            0x00ba90a4      push  edi
            0x00ba90a5      mov   edi, dword [ecx+0x18]
            0x00ba90a8      lea   esi, dword [edi+eax*4]
            0x00ba90ab      cmp   esi, edi
        ,=< 0x00ba90ad      jz    0xba90ca
        |   0x00ba90af      push  ebx
        |   0x00ba90b0      mov   ebx, dword [esp+0x10]
       .--> 0x00ba90b4      mov   eax, dword [ebx]
       :|   0x00ba90b6      add   esi, 0xfffffffc                      ; 4294967292
       :|   0x00ba90b9      mov   ecx, ebx
       :|   0x00ba90bb      push  dword [esi]
       :|   0x00ba90bd      mov   eax, dword [eax]
       :|   0x00ba90bf      call  eax
       :|   0x00ba90c1      test  al, al
      ,===< 0x00ba90c3      jnz   0xba90c9
      |:|   0x00ba90c5      cmp   esi, edi
      |`==< 0x00ba90c7      jnz   0xba90b4
      `---> 0x00ba90c9      pop   ebx
        `-> 0x00ba90ca      pop   edi
            0x00ba90cb      pop   esi
            0x00ba90cc      ret   0x04
            0x00ba90cf      int3
            0x00ba90d0      movss xmm1, dword [esp+0x04]
            0x00ba90d6      movss xmm2, dword [0x193e5dc]              ; [0x193e5dc:4]=0x40c90fdb
            0x00ba90de      movaps xmm0, xmm1
            0x00ba90e1      divss xmm0, xmm2
            0x00ba90e5      cvtps2pd xmm0, xmm0
            0x00ba90e8      cvttsd2si eax, xmm0
            0x00ba90ec      movd  xmm0, eax
            0x00ba90f0      cvtdq2ps xmm0, xmm0
            0x00ba90f3      mulss xmm0, xmm2
            0x00ba90f7      subss xmm1, xmm0
            0x00ba90fb      movss xmm0, dword [0x193e5f8]              ; [0x193e5f8:4]=0xc0490fdb
            0x00ba9103      comiss xmm0, xmm1
        ,=< 0x00ba9106      jb    0xba910e
        |   0x00ba9108      addss xmm1, xmm2
       ,==< 0x00ba910c      jmp   0xba911b
       |`-> 0x00ba910e      comiss xmm1, dword [0x193e5cc]
       |,=< 0x00ba9115      jbe   0xba911b
       ||   0x00ba9117      subss xmm1, xmm2
       ``-> 0x00ba911b      movss xmm2, dword [0x19ac4e0]              ; [0x19ac4e0:4]=0xbf490fdb
            0x00ba9123      comiss xmm1, xmm2
            0x00ba9126      movss xmm0, dword [0x19ab39c]              ; [0x19ab39c:4]=0x3f490fdb
        ,=< 0x00ba912e      jbe   0xba9138
        |   0x00ba9130      comiss xmm0, xmm1
       ,==< 0x00ba9133      jb    0xba9138
       ||   0x00ba9135      fldz
       ||   0x00ba9137      ret
       ``-> 0x00ba9138      comiss xmm1, xmm0
        ,=< 0x00ba913b      jbe   0xba9151
        |   0x00ba913d      movss xmm0, dword [0x19ac4dc]              ; [0x19ac4dc:4]=0x4016cbe4
        |   0x00ba9145      comiss xmm0, xmm1
       ,==< 0x00ba9148      jb    0xba9151
       ||   0x00ba914a      fld   dword [0x193e5b4]
       ||   0x00ba9150      ret
       ``-> 0x00ba9151      comiss xmm1, dword [0x19ac4e4]
        ,=< 0x00ba9158      jbe   0xba9166
        |   0x00ba915a      comiss xmm2, xmm1
       ,==< 0x00ba915d      jb    0xba9166
       ||   0x00ba915f      fld   dword [0x193e5f4]
       ||   0x00ba9165      ret
       ``-> 0x00ba9166      fld   dword [0x193e5cc]
            0x00ba916c      ret
            0x00ba916d      int3
            0x00ba916e      int3
            0x00ba916f      int3
            0x00ba9170      push  ebp
            0x00ba9171      mov   ebp, esp
            0x00ba9173      push  0xffffffff                           ; 255
            0x00ba9175      push  0x184d3f8
            0x00ba917a      mov   eax, dword fs:[0x0]
            0x00ba9180      push  eax
            0x00ba9181      sub   esp, 0x2c
            0x00ba9184      push  esi
            0x00ba9185      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00ba918a      xor   eax, ebp
            0x00ba918c      push  eax
            0x00ba918d      lea   eax, dword [ebp-0x0c]
            0x00ba9190      mov   dword fs:[0x0], eax
            0x00ba9196      mov   esi, ecx
            0x00ba9198      push  dword [ebp+0x08]
            0x00ba919b      lea   ecx, dword [ebp-0x38]
            0x00ba919e      call  0xb57f80
            0x00ba91a3      push  dword [ebp+0x0c]
            0x00ba91a6      lea   eax, dword [ebp-0x38]
            0x00ba91a9      mov   dword [ebp-0x04], 0x00
            0x00ba91b0      push  eax
            0x00ba91b1      mov   ecx, esi
            0x00ba91b3      call  0xa87bd0
            0x00ba91b8      push  0x01                                 ; 1
            0x00ba91ba      lea   eax, dword [esi+0x10]
            0x00ba91bd      push  eax
            0x00ba91be      lea   ecx, dword [ebp-0x38]
            0x00ba91c1      call  0xb5abf0
            0x00ba91c6      lea   ecx, dword [ebp-0x38]
            0x00ba91c9      call  0xb589a0
            0x00ba91ce      mov   ecx, dword [ebp-0x0c]
            0x00ba91d1      mov   dword fs:[0x0], ecx
            0x00ba91d8      pop   ecx
            0x00ba91d9      pop   esi
            0x00ba91da      mov   esp, ebp
            0x00ba91dc      pop   ebp
            0x00ba91dd      ret   0x08
            0x00ba91e0      push  ebp
            0x00ba91e1      mov   ebp, esp
            0x00ba91e3      push  0xffffffff                           ; 255
            0x00ba91e5      push  0x184d368
            0x00ba91ea      mov   eax, dword fs:[0x0]
            0x00ba91f0      push  eax
            0x00ba91f1      sub   esp, 0x1c
            0x00ba91f4      push  esi
            0x00ba91f5      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00ba91fa      xor   eax, ebp
            0x00ba91fc      push  eax
            0x00ba91fd      lea   eax, dword [ebp-0x0c]
            0x00ba9200      mov   dword fs:[0x0], eax
            0x00ba9206      mov   esi, ecx
            0x00ba9208      push  dword [ebp+0x08]
            0x00ba920b      lea   ecx, dword [ebp-0x28]
            0x00ba920e      call  0xb58330
            0x00ba9213      push  dword [ebp+0x0c]
            0x00ba9216      lea   eax, dword [ebp-0x28]
            0x00ba9219      mov   dword [ebp-0x04], 0x00
            0x00ba9220      push  eax
            0x00ba9221      mov   ecx, esi
            0x00ba9223      call  0xa87bf0
            0x00ba9228      mov   ecx, dword [ebp-0x10]
            0x00ba922b      lea   edx, dword [ebp+0x08]
            0x00ba922e      mov   al, byte [esi+0x10]
            0x00ba9231      mov   byte [ebp+0x08], al
            0x00ba9234      push  0x01                                 ; 1
            0x00ba9236      mov   eax, dword [ecx]
            0x00ba9238      push  edx
            0x00ba9239      call  dword [eax+0x1c]                     ; 28
            0x00ba923c      lea   ecx, dword [ebp-0x28]
            0x00ba923f      call  0xb589c0
            0x00ba9244      mov   ecx, dword [ebp-0x0c]
            0x00ba9247      mov   dword fs:[0x0], ecx
            0x00ba924e      pop   ecx
            0x00ba924f      pop   esi
            0x00ba9250      mov   esp, ebp
            0x00ba9252      pop   ebp
            0x00ba9253      ret   0x08
            0x00ba9256      int3
            0x00ba9257      int3
            0x00ba9258      int3
            0x00ba9259      int3
            0x00ba925a      int3
            0x00ba925b      int3
            0x00ba925c      int3
            0x00ba925d      int3
            0x00ba925e      int3
            0x00ba925f      int3
            0x00ba9260      push  esi
            0x00ba9261      push  edi
            0x00ba9262      push  dword [esp+0x10]
            0x00ba9266      mov   edi, dword [esp+0x10]
            0x00ba926a      mov   esi, ecx
            0x00ba926c      push  edi
            0x00ba926d      call  0x51dbd0
            0x00ba9272      mov   al, byte [esi+0x10]
            0x00ba9275      lea   ecx, dword [edi+0x10]
            0x00ba9278      neg   ecx
            0x00ba927a      mov   byte [esp+0x10], al
            0x00ba927e      push  0x01                                 ; 1
            0x00ba9280      lea   eax, dword [esp+0x14]
            0x00ba9284      sbb   ecx, ecx
            0x00ba9286      push  eax
            0x00ba9287      and   ecx, edi
            0x00ba9289      call  0xb5ae20
            0x00ba928e      pop   edi
            0x00ba928f      pop   esi
            0x00ba9290      ret   0x08
            0x00ba9293      int3
            0x00ba9294      int3
            0x00ba9295      int3
            0x00ba9296      int3
            0x00ba9297      int3
            0x00ba9298      int3
            0x00ba9299      int3
            0x00ba929a      int3
            0x00ba929b      int3
            0x00ba929c      int3
            0x00ba929d      int3
            0x00ba929e      int3
            0x00ba929f      int3
            0x00ba92a0      push  ebp
            0x00ba92a1      mov   ebp, esp
            0x00ba92a3      push  0xffffffff                           ; 255
            0x00ba92a5      push  0x184d3f8
            0x00ba92aa      mov   eax, dword fs:[0x0]
            0x00ba92b0      push  eax
            0x00ba92b1      sub   esp, 0x2c
            0x00ba92b4      push  esi
            0x00ba92b5      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00ba92ba      xor   eax, ebp
            0x00ba92bc      push  eax
            0x00ba92bd      lea   eax, dword [ebp-0x0c]
            0x00ba92c0      mov   dword fs:[0x0], eax
            0x00ba92c6      mov   esi, ecx
            0x00ba92c8      push  dword [ebp+0x08]
            0x00ba92cb      lea   ecx, dword [ebp-0x38]
            0x00ba92ce      call  0xb580a0
            0x00ba92d3      push  dword [ebp+0x0c]
            0x00ba92d6      lea   eax, dword [ebp-0x38]
            0x00ba92d9      mov   dword [ebp-0x04], 0x00
            0x00ba92e0      push  eax
            0x00ba92e1      mov   ecx, esi
            0x00ba92e3      call  0xa87bd0
            0x00ba92e8      push  0x01                                 ; 1
            0x00ba92ea      lea   eax, dword [esi+0x10]
            0x00ba92ed      push  eax
            0x00ba92ee      lea   ecx, dword [ebp-0x38]
            0x00ba92f1      call  0xb5abf0
            0x00ba92f6      lea   ecx, dword [ebp-0x38]
            0x00ba92f9      call  0xb589a0
            0x00ba92fe      mov   ecx, dword [ebp-0x0c]
            0x00ba9301      mov   dword fs:[0x0], ecx
            0x00ba9308      pop   ecx
            0x00ba9309      pop   esi
            0x00ba930a      mov   esp, ebp
            0x00ba930c      pop   ebp
            0x00ba930d      ret   0x08
            0x00ba9310      push  ebp
            0x00ba9311      mov   ebp, esp
            0x00ba9313      push  0xffffffff                           ; 255
            0x00ba9315      push  0x184d3f8
            0x00ba931a      mov   eax, dword fs:[0x0]
            0x00ba9320      push  eax
            0x00ba9321      sub   esp, 0x2c
            0x00ba9324      push  esi
            0x00ba9325      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00ba932a      xor   eax, ebp
            0x00ba932c      push  eax
            0x00ba932d      lea   eax, dword [ebp-0x0c]
            0x00ba9330      mov   dword fs:[0x0], eax
            0x00ba9336      mov   esi, ecx
            0x00ba9338      push  dword [ebp+0x08]
            0x00ba933b      lea   ecx, dword [ebp-0x38]
            0x00ba933e      call  0xb581e0
            0x00ba9343      push  dword [ebp+0x0c]
            0x00ba9346      lea   eax, dword [ebp-0x38]
            0x00ba9349      mov   dword [ebp-0x04], 0x00
            0x00ba9350      push  eax
            0x00ba9351      mov   ecx, esi
            0x00ba9353      call  0xa87bd0
            0x00ba9358      push  0x01                                 ; 1
            0x00ba935a      lea   eax, dword [esi+0x10]
            0x00ba935d      push  eax
            0x00ba935e      lea   ecx, dword [ebp-0x38]
            0x00ba9361      call  0xb5abf0
            0x00ba9366      lea   ecx, dword [ebp-0x38]
            0x00ba9369      call  0xb589a0
            0x00ba936e      mov   ecx, dword [ebp-0x0c]
            0x00ba9371      mov   dword fs:[0x0], ecx
            0x00ba9378      pop   ecx
            0x00ba9379      pop   esi
            0x00ba937a      mov   esp, ebp
            0x00ba937c      pop   ebp
            0x00ba937d      ret   0x08
            0x00ba9380      push  ebp
            0x00ba9381      mov   ebp, esp
            0x00ba9383      push  0xffffffff                           ; 255
            0x00ba9385      push  0x184d3f8
            0x00ba938a      mov   eax, dword fs:[0x0]
            0x00ba9390      push  eax
            0x00ba9391      sub   esp, 0x2c
            0x00ba9394      push  esi
            0x00ba9395      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00ba939a      xor   eax, ebp
            0x00ba939c      push  eax
            0x00ba939d      lea   eax, dword [ebp-0x0c]
            0x00ba93a0      mov   dword fs:[0x0], eax
            0x00ba93a6      mov   esi, ecx
            0x00ba93a8      push  dword [ebp+0x08]
            0x00ba93ab      lea   ecx, dword [ebp-0x38]
            0x00ba93ae      call  0xb57f80
            0x00ba93b3      push  dword [ebp+0x0c]
            0x00ba93b6      lea   eax, dword [ebp-0x38]
            0x00ba93b9      mov   dword [ebp-0x04], 0x00
            0x00ba93c0      push  eax
            0x00ba93c1      mov   ecx, esi
            0x00ba93c3      call  0xa87bd0
            0x00ba93c8      push  0x04                                 ; 4
            0x00ba93ca      lea   eax, dword [esi+0x0c]
            0x00ba93cd      push  eax
            0x00ba93ce      lea   ecx, dword [ebp-0x38]
            0x00ba93d1      call  0xb5abf0
            0x00ba93d6      push  0x04                                 ; 4
            0x00ba93d8      lea   eax, dword [esi+0x10]
            0x00ba93db      push  eax
            0x00ba93dc      lea   ecx, dword [ebp-0x38]
            0x00ba93df      call  0xb5abf0
            0x00ba93e4      push  0x04                                 ; 4
            0x00ba93e6      lea   eax, dword [esi+0x14]
            0x00ba93e9      push  eax
            0x00ba93ea      lea   ecx, dword [ebp-0x38]
            0x00ba93ed      call  0xb5abf0
            0x00ba93f2      push  0x04                                 ; 4
            0x00ba93f4      lea   eax, dword [ebp+0x08]
            0x00ba93f7      mov   dword [ebp+0x08], 0x00
            0x00ba93fe      push  eax
            0x00ba93ff      lea   ecx, dword [ebp-0x38]
            0x00ba9402      call  0xb5abf0
            0x00ba9407      mov   eax, dword [ebp+0x08]
            0x00ba940a      lea   ecx, dword [ebp-0x38]
            0x00ba940d      mov   dword [esi+0x18], eax
            0x00ba9410      lea   eax, dword [ebp+0x08]
            0x00ba9413      push  0x04                                 ; 4
            0x00ba9415      push  eax
            0x00ba9416      mov   dword [ebp+0x08], 0x00
            0x00ba941d      call  0xb5abf0
            0x00ba9422      mov   eax, dword [ebp+0x08]
            0x00ba9425      lea   ecx, dword [ebp-0x38]
            0x00ba9428      mov   dword [esi+0x08], eax
            0x00ba942b      call  0xb589a0
            0x00ba9430      mov   ecx, dword [ebp-0x0c]
            0x00ba9433      mov   dword fs:[0x0], ecx
            0x00ba943a      pop   ecx
            0x00ba943b      pop   esi
            0x00ba943c      mov   esp, ebp
            0x00ba943e      pop   ebp
            0x00ba943f      ret   0x08
            0x00ba9442      int3
            0x00ba9443      int3
            0x00ba9444      int3
            0x00ba9445      int3
            0x00ba9446      int3
            0x00ba9447      int3
            0x00ba9448      int3
            0x00ba9449      int3
            0x00ba944a      int3
            0x00ba944b      int3
            0x00ba944c      int3
            0x00ba944d      int3
            0x00ba944e      int3
            0x00ba944f      int3
            0x00ba9450      push  ebp
            0x00ba9451      mov   ebp, esp
            0x00ba9453      push  0xffffffff                           ; 255
            0x00ba9455      push  0x184d368
            0x00ba945a      mov   eax, dword fs:[0x0]
            0x00ba9460      push  eax
            0x00ba9461      sub   esp, 0x1c
            0x00ba9464      push  esi
            0x00ba9465      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00ba946a      xor   eax, ebp
            0x00ba946c      push  eax
            0x00ba946d      lea   eax, dword [ebp-0x0c]
            0x00ba9470      mov   dword fs:[0x0], eax
            0x00ba9476      mov   esi, ecx
            0x00ba9478      push  dword [ebp+0x08]
            0x00ba947b      lea   ecx, dword [ebp-0x28]
            0x00ba947e      call  0xb58330
            0x00ba9483      push  dword [ebp+0x0c]
            0x00ba9486      lea   eax, dword [ebp-0x28]
            0x00ba9489      mov   dword [ebp-0x04], 0x00
            0x00ba9490      push  eax
            0x00ba9491      mov   ecx, esi
            0x00ba9493      call  0xa87bf0
            0x00ba9498      mov   ecx, dword [ebp-0x10]
            0x00ba949b      lea   edx, dword [ebp+0x08]
            0x00ba949e      invalid
            0x00ba949f      inc   esi
            0x00c182a0      mov   ecx, dword [ecx+0x20]
            0x00c182a3      mov   eax, dword [esp+0x04]
            0x00c182a7      mov   eax, dword [ecx+eax*4]
            0x00c182aa      ret   0x04
            0x00c182ad      int3
            0x00c182ae      int3
            0x00c182af      int3
            0x00c182b0      push  ecx
            0x00c182b1      mov   eax, dword [esp+0x08]
            0x00c182b5      mov   edx, eax
            0x00c182b7      shl   eax, 0x04
            0x00c182ba      xor   edx, 0xdeadbeef
            0x00c182c0      add   edx, eax
            0x00c182c2      mov   eax, edx
            0x00c182c4      shr   eax, 0x0a
            0x00c182c7      xor   edx, eax
            0x00c182c9      mov   eax, edx
            0x00c182cb      shr   eax, 0x18
            0x00c182ce      add   eax, edx
            0x00c182d0      push  esi
            0x00c182d1      mov   esi, ecx
            0x00c182d3      imul  ecx, eax, 0x81
            0x00c182d9      lea   eax, dword [esp+0x04]
            0x00c182dd      push  eax
            0x00c182de      mov   eax, ecx
            0x00c182e0      shr   eax, 0x0d
            0x00c182e3      xor   eax, ecx
            0x00c182e5      lea   ecx, dword [esi+0x0c]
            0x00c182e8      push  eax
            0x00c182e9      lea   eax, dword [esp+0x14]
            0x00c182ed      push  eax
            0x00c182ee      call  0x4dc510
            0x00c182f3      mov   eax, dword [esp+0x04]
            0x00c182f7      mov   ecx, dword [eax+0x04]
            0x00c182fa      call  0x59e5f0
            0x00c182ff      pop   esi
            0x00c18300      pop   ecx
            0x00c18301      ret   0x04
            0x00c18304      int3
            0x00c18305      int3
            0x00c18306      int3
            0x00c18307      int3
            0x00c18308      int3
            0x00c18309      int3
            0x00c1830a      int3
            0x00c1830b      int3
            0x00c1830c      int3
            0x00c1830d      int3
            0x00c1830e      int3
            0x00c1830f      int3
            0x00c18310      push  ecx
            0x00c18311      mov   eax, dword [esp+0x08]
            0x00c18315      mov   edx, eax
            0x00c18317      shl   eax, 0x04
            0x00c1831a      xor   edx, 0xdeadbeef
            0x00c18320      add   edx, eax
            0x00c18322      mov   eax, edx
            0x00c18324      shr   eax, 0x0a
            0x00c18327      xor   edx, eax
            0x00c18329      mov   eax, edx
            0x00c1832b      shr   eax, 0x18
            0x00c1832e      add   eax, edx
            0x00c18330      push  esi
            0x00c18331      mov   esi, ecx
            0x00c18333      imul  ecx, eax, 0x81
            0x00c18339      lea   eax, dword [esp+0x04]
            0x00c1833d      push  eax
            0x00c1833e      mov   eax, ecx
            0x00c18340      shr   eax, 0x0d
            0x00c18343      xor   eax, ecx
            0x00c18345      lea   ecx, dword [esi+0x0c]
            0x00c18348      push  eax
            0x00c18349      lea   eax, dword [esp+0x14]
            0x00c1834d      push  eax
            0x00c1834e      call  0x4dc510
            0x00c18353      mov   eax, dword [esp+0x04]
            0x00c18357      pop   esi
            0x00c18358      mov   eax, dword [eax+0x04]
            0x00c1835b      add   eax, 0x40                            ; 64
            0x00c1835e      pop   ecx
            0x00c1835f      ret   0x04
            0x00c18362      int3
            0x00c18363      int3
            0x00c18364      int3
            0x00c18365      int3
            0x00c18366      int3
            0x00c18367      int3
            0x00c18368      int3
            0x00c18369      int3
            0x00c1836a      int3
            0x00c1836b      int3
            0x00c1836c      int3
            0x00c1836d      int3
            0x00c1836e      int3
            0x00c1836f      int3
            0x00c18370      mov   eax, dword [ecx]
            0x00c18372      push  dword [esp+0x04]
            0x00c18376      call  dword [eax+0x64]                     ; 100
            0x00c18379      movd  xmm0, eax
            0x00c1837d      cvtdq2pd xmm0, xmm0
            0x00c18381      shr   eax, 0x1f
            0x00c18384      addsd xmm0, qword [eax*8+0x1933920]
            0x00c1838d      cvtpd2ps xmm0, xmm0
            0x00c18391      mulss xmm0, dword [0x195ee48]
            0x00c18399      movss dword [esp+0x04], xmm0
            0x00c1839f      fld   dword [esp+0x04]
            0x00c183a3      ret   0x04
            0x00c183a6      int3
            0x00c183a7      int3
            0x00c183a8      int3
            0x00c183a9      int3
            0x00c183aa      int3
            0x00c183ab      int3
            0x00c183ac      int3
            0x00c183ad      int3
            0x00c183ae      int3
            0x00c183af      int3
            0x00c183b0      sub   esp, 0x08
            0x00c183b3      movss xmm0, dword [0x203d7f0]              ; [0x203d7f0:4]=0
            0x00c183bb      sub   esp, 0x08
            0x00c183be      mulss xmm0, dword [0x193efa0]
            0x00c183c6      cvtps2pd xmm0, xmm0
            0x00c183c9      movsd qword [esp+0x08], xmm0
            0x00c183cf      fld   qword [esp+0x08]
            0x00c183d3      fstp  qword [esp]
            0x00c183d6      call  0x1809c2e
            0x00c183db      fstp  qword [esp+0x08]
            0x00c183df      movsd xmm0, qword [esp+0x08]
            0x00c183e5      add   esp, 0x08
            0x00c183e8      cvtpd2ps xmm0, xmm0
            0x00c183ec      call  0x18077c0
            0x00c183f1      xorps xmm0, xmm0
            0x00c183f4      cvtsi2sd xmm0, eax
            0x00c183f8      shr   eax, 0x1f
            0x00c183fb      addsd xmm0, qword [eax*8+0x1933920]
            0x00c18404      cvtpd2ps xmm1, xmm0
            0x00c18408      comiss xmm1, dword [0x193e550]
        ,=< 0x00c1840f      jbe   0xc18427
        |   0x00c18411      movss xmm0, dword [0x193d168]              ; [0x193d168:4]=0x3f000000
        |   0x00c18419      addss xmm0, xmm1
        |   0x00c1841d      cvttss2si eax, xmm0
        |   0x00c18421      add   esp, 0x08
        |   0x00c18424      ret   0x04
        `-> 0x00c18427      movss xmm0, dword [0x193e8ec]              ; [0x193e8ec:4]=0xbf000000
            0x00c1842f      addss xmm0, xmm1
            0x00c18433      cvttss2si eax, xmm0
            0x00c18437      add   esp, 0x08
            0x00c1843a      ret   0x04
            0x00c1843d      int3
            0x00c1843e      int3
            0x00c1843f      int3
            0x00c18440      sub   esp, 0x08
            0x00c18443      push  dword [esp+0x0c]
            0x00c18447      call  0xa659b0
            0x00c1844c      add   esp, 0x04
            0x00c1844f      test  eax, eax
        ,=< 0x00c18451      jz    0xc18513
        |   0x00c18457      mov   ecx, eax
        |   0x00c18459      call  0x5c0950
        |   0x00c1845e      test  eax, eax
       ,==< 0x00c18460      jz    0xc18513
       ||   0x00c18466      movss xmm1, dword [0x203d7f0]              ; [0x203d7f0:4]=0
       ||   0x00c1846e      xorps xmm0, xmm0
       ||   0x00c18471      mulss xmm1, dword [0x19338e0]
       ||   0x00c18479      sub   esp, 0x08
       ||   0x00c1847c      cvtsi2sd xmm0, eax
       ||   0x00c18480      shr   eax, 0x1f
       ||   0x00c18483      addsd xmm0, qword [eax*8+0x1933920]
       ||   0x00c1848c      cvtpd2ps xmm0, xmm0
       ||   0x00c18490      divss xmm1, xmm0
       ||   0x00c18494      mulss xmm1, dword [0x193efa0]
       ||   0x00c1849c      cvtps2pd xmm0, xmm1
       ||   0x00c1849f      movsd qword [esp+0x08], xmm0
       ||   0x00c184a5      fld   qword [esp+0x08]
       ||   0x00c184a9      fstp  qword [esp]
       ||   0x00c184ac      call  0x1809c2e
       ||   0x00c184b1      fstp  qword [esp+0x08]
       ||   0x00c184b5      movsd xmm0, qword [esp+0x08]
       ||   0x00c184bb      add   esp, 0x08
       ||   0x00c184be      cvtpd2ps xmm0, xmm0
       ||   0x00c184c2      call  0x18077c0
       ||   0x00c184c7      xorps xmm0, xmm0
       ||   0x00c184ca      cvtsi2sd xmm0, eax
       ||   0x00c184ce      shr   eax, 0x1f
       ||   0x00c184d1      addsd xmm0, qword [eax*8+0x1933920]
       ||   0x00c184da      cvtpd2ps xmm1, xmm0
       ||   0x00c184de      comiss xmm1, dword [0x193e550]
      ,===< 0x00c184e5      jbe   0xc184fd
      |||   0x00c184e7      movss xmm0, dword [0x193d168]              ; [0x193d168:4]=0x3f000000
      |||   0x00c184ef      addss xmm0, xmm1
      |||   0x00c184f3      cvttss2si eax, xmm0
      |||   0x00c184f7      add   esp, 0x08
      |||   0x00c184fa      ret   0x04
      `---> 0x00c184fd      invalid
       ||   0x00c184fe      invalid
       ||   0x00c184ff      invalid
            0x00c07290      push  ebx
            0x00c07291      push  esi
            0x00c07292      mov   esi, dword [esp+0x10]
            0x00c07296      push  edi
            0x00c07297      mov   edi, ecx
            0x00c07299      mov   ebx, dword [edi+0x0c]
            0x00c0729c      mov   eax, dword [edi+0x08]
            0x00c0729f      imul  edx, ebx, 0xb4
            0x00c072a5      add   edx, eax
            0x00c072a7      cmp   eax, edx
        ,=< 0x00c072a9      jz    0xc072c3
        |   0x00c072ab      nop   dword [eax+eax*1], eax
       .--> 0x00c072b0      cmp   dword [eax], 0x3e                    ; '>'
      ,===< 0x00c072b3      jnz   0xc072ba
      |:|   0x00c072b5      cmp   dword [eax+0x04], esi
     ,====< 0x00c072b8      jz    0xc072f3
     |`---> 0x00c072ba      add   eax, 0xb4                            ; 180
     | :|   0x00c072bf      cmp   eax, edx
     | `==< 0x00c072c1      jnz   0xc072b0
     | .`-> 0x00c072c3      cmp   ebx, dword [edi]
     | :,=< 0x00c072c5      jnz   0xc072cc
     | :|   0x00c072c7      call  0x9d6ad0
     | :`-> 0x00c072cc      imul  ecx, ebx, 0xb4
     | :    0x00c072d2      lea   eax, dword [ebx+0x01]
     | :    0x00c072d5      mov   dword [edi+0x0c], eax
     | :    0x00c072d8      mov   eax, dword [esp+0x10]
     | :    0x00c072dc      add   ecx, dword [edi+0x08]
     | :    0x00c072df      pop   edi
     | :    0x00c072e0      mov   dword [ecx+0x04], esi
     | :    0x00c072e3      mov   dword [ecx], 0x3e                    ; '>'
     | :                                                               ; [0x3e:4]=-1 ; 62
     | :    0x00c072e9      mov   eax, dword [eax]
     | :    0x00c072eb      pop   esi
     | :    0x00c072ec      mov   dword [ecx+0x08], eax
     | :    0x00c072ef      pop   ebx
     | :    0x00c072f0      ret   0x08
     `----> 0x00c072f3      cmp   eax, edx
       `==< 0x00c072f5      jz    0xc072c3
            0x00c072f7      mov   ecx, dword [esp+0x10]
            0x00c072fb      pop   edi
            0x00c072fc      pop   esi
            0x00c072fd      pop   ebx
            0x00c072fe      mov   ecx, dword [ecx]
            0x00c07300      mov   dword [eax+0x08], ecx
            0x00c07303      ret   0x08
            0x00c07306      int3
            0x00c07307      int3
            0x00c07308      int3
            0x00c07309      int3
            0x00c0730a      int3
            0x00c0730b      int3
            0x00c0730c      int3
            0x00c0730d      int3
            0x00c0730e      int3
            0x00c0730f      int3
            0x00c07310      push  ebx
            0x00c07311      push  esi
            0x00c07312      mov   esi, ecx
            0x00c07314      push  edi
            0x00c07315      mov   edi, dword [esp+0x14]
            0x00c07319      mov   ebx, dword [esi+0x0c]
            0x00c0731c      mov   eax, dword [esi+0x08]
            0x00c0731f      invalid
