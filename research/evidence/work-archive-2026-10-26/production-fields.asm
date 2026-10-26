            0x00c06c20      push  ebx
            0x00c06c21      push  esi
            0x00c06c22      mov   esi, dword [esp+0x0c]
            0x00c06c26      mov   ebx, ecx
            0x00c06c28      push  edi
            0x00c06c29      push  dword [esp+0x14]
            0x00c06c2d      push  esi
            0x00c06c2e      call  0xb53df0
            0x00c06c33      push  0x00
            0x00c06c35      lea   eax, dword [ebx+0x08]
            0x00c06c38      lea   edi, dword [esi+0x14]
            0x00c06c3b      push  eax
            0x00c06c3c      mov   ecx, edi
            0x00c06c3e      call  0xb074c0
            0x00c06c43      xor   eax, eax
            0x00c06c45      lea   ecx, dword [ebx+0x0c]
            0x00c06c48      test  edi, edi
            0x00c06c4a      cmovz esi, eax
            0x00c06c4d      push  dword [esi+0x0c]
            0x00c06c50      push  esi
            0x00c06c51      call  0xbd01e0
            0x00c06c56      lea   eax, dword [ebx+0x1c]
            0x00c06c59      mov   ecx, edi
            0x00c06c5b      push  eax
            0x00c06c5c      call  0xc061f0
            0x00c06c61      push  0x00
            0x00c06c63      lea   eax, dword [ebx+0x68]
            0x00c06c66      mov   ecx, edi
            0x00c06c68      push  eax
            0x00c06c69      call  0xa75940
            0x00c06c6e      mov   esi, edi
            0x00c06c70      lea   eax, dword [edi-0x14]
            0x00c06c73      neg   esi
            0x00c06c75      push  0x04                                 ; 4
            0x00c06c77      sbb   esi, esi
            0x00c06c79      and   esi, eax
            0x00c06c7b      lea   eax, dword [ebx+0x6c]
            0x00c06c7e      push  eax
            0x00c06c7f      mov   ecx, esi
            0x00c06c81      call  0xb5abf0
            0x00c06c86      push  0x04                                 ; 4
            0x00c06c88      lea   eax, dword [ebx+0x70]
            0x00c06c8b      mov   ecx, esi
            0x00c06c8d      push  eax
            0x00c06c8e      call  0xb5abf0
            0x00c06c93      lea   eax, dword [ebx+0x74]
            0x00c06c96      mov   ecx, edi
            0x00c06c98      push  eax
            0x00c06c99      call  0xc06070
            0x00c06c9e      push  0x04                                 ; 4
            0x00c06ca0      lea   eax, dword [esp+0x18]
            0x00c06ca4      mov   dword [esp+0x18], 0x00
            0x00c06cac      push  eax
            0x00c06cad      mov   ecx, esi
            0x00c06caf      call  0xb5abf0
            0x00c06cb4      mov   eax, dword [esp+0x14]
            0x00c06cb8      mov   ecx, esi
            0x00c06cba      mov   dword [ebx+0x90], eax
            0x00c06cc0      lea   eax, dword [ebx+0x94]
            0x00c06cc6      push  0x01                                 ; 1
            0x00c06cc8      push  eax
            0x00c06cc9      call  0xb5abf0
            0x00c06cce      push  0x01                                 ; 1
            0x00c06cd0      lea   eax, dword [ebx+0x95]
            0x00c06cd6      mov   ecx, esi
            0x00c06cd8      push  eax
            0x00c06cd9      call  0xb5abf0
            0x00c06cde      push  dword [esp+0x14]
            0x00c06ce2      lea   eax, dword [ebx+0x98]
            0x00c06ce8      mov   ecx, edi
            0x00c06cea      push  eax
            0x00c06ceb      call  0xc069a0
            0x00c06cf0      push  0x01                                 ; 1
            0x00c06cf2      lea   eax, dword [ebx+0x96]
            0x00c06cf8      mov   ecx, esi
            0x00c06cfa      push  eax
            0x00c06cfb      call  0xb5abf0
            0x00c06d00      pop   edi
            0x00c06d01      pop   esi
            0x00c06d02      pop   ebx
            0x00c06d03      ret   0x08
            0x00c06d06      int3
            0x00c06d07      int3
            0x00c06d08      int3
            0x00c06d09      int3
            0x00c06d0a      int3
            0x00c06d0b      int3
            0x00c06d0c      int3
            0x00c06d0d      int3
            0x00c06d0e      int3
            0x00c06d0f      int3
            0x00c06d10      push  ebx
            0x00c06d11      push  esi
            0x00c06d12      mov   esi, dword [esp+0x10]
            0x00c06d16      mov   ebx, ecx
            0x00c06d18      push  edi
            0x00c06d19      mov   edi, dword [esp+0x10]
            0x00c06d1d      push  esi
            0x00c06d1e      push  edi
            0x00c06d1f      call  0xab4330
            0x00c06d24      mov   ecx, dword [ebx+0x2c]
            0x00c06d27      push  esi
            0x00c06d28      push  edi
            0x00c06d29      mov   eax, dword [ecx]
            0x00c06d2b      call  dword [eax+0x08]                     ; 8
            0x00c06d2e      push  0x04                                 ; 4
            0x00c06d30      lea   eax, dword [esp+0x18]
            0x00c06d34      mov   dword [esp+0x18], 0x00
            0x00c06d3c      lea   esi, dword [edi+0x14]
            0x00c06d3f      push  eax
            0x00c061f0      sub   esp, 0x14
            0x00c061f3      push  ebx
            0x00c061f4      push  ebp
            0x00c061f5      push  esi
            0x00c061f6      mov   esi, ecx
            0x00c061f8      mov   dword [esp+0x0c], 0x00
            0x00c06200      push  edi
            0x00c06201      neg   ecx
            0x00c06203      lea   eax, dword [esp+0x10]
            0x00c06207      push  0x04                                 ; 4
            0x00c06209      push  eax
            0x00c0620a      lea   eax, dword [esi-0x14]
            0x00c0620d      sbb   ecx, ecx
            0x00c0620f      and   ecx, eax
            0x00c06211      call  0xb5abf0
            0x00c06216      mov   ebx, dword [esp+0x28]
            0x00c0621a      mov   edi, dword [esp+0x10]
            0x00c0621e      mov   ecx, dword [ebx+0x44]
            0x00c06221      cmp   edi, ecx
        ,=< 0x00c06223      jb    0xc06283
        |   0x00c06225      mov   ebp, 0x04
        |   0x00c0622a      cmp   ecx, ebp
       ,==< 0x00c0622c      jnb   0xc0624f
       ||   0x00c0622e      mov   eax, ecx
       ||   0x00c06230      lea   edx, dword [ebx+0x0c]
       ||   0x00c06233      shl   eax, 0x04
       ||   0x00c06236      add   edx, eax
      .---> 0x00c06238      mov   eax, ebp
      :||   0x00c0623a      cmp   edi, eax
      :||   0x00c0623c      cmovb eax, edi
      :||   0x00c0623f      cmp   ecx, eax
     ,====< 0x00c06241      jnb   0xc0624f
     |:||   0x00c06243      mov   dword [edx], 0x00
     |:||   0x00c06249      inc   ecx
     |:||   0x00c0624a      add   edx, 0x10                            ; 16
     |`===< 0x00c0624d      jmp   0xc06238
     `-`--> 0x00c0624f      cmp   edi, ebp
       ,==< 0x00c06251      jbe   0xc06283
       ||   0x00c06253      push  edi
       ||   0x00c06254      mov   ecx, ebx
       ||   0x00c06256      call  0xc10f70
       ||   0x00c0625b      cmp   dword [ebx+0x44], ebp
       ||   0x00c0625e      cmovnbe ebp, dword [ebx+0x44]
       ||   0x00c06262      cmp   ebp, edi
      ,===< 0x00c06264      jnb   0xc06283
      |||   0x00c06266      lea   ecx, dword [ebp-0x04]
      |||   0x00c06269      mov   edx, edi
      |||   0x00c0626b      shl   ecx, 0x04
      |||   0x00c0626e      sub   edx, ebp
     .----> 0x00c06270      mov   eax, dword [ebx+0x40]
     :|||   0x00c06273      lea   ecx, dword [ecx+0x10]
     :|||   0x00c06276      mov   dword [eax+ecx*1-0x04], 0x00
     :|||   0x00c0627e      sub   edx, 0x01
     `====< 0x00c06281      jnz   0xc06270
      ```-> 0x00c06283      xor   eax, eax
            0x00c06285      mov   dword [ebx+0x44], edi
            0x00c06288      mov   dword [esp+0x14], eax
            0x00c0628c      cmp   dword [esp+0x10], eax
        ,=< 0x00c06290      jbe   0xc06320
        |   0x00c06296      mov   edx, 0xffffffc0                      ; 4294967232
        |   0x00c0629b      lea   ecx, dword [ebx+0x40]
        |   0x00c0629e      mov   dword [esp+0x18], edx
        |   0x00c062a2      mov   dword [esp+0x20], ecx
       .--> 0x00c062a6      cmp   eax, 0x04                            ; 4
       :|   0x00c062a9      mov   eax, ecx
      ,===< 0x00c062ab      jb    0xc062af
      |:|   0x00c062ad      mov   eax, dword [ecx]
      `---> 0x00c062af      add   eax, edx
       :|   0x00c062b1      mov   ebx, 0x03
       :|   0x00c062b6      mov   dword [esp+0x1c], eax
       :|   0x00c062ba      mov   edi, eax
       :|   0x00c062bc      nop   dword [eax], eax
      .---> 0x00c062c0      mov   ecx, esi
      ::|   0x00c062c2      lea   eax, dword [esi-0x14]
      ::|   0x00c062c5      neg   ecx
      ::|   0x00c062c7      lea   ebp, dword [esi-0x14]
      ::|   0x00c062ca      push  0x04                                 ; 4
      ::|   0x00c062cc      sbb   ecx, ecx
      ::|   0x00c062ce      push  edi
      ::|   0x00c062cf      and   ecx, eax
      ::|   0x00c062d1      call  0xb5abf0
      ::|   0x00c062d6      add   edi, 0x04
      ::|   0x00c062d9      sub   ebx, 0x01
      `===< 0x00c062dc      jnz   0xc062c0
       :|   0x00c062de      push  0x04                                 ; 4
       :|   0x00c062e0      lea   eax, dword [esp+0x2c]
       :|   0x00c062e4      mov   dword [esp+0x2c], ebx
       :|   0x00c062e8      push  eax
       :|   0x00c062e9      xor   eax, eax
       :|   0x00c062eb      test  esi, esi
       :|   0x00c062ed      cmovz ebp, eax
       :|   0x00c062f0      mov   ecx, ebp
       :|   0x00c062f2      call  0xb5abf0
       :|   0x00c062f7      mov   ecx, dword [esp+0x1c]
       :|   0x00c062fb      mov   eax, dword [esp+0x28]
       :|   0x00c062ff      mov   edx, dword [esp+0x18]
       :|   0x00c06303      add   edx, 0x10                            ; 16
       :|   0x00c06306      mov   dword [ecx+0x0c], eax
       :|   0x00c06309      mov   eax, dword [esp+0x14]
       :|   0x00c0630d      mov   ecx, dword [esp+0x20]
       :|   0x00c06311      inc   eax
       :|   0x00c06312      mov   dword [esp+0x14], eax
       :|   0x00c06316      mov   dword [esp+0x18], edx
       :|   0x00c0631a      cmp   eax, dword [esp+0x10]
       `==< 0x00c0631e      jb    0xc062a6
        `-> 0x00c06320      lea   eax, dword [esi-0x14]
            0x00c06323      neg   esi
            0x00c06325      pop   edi
            0x00c06326      sbb   esi, esi
            0x00c06328      and   eax, esi
            0x00c0632a      pop   esi
            0x00c0632b      pop   ebp
            0x00c0632c      pop   ebx
            0x00c0632d      add   esp, 0x14
            0x00c06330      ret   0x04
            0x00c06333      int3
            0x00c06334      int3
            0x00c06335      int3
            0x00c06336      int3
            0x00c06337      int3
            0x00c06338      int3
            0x00c06339      int3
            0x00c0633a      int3
            0x00c0633b      int3
            0x00c0633c      int3
            0x00c0633d      int3
            0x00c0633e      int3
            0x00c0633f      int3
            0x00c06340      sub   esp, 0x14
            0x00c06343      push  ebx
            0x00c06344      push  ebp
            0x00c06345      push  esi
            0x00c06346      mov   esi, dword [esp+0x24]
            0x00c0634a      lea   edx, dword [esp+0x14]
            0x00c0634e      mov   ebp, ecx
            0x00c06350      test  ebp, ebp
            0x00c06352      mov   dword [esp+0x1c], ebp
            0x00c06356      push  0x04                                 ; 4
            0x00c06358      mov   eax, dword [esi+0x44]
            0x00c0635b      mov   dword [esp+0x18], eax
            0x00c0635f      lea   ebx, dword [ebp+0x08]
            0x00c06362      mov   eax, 0x18                            ; 24
            0x00c06367      cmovz ebx, eax
            0x00c0636a      push  edx
            0x00c0636b      mov   ecx, dword [ebx]
            0x00c0636d      mov   eax, dword [ecx]
            0x00c0636f      call  dword [eax+0x1c]                     ; 28
            0x00c06372      xor   eax, eax
            0x00c06374      mov   dword [esp+0x0c], eax
            0x00c06378      cmp   dword [esi+0x44], eax
        ,=< 0x00c0637b      jbe   0xc063f6
        |   0x00c0637d      mov   ecx, 0xffffffc0                      ; 4294967232
        |   0x00c06382      lea   ebp, dword [esi+0x40]
        |   0x00c06385      mov   dword [esp+0x10], ecx
        |   0x00c06389      push  edi
        |   0x00c0638a      nop   word [eax+eax*1], ax
       .--> 0x00c06390      cmp   eax, 0x04                            ; 4
       :|   0x00c06393      mov   eax, ebp
      ,===< 0x00c06395      jb    0xc0639a
      |:|   0x00c06397      mov   eax, dword [ebp]
      `---> 0x00c0639a      lea   edi, dword [ecx+eax*1]
       :|   0x00c0639d      xor   esi, esi
       :|   0x00c0639f      nop
      .---> 0x00c063a0      mov   ecx, dword [ebx]
      ::|   0x00c063a2      lea   edx, dword [esp+0x1c]
      ::|   0x00c063a6      movss xmm0, dword [edi+esi*4]
      ::|   0x00c063ab      movss dword [esp+0x1c], xmm0
      ::|   0x00c063b1      push  0x04                                 ; 4
      ::|   0x00c063b3      mov   eax, dword [ecx]
      ::|   0x00c063b5      push  edx
      ::|   0x00c063b6      call  dword [eax+0x1c]                     ; 28
      ::|   0x00c063b9      inc   esi
      ::|   0x00c063ba      cmp   esi, 0x03                            ; 3
      `===< 0x00c063bd      jnz   0xc063a0
       :|   0x00c063bf      mov   ecx, dword [ebx]
       :|   0x00c063c1      lea   edx, dword [esp+0x1c]
       :|   0x00c063c5      mov   eax, dword [edi+0x0c]
       :|   0x00c063c8      mov   dword [esp+0x1c], eax
       :|   0x00c063cc      push  0x04                                 ; 4
       :|   0x00c063ce      mov   eax, dword [ecx]
       :|   0x00c063d0      push  edx
       :|   0x00c063d1      call  dword [eax+0x1c]                     ; 28
       :|   0x00c063d4      mov   eax, dword [esp+0x10]
       :|   0x00c063d8      mov   edx, dword [esp+0x28]
       :|   0x00c063dc      inc   eax
       :|   0x00c063dd      mov   ecx, dword [esp+0x14]
       :|   0x00c063e1      add   ecx, 0x10                            ; 16
       :|   0x00c063e4      mov   dword [esp+0x10], eax
       :|   0x00c063e8      mov   dword [esp+0x14], ecx
       :|   0x00c063ec      cmp   eax, dword [edx+0x44]
       `==< 0x00c063ef      jb    0xc06390
        |   0x00c063f1      mov   ebp, dword [esp+0x20]
        |   0x00c063f5      pop   edi
        `-> 0x00c063f6      lea   eax, dword [ebp-0x10]
            0x00c063f9      neg   ebp
            0x00c063fb      pop   esi
            0x00c063fc      sbb   ebp, ebp
            0x00c063fe      and   eax, ebp
            0x00c06400      pop   ebp
            0x00c06401      pop   ebx
            0x00c06402      add   esp, 0x14
            0x00c06405      ret   0x04
            0x00c06408      int3
            0x00c06409      int3
            0x00c0640a      int3
            0x00c0640b      int3
            0x00c0640c      int3
            0x00c0640d      int3
            0x00c0640e      int3
            0x00c0640f      int3
            0x00c06410      sub   esp, 0x14
            0x00c06413      mov   edx, dword [ecx]
            0x00c06415      mov   eax, 0x0e                            ; 0xe ; 14
            0x00c0641a      shr   edx, 0x1b
            0x00c0641d      push  ebx
            0x00c0641e      push  ebp
            0x00c0641f      mov   ebp, dword [ecx+0x04]
            0x00c06422      push  esi
            0x00c06423      lea   esi, dword [edx-0x01]
            0x00c06426      mov   dword [esp+0x14], ebp
            0x00c0642a      cmp   esi, eax
            0x00c0642c      lea   ecx, dword [edx-0x01]
            0x00c0642f      push  edi
            0x00c06430      mov   ebx, esi
            0x00c06432      mov   edi, 0x01
            0x00c06437      cmovb ebx, eax
            0x00c0643a      mov   eax, edi
            0x00c0643c      shl   eax, cl
            0x00c0643e      invalid
            0x00c0643f      invalid
            0x00b53df0      push  ebp
            0x00b53df1      mov   ebp, esp
            0x00b53df3      push  0xffffffff                           ; 255
            0x00b53df5      push  0x184d3f8
            0x00b53dfa      mov   eax, dword fs:[0x0]
            0x00b53e00      push  eax
            0x00b53e01      sub   esp, 0x2c
            0x00b53e04      push  esi
            0x00b53e05      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b53e0a      xor   eax, ebp
            0x00b53e0c      push  eax
            0x00b53e0d      lea   eax, dword [ebp-0x0c]
            0x00b53e10      mov   dword fs:[0x0], eax
            0x00b53e16      mov   esi, ecx
            0x00b53e18      push  dword [ebp+0x08]
            0x00b53e1b      lea   ecx, dword [ebp-0x38]
            0x00b53e1e      call  0xb57f80
            0x00b53e23      push  0x04                                 ; 4
            0x00b53e25      lea   eax, dword [ebp+0x08]
            0x00b53e28      mov   dword [ebp-0x04], 0x00
            0x00b53e2f      push  eax
            0x00b53e30      lea   ecx, dword [ebp-0x38]
            0x00b53e33      mov   dword [ebp+0x08], 0x00
            0x00b53e3a      call  0xb5abf0
            0x00b53e3f      mov   eax, dword [ebp+0x08]
            0x00b53e42      lea   ecx, dword [ebp-0x38]
            0x00b53e45      mov   dword [esi+0x04], eax
            0x00b53e48      call  0xb589a0
            0x00b53e4d      mov   ecx, dword [ebp-0x0c]
            0x00b53e50      mov   dword fs:[0x0], ecx
            0x00b53e57      pop   ecx
            0x00b53e58      pop   esi
            0x00b53e59      mov   esp, ebp
            0x00b53e5b      pop   ebp
            0x00b53e5c      ret   0x08
            0x00b53e5f      int3
            0x00b53e60      push  ebp
            0x00b53e61      mov   ebp, esp
            0x00b53e63      push  0xffffffff                           ; 255
            0x00b53e65      push  0x184d368
            0x00b53e6a      mov   eax, dword fs:[0x0]
            0x00b53e70      push  eax
            0x00b53e71      sub   esp, 0x1c
            0x00b53e74      push  esi
            0x00b53e75      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b53e7a      xor   eax, ebp
            0x00b53e7c      push  eax
            0x00b53e7d      lea   eax, dword [ebp-0x0c]
            0x00b53e80      mov   dword fs:[0x0], eax
            0x00b53e86      mov   esi, ecx
            0x00b53e88      push  dword [ebp+0x08]
            0x00b53e8b      lea   ecx, dword [ebp-0x28]
            0x00b53e8e      call  0xb58330
            0x00b53e93      mov   ecx, dword [ebp-0x10]
            0x00b53e96      lea   edx, dword [ebp+0x08]
            0x00b53e99      mov   eax, dword [esi+0x04]
            0x00b53e9c      mov   dword [ebp+0x08], eax
            0x00b53e9f      push  0x04                                 ; 4
            0x00b53ea1      mov   eax, dword [ecx]
            0x00b53ea3      push  edx
            0x00b53ea4      mov   dword [ebp-0x04], 0x00
            0x00b53eab      call  dword [eax+0x1c]                     ; 28
            0x00b53eae      lea   ecx, dword [ebp-0x28]
            0x00b53eb1      call  0xb589c0
            0x00b53eb6      mov   ecx, dword [ebp-0x0c]
            0x00b53eb9      mov   dword fs:[0x0], ecx
            0x00b53ec0      pop   ecx
            0x00b53ec1      pop   esi
            0x00b53ec2      mov   esp, ebp
            0x00b53ec4      pop   ebp
            0x00b53ec5      ret   0x08
            0x00b53ec8      int3
            0x00b53ec9      int3
            0x00b53eca      int3
            0x00b53ecb      int3
            0x00b53ecc      int3
            0x00b53ecd      int3
            0x00b53ece      int3
            0x00b53ecf      int3
            0x00b53ed0      push  ecx
            0x00b53ed1      mov   eax, dword [ecx+0x04]
            0x00b53ed4      mov   dword [esp], eax
            0x00b53ed7      lea   eax, dword [esp]
            0x00b53eda      push  0x04                                 ; 4
            0x00b53edc      push  eax
            0x00b53edd      mov   eax, dword [esp+0x10]
            0x00b53ee1      lea   ecx, dword [eax+0x10]
            0x00b53ee4      neg   ecx
            0x00b53ee6      sbb   ecx, ecx
            0x00b53ee8      and   ecx, eax
            0x00b53eea      call  0xb5ae20
            0x00b53eef      pop   ecx
            0x00b53ef0      ret   0x08
            0x00b53ef3      int3
            0x00b53ef4      int3
            0x00b53ef5      int3
            0x00b53ef6      int3
            0x00b53ef7      int3
            0x00b53ef8      int3
            0x00b53ef9      int3
            0x00b53efa      int3
            0x00b53efb      int3
            0x00b53efc      int3
            0x00b53efd      int3
            0x00b53efe      int3
            0x00b53eff      int3
            0x00b53f00      push  ebp
            0x00b53f01      mov   ebp, esp
            0x00b53f03      push  0xffffffff                           ; 255
            0x00b53f05      push  0x184d3f8
            0x00b53f0a      mov   eax, dword fs:[0x0]
            0x00b53f10      push  eax
            0x00b53f11      sub   esp, 0x2c
            0x00b53f14      push  esi
            0x00b53f15      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b53f1a      xor   eax, ebp
            0x00b53f1c      push  eax
            0x00b53f1d      lea   eax, dword [ebp-0x0c]
            0x00b53f20      mov   dword fs:[0x0], eax
            0x00b53f26      mov   esi, ecx
            0x00b53f28      push  dword [ebp+0x08]
            0x00b53f2b      lea   ecx, dword [ebp-0x38]
            0x00b53f2e      call  0xb580a0
            0x00b53f33      push  0x04                                 ; 4
            0x00b53f35      lea   eax, dword [ebp+0x08]
            0x00b53f38      mov   dword [ebp-0x04], 0x00
            0x00b53f3f      push  eax
            0x00b53f40      lea   ecx, dword [ebp-0x38]
            0x00b53f43      mov   dword [ebp+0x08], 0x00
            0x00b53f4a      call  0xb5abf0
            0x00b53f4f      mov   eax, dword [ebp+0x08]
            0x00b53f52      lea   ecx, dword [ebp-0x38]
            0x00b53f55      mov   dword [esi+0x04], eax
            0x00b53f58      call  0xb589a0
            0x00b53f5d      mov   ecx, dword [ebp-0x0c]
            0x00b53f60      mov   dword fs:[0x0], ecx
            0x00b53f67      pop   ecx
            0x00b53f68      pop   esi
            0x00b53f69      mov   esp, ebp
            0x00b53f6b      pop   ebp
            0x00b53f6c      ret   0x08
            0x00b53f6f      int3
            0x00b53f70      push  ebp
            0x00b53f71      mov   ebp, esp
            0x00b53f73      push  0xffffffff                           ; 255
            0x00b53f75      push  0x184d3f8
            0x00b53f7a      mov   eax, dword fs:[0x0]
            0x00b53f80      push  eax
            0x00b53f81      sub   esp, 0x2c
            0x00b53f84      push  esi
            0x00b53f85      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b53f8a      xor   eax, ebp
            0x00b53f8c      push  eax
            0x00b53f8d      lea   eax, dword [ebp-0x0c]
            0x00b53f90      mov   dword fs:[0x0], eax
            0x00b53f96      mov   esi, ecx
            0x00b53f98      push  dword [ebp+0x08]
            0x00b53f9b      lea   ecx, dword [ebp-0x38]
            0x00b53f9e      call  0xb581e0
            0x00b53fa3      push  0x04                                 ; 4
            0x00b53fa5      lea   eax, dword [ebp+0x08]
            0x00b53fa8      mov   dword [ebp-0x04], 0x00
            0x00b53faf      push  eax
            0x00b53fb0      lea   ecx, dword [ebp-0x38]
            0x00b53fb3      mov   dword [ebp+0x08], 0x00
            0x00b53fba      call  0xb5abf0
            0x00b53fbf      mov   eax, dword [ebp+0x08]
            0x00b53fc2      lea   ecx, dword [ebp-0x38]
            0x00b53fc5      mov   dword [esi+0x04], eax
            0x00b53fc8      call  0xb589a0
            0x00b53fcd      mov   ecx, dword [ebp-0x0c]
            0x00b53fd0      mov   dword fs:[0x0], ecx
            0x00b53fd7      pop   ecx
            0x00b53fd8      pop   esi
            0x00b53fd9      mov   esp, ebp
            0x00b53fdb      pop   ebp
            0x00b53fdc      ret   0x08
            0x00b53fdf      int3
            0x00b53fe0      push  ebp
            0x00b53fe1      mov   ebp, esp
            0x00b53fe3      push  0xffffffff                           ; 255
            0x00b53fe5      push  0x184d3f8
            0x00b53fea      mov   eax, dword fs:[0x0]
            0x00b53ff0      push  eax
            0x00b53ff1      sub   esp, 0x2c
            0x00b53ff4      push  esi
            0x00b53ff5      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b53ffa      xor   eax, ebp
            0x00b53ffc      push  eax
            0x00b53ffd      lea   eax, dword [ebp-0x0c]
            0x00b54000      mov   dword fs:[0x0], eax
            0x00b54006      mov   esi, ecx
            0x00b54008      push  dword [ebp+0x08]
            0x00b5400b      lea   ecx, dword [ebp-0x38]
            0x00b5400e      call  0xb581e0
            0x00b54013      push  dword [ebp+0x0c]
            0x00b54016      lea   eax, dword [ebp-0x38]
            0x00b54019      mov   dword [ebp-0x04], 0x00
            0x00b54020      push  eax
            0x00b54021      mov   ecx, esi
            0x00b54023      call  0xb4c170
            0x00b54028      lea   ecx, dword [ebp-0x38]
            0x00b5402b      call  0xb589a0
            0x00b074c0      sub   esp, 0x0c
            0x00b074c3      push  esi
            0x00b074c4      push  0x04                                 ; 4
            0x00b074c6      lea   eax, dword [esp+0x0c]
            0x00b074ca      mov   dword [esp+0x0c], 0x00
            0x00b074d2      push  eax
            0x00b074d3      lea   eax, dword [ecx-0x14]
            0x00b074d6      neg   ecx
            0x00b074d8      sbb   ecx, ecx
            0x00b074da      and   ecx, eax
            0x00b074dc      call  0xb5abf0
            0x00b074e1      lea   eax, dword [esp+0x07]
            0x00b074e5      push  eax
            0x00b074e6      push  dword [esp+0x0c]
            0x00b074ea      lea   ecx, dword [esp+0x14]
            0x00b074ee      call  0x4f7950
            0x00b074f3      mov   esi, dword [eax]
            0x00b074f5      call  0x512430
            0x00b074fa      cmp   esi, dword [eax]
        ,=< 0x00b074fc      jz    0xb0751f
        |   0x00b074fe      mov   eax, dword [0x201e2d8]               ; [0x201e2d8:4]=0
        |   0x00b07503      push  0x00
        |   0x00b07505      mov   ecx, dword [eax+0x54]
        |   0x00b07508      push  ecx
        |   0x00b07509      mov   eax, esp
        |   0x00b0750b      mov   dword [eax], esi
        |   0x00b0750d      call  0xae5730
        |   0x00b07512      mov   ecx, dword [esp+0x14]
        |   0x00b07516      mov   dword [ecx], eax
        |   0x00b07518      pop   esi
        |   0x00b07519      add   esp, 0x0c
        |   0x00b0751c      ret   0x08
        `-> 0x00b0751f      mov   eax, dword [esp+0x14]
            0x00b07523      pop   esi
            0x00b07524      mov   dword [eax], 0x00
            0x00b0752a      add   esp, 0x0c
            0x00b0752d      ret   0x08
            0x00b07530      push  esi
            0x00b07531      call  0xb04970
            0x00b07536      mov   ecx, dword [0x203a2a0]               ; [0x203a2a0:4]=0
            0x00b0753c      mov   esi, eax
            0x00b0753e      cmp   byte [ecx+0x80], 0x00
        ,=< 0x00b07545      jnz   0xb07553
        |   0x00b07547      push  0x00
        |   0x00b07549      push  0x04                                 ; 4
        |   0x00b0754b      call  0xb078b0
        |   0x00b07550      add   esp, 0x08
        `-> 0x00b07553      push  dword [esp+0x0c]
            0x00b07557      mov   ecx, esi
            0x00b07559      push  dword [esp+0x0c]
            0x00b0755d      push  0xb079b0
            0x00b07562      call  0x56d330
            0x00b07567      pop   esi
            0x00b07568      ret
            0x00b07569      int3
            0x00b0756a      int3
            0x00b0756b      int3
            0x00b0756c      int3
            0x00b0756d      int3
            0x00b0756e      int3
            0x00b0756f      int3
            0x00b07570      push  esi
            0x00b07571      call  0xb04a20
            0x00b07576      mov   ecx, dword [0x203a2a0]               ; [0x203a2a0:4]=0
            0x00b0757c      mov   esi, eax
            0x00b0757e      cmp   byte [ecx+0x80], 0x00
        ,=< 0x00b07585      jnz   0xb07593
        |   0x00b07587      push  0x00
        |   0x00b07589      push  0x04                                 ; 4
        |   0x00b0758b      call  0xb078b0
        |   0x00b07590      add   esp, 0x08
        `-> 0x00b07593      push  dword [esp+0x0c]
            0x00b07597      mov   ecx, esi
            0x00b07599      push  dword [esp+0x0c]
            0x00b0759d      push  0xb079e0
            0x00b075a2      call  0x56d330
            0x00b075a7      pop   esi
            0x00b075a8      ret
            0x00b075a9      int3
            0x00b075aa      int3
            0x00b075ab      int3
            0x00b075ac      int3
            0x00b075ad      int3
            0x00b075ae      int3
            0x00b075af      int3
            0x00b075b0      push  esi
            0x00b075b1      call  0xb04ad0
            0x00b075b6      mov   ecx, dword [0x203a7fc]               ; [0x203a7fc:4]=0
            0x00b075bc      mov   esi, eax
            0x00b075be      cmp   byte [ecx+0x80], 0x00
        ,=< 0x00b075c5      jnz   0xb075d3
        |   0x00b075c7      push  0x00
        |   0x00b075c9      push  0x04                                 ; 4
        |   0x00b075cb      call  0xb07930
        |   0x00b075d0      add   esp, 0x08
        `-> 0x00b075d3      push  dword [esp+0x0c]
            0x00b075d7      mov   ecx, esi
            0x00b075d9      push  dword [esp+0x0c]
            0x00b075dd      push  0xb07a10
            0x00b075e2      call  0x56d330
            0x00b075e7      pop   esi
            0x00b075e8      ret
            0x00b075e9      int3
            0x00b075ea      int3
            0x00b075eb      int3
            0x00b075ec      int3
            0x00b075ed      int3
            0x00b075ee      int3
            0x00b075ef      int3
            0x00b075f0      push  esi
            0x00b075f1      call  0xb04b80
            0x00b075f6      mov   ecx, dword [0x203a7fc]               ; [0x203a7fc:4]=0
            0x00b075fc      mov   esi, eax
            0x00b075fe      invalid
            0x00b075ff      invalid
            0x00bd01e0      push  ebp
            0x00bd01e1      mov   ebp, esp
            0x00bd01e3      push  0xffffffff                           ; 255
            0x00bd01e5      push  0x184d3f8
            0x00bd01ea      mov   eax, dword fs:[0x0]
            0x00bd01f0      push  eax
            0x00bd01f1      sub   esp, 0x2c
            0x00bd01f4      push  esi
            0x00bd01f5      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00bd01fa      xor   eax, ebp
            0x00bd01fc      push  eax
            0x00bd01fd      lea   eax, dword [ebp-0x0c]
            0x00bd0200      mov   dword fs:[0x0], eax
            0x00bd0206      mov   esi, ecx
            0x00bd0208      push  dword [ebp+0x08]
            0x00bd020b      lea   ecx, dword [ebp-0x38]
            0x00bd020e      call  0xb57f80
            0x00bd0213      push  0x00
            0x00bd0215      push  esi
            0x00bd0216      lea   ecx, dword [ebp-0x24]
            0x00bd0219      mov   dword [ebp-0x04], 0x00
            0x00bd0220      call  0xa66fc0
            0x00bd0225      push  0x00
            0x00bd0227      lea   eax, dword [esi+0x04]
            0x00bd022a      push  eax
            0x00bd022b      lea   ecx, dword [ebp-0x24]
            0x00bd022e      call  0xa66fc0
            0x00bd0233      push  0x00
            0x00bd0235      lea   eax, dword [esi+0x08]
            0x00bd0238      push  eax
            0x00bd0239      lea   ecx, dword [ebp-0x24]
            0x00bd023c      call  0xa66fc0
            0x00bd0241      push  0x04                                 ; 4
            0x00bd0243      lea   eax, dword [esi+0x0c]
            0x00bd0246      push  eax
            0x00bd0247      lea   ecx, dword [ebp-0x38]
            0x00bd024a      call  0xb5abf0
            0x00bd024f      lea   ecx, dword [ebp-0x38]
            0x00bd0252      call  0xb589a0
            0x00bd0257      mov   ecx, dword [ebp-0x0c]
            0x00bd025a      mov   dword fs:[0x0], ecx
            0x00bd0261      pop   ecx
            0x00bd0262      pop   esi
            0x00bd0263      mov   esp, ebp
            0x00bd0265      pop   ebp
            0x00bd0266      ret   0x08
            0x00bd0269      int3
            0x00bd026a      int3
            0x00bd026b      int3
            0x00bd026c      int3
            0x00bd026d      int3
            0x00bd026e      int3
            0x00bd026f      int3
            0x00bd0270      push  ebp
            0x00bd0271      mov   ebp, esp
            0x00bd0273      push  0xffffffff                           ; 255
            0x00bd0275      push  0x184d368
            0x00bd027a      mov   eax, dword fs:[0x0]
            0x00bd0280      push  eax
            0x00bd0281      sub   esp, 0x1c
            0x00bd0284      push  esi
            0x00bd0285      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00bd028a      xor   eax, ebp
            0x00bd028c      push  eax
            0x00bd028d      lea   eax, dword [ebp-0x0c]
            0x00bd0290      mov   dword fs:[0x0], eax
            0x00bd0296      mov   esi, ecx
            0x00bd0298      push  dword [ebp+0x08]
            0x00bd029b      lea   ecx, dword [ebp-0x28]
            0x00bd029e      call  0xb58330
            0x00bd02a3      push  0x00
            0x00bd02a5      push  dword [esi]
            0x00bd02a7      lea   ecx, dword [ebp-0x18]
            0x00bd02aa      mov   dword [ebp-0x04], 0x00
            0x00bd02b1      call  0xa69870
            0x00bd02b6      push  0x00
            0x00bd02b8      push  dword [esi+0x04]
            0x00bd02bb      lea   ecx, dword [ebp-0x18]
            0x00bd02be      call  0xa69870
            0x00bd02c3      push  0x00
            0x00bd02c5      push  dword [esi+0x08]
            0x00bd02c8      lea   ecx, dword [ebp-0x18]
            0x00bd02cb      call  0xa69870
            0x00bd02d0      mov   ecx, dword [ebp-0x10]
            0x00bd02d3      lea   edx, dword [ebp+0x08]
            0x00bd02d6      mov   eax, dword [esi+0x0c]
            0x00bd02d9      mov   dword [ebp+0x08], eax
            0x00bd02dc      push  0x04                                 ; 4
            0x00bd02de      mov   eax, dword [ecx]
            0x00bd02e0      push  edx
            0x00bd02e1      call  dword [eax+0x1c]                     ; 28
            0x00bd02e4      lea   ecx, dword [ebp-0x28]
            0x00bd02e7      call  0xb589c0
            0x00bd02ec      mov   ecx, dword [ebp-0x0c]
            0x00bd02ef      mov   dword fs:[0x0], ecx
            0x00bd02f6      pop   ecx
            0x00bd02f7      pop   esi
            0x00bd02f8      mov   esp, ebp
            0x00bd02fa      pop   ebp
            0x00bd02fb      ret   0x08
            0x00bd02fe      int3
            0x00bd02ff      int3
            0x00bd0300      push  esi
            0x00bd0301      push  edi
            0x00bd0302      mov   edi, dword [esp+0x0c]
            0x00bd0306      mov   esi, ecx
            0x00bd0308      push  0x00
            0x00bd030a      add   edi, 0x10                            ; 16
            0x00bd030d      mov   ecx, edi
            0x00bd030f      push  dword [esi]
            0x00bd0311      call  0xa69920
            0x00bd0316      push  0x00
            0x00bd0318      push  dword [esi+0x04]
            0x00bd031b      mov   ecx, edi
            0x00bd031d      call  0xa69920
            0x00bd0322      push  0x00
            0x00bd0324      push  dword [esi+0x08]
            0x00bd0327      mov   ecx, edi
            0x00bd0329      call  0xa69920
            0x00bd032e      mov   eax, dword [esi+0x0c]
            0x00bd0331      lea   ecx, dword [edi-0x10]
            0x00bd0334      neg   edi
            0x00bd0336      mov   dword [esp+0x0c], eax
            0x00bd033a      push  0x04                                 ; 4
            0x00bd033c      lea   eax, dword [esp+0x10]
            0x00bd0340      sbb   edi, edi
            0x00bd0342      push  eax
            0x00bd0343      and   ecx, edi
            0x00bd0345      call  0xb5ae20
            0x00bd034a      pop   edi
            0x00bd034b      pop   esi
            0x00bd034c      ret   0x08
            0x00bd034f      int3
            0x00bd0350      mov   byte [ecx+0x9d], 0x00
            0x00bd0357      ret
            0x00bd0358      int3
            0x00bd0359      int3
            0x00bd035a      int3
            0x00bd035b      int3
            0x00bd035c      int3
            0x00bd035d      int3
            0x00bd035e      int3
            0x00bd035f      int3
            0x00bd0360      push  ebp
            0x00bd0361      mov   ebp, esp
            0x00bd0363      push  0xffffffff                           ; 255
            0x00bd0365      push  0x186f298
            0x00bd036a      mov   eax, dword fs:[0x0]
            0x00b5abf0      push  ebp
            0x00b5abf1      lea   ebp, dword [esp-0x28]
            0x00b5abf5      sub   esp, 0x28
            0x00b5abf8      push  0xffffffff                           ; 255
            0x00b5abfa      push  0x186c372
            0x00b5abff      mov   eax, dword fs:[0x0]
            0x00b5ac05      push  eax
            0x00b5ac06      sub   esp, 0x98
            0x00b5ac0c      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b5ac11      xor   eax, ebp
            0x00b5ac13      mov   dword [ebp+0x24], eax
            0x00b5ac16      push  esi
            0x00b5ac17      push  edi
            0x00b5ac18      push  eax
            0x00b5ac19      lea   eax, dword [ebp-0x0c]
            0x00b5ac1c      mov   dword fs:[0x0], eax
            0x00b5ac22      mov   esi, ecx
            0x00b5ac24      mov   edx, dword [ebp+0x30]
            0x00b5ac27      mov   edi, dword [ebp+0x34]
            0x00b5ac2a      mov   dword [ebp], 0x00
            0x00b5ac31      cmp   byte [esi+0x10], 0x00
        ,=< 0x00b5ac35      jnz   0xb5adfd
        |   0x00b5ac3b      lea   eax, dword [ebp+0x04]
        |   0x00b5ac3e      mov   dword [ebp+0x04], 0x00
        |   0x00b5ac45      push  eax
        |   0x00b5ac46      push  edi
        |   0x00b5ac47      lea   ecx, dword [esi+0x18]
        |   0x00b5ac4a      push  edx
        |   0x00b5ac4b      call  0x51d1e0
        |   0x00b5ac50      cmp   dword [ebp+0x04], 0x00
       ,==< 0x00b5ac54      jz    0xb5adfd
       ||   0x00b5ac5a      cmp   byte [esi+0x11], 0x00
       ||   0x00b5ac5e      mov   byte [esi+0x10], 0x01
      ,===< 0x00b5ac62      jnz   0xb5adfd
      |||   0x00b5ac68      lea   ecx, dword [ebp-0x54]
      |||   0x00b5ac6b      mov   dword [ebp-0xa4], 0x1929534
      |||   0x00b5ac75      call  dword [sym.imp.MSVCP140.dll_protected:_void___thiscall_std::basic_ios_char__struct_std::char_traits_char__::constructor_void] ; 0x1914458 ; "N\x99\x96\U00000001\U00000014\x99\x96\U00000001Ԙ\x96\U00000001\x9e\x98\x96\U00000001X\x98\x96\U00000001\U00000010\x98\x96\U0000"
      |||   0x00b5ac7b      push  0x00
      |||   0x00b5ac7d      push  0x00
      |||   0x00b5ac7f      lea   eax, dword [ebp-0xa0]
      |||   0x00b5ac85      mov   dword [ebp-0x04], 0x00
      |||   0x00b5ac8c      push  eax
      |||   0x00b5ac8d      lea   ecx, dword [ebp-0xa4]
      |||   0x00b5ac93      mov   dword [ebp], 0x01
      |||   0x00b5ac9a      call  dword [sym.imp.MSVCP140.dll_public:_void___thiscall_std::basic_ostream_char__struct_std::char_traits_char__::constructor_class_std::basic_streambuf_char__struct_std::char_traits_char______bool] ; 0x1914444 ; "t\x9a\x96\U00000001<\x9a\x96\U00000001\xfe\x99\x96\U00000001\xbc\x99\x96\U00000001\x84\x99\x96\U00000001N\x99\x96\U00000001\U000"
      |||   0x00b5aca0      mov   eax, dword [ebp-0xa4]
      |||   0x00b5aca6      mov   dword [ebp-0x04], 0x02
      |||   0x00b5acad      mov   eax, dword [eax+0x04]
      |||   0x00b5acb0      mov   dword [ebp+eax*1-0xa4], 0x1929528
      |||   0x00b5acbb      mov   eax, dword [ebp-0xa4]
      |||   0x00b5acc1      mov   ecx, dword [eax+0x04]
      |||   0x00b5acc4      lea   eax, dword [ecx-0x50]
      |||   0x00b5acc7      mov   dword [ebp+ecx*1-0xa8], eax
      |||   0x00b5acce      lea   ecx, dword [ebp-0xa0]
      |||   0x00b5acd4      call  dword [sym.imp.MSVCP140.dll_protected:_void___thiscall_std::basic_streambuf_char__struct_std::char_traits_char__::constructor_void] ; 0x1914494
      |||   0x00b5acda      mov   eax, dword [ebp-0xa4]
      |||   0x00b5ace0      mov   dword [ebp-0xa0], 0x19294e8
      |||   0x00b5acea      mov   dword [ebp-0x68], 0x00
      |||   0x00b5acf1      mov   dword [ebp-0x64], 0x04
      |||   0x00b5acf8      mov   eax, dword [eax+0x04]
      |||   0x00b5acfb      mov   dword [ebp+eax*1-0xa4], 0x1929530
      |||   0x00b5ad06      mov   eax, dword [ebp-0xa4]
      |||   0x00b5ad0c      mov   ecx, dword [eax+0x04]
      |||   0x00b5ad0f      lea   eax, dword [ecx-0x50]
      |||   0x00b5ad12      mov   dword [ebp+ecx*1-0xa8], eax
      |||   0x00b5ad19      lea   eax, dword [ebp-0xa4]
      |||   0x00b5ad1f      invalid
0x019b0180  0x00c091b0 0x00c0fac0 0x00c0f850 0x00c0f980  ........P.......
0x019b0190  0x00c0fad0 0x00c0fb40 0x00c0fbb0 0x00c0fb40  ....@.......@...
0x019b01a0  0x00c0cd90 0x00c0de10 0x00c09820 0x0051dbd0  ........ .....Q.
0x019b01b0  0x01bae7a0 0x00c090d0 0x00c0f480 0x00c0f300  ................
0x019b01c0  0x00c0f3c0 0x00c0f530 0x00c0f5a0 0x00c0f610  ....0...........
0x019b01d0  0x00c0f5a0 0x00c0ccf0 0x00c0ddd0 0x00c095d0  ................
0x019b01e0  0x0051dbd0 0x00000000 0x61206e55 0x6e6f6976  ..Q.....Un avion
0x019b01f0  0x65206120 0x63206574 0x20656572 0x736e6164   a ete cree dans
