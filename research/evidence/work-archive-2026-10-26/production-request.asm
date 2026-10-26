            0x00c0b190      push  ebp
            0x00c0b191      mov   ebp, esp
            0x00c0b193      push  0xffffffff                           ; 255
            0x00c0b195      push  0x18765d7
            0x00c0b19a      mov   eax, dword fs:[0x0]
            0x00c0b1a0      push  eax
            0x00c0b1a1      sub   esp, 0x17c
            0x00c0b1a7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0b1ac      xor   eax, ebp
            0x00c0b1ae      mov   dword [ebp-0x10], eax
            0x00c0b1b1      push  esi
            0x00c0b1b2      push  edi
            0x00c0b1b3      push  eax
            0x00c0b1b4      lea   eax, dword [ebp-0x0c]
            0x00c0b1b7      mov   dword fs:[0x0], eax
            0x00c0b1bd      mov   edi, ecx
            0x00c0b1bf      mov   eax, dword [ebp+0x08]
            0x00c0b1c2      mov   dword [ebp-0x138], eax
            0x00c0b1c8      mov   eax, dword [ebp+0x10]
            0x00c0b1cb      mov   dword [ebp-0x134], eax
            0x00c0b1d1      mov   eax, dword [ebp+0x14]
            0x00c0b1d4      mov   dword [ebp-0x130], eax
            0x00c0b1da      mov   eax, dword [0x201e2d8]               ; [0x201e2d8:4]=0
            0x00c0b1df      mov   dword [ebp-0x14], eax
            0x00c0b1e2      mov   eax, dword [edi]
            0x00c0b1e4      mov   eax, dword [eax+0x20]
            0x00c0b1e7      call  eax
            0x00c0b1e9      mov   esi, dword [ebp+0x0c]
            0x00c0b1ec      lea   ecx, dword [edi+0x1c]
            0x00c0b1ef      mov   dword [ebp-0x13c], eax
            0x00c0b1f5      cmp   esi, 0x04                            ; 4
        ,=< 0x00c0b1f8      jnb   0xc0b203
        |   0x00c0b1fa      mov   eax, esi
        |   0x00c0b1fc      shl   eax, 0x04
        |   0x00c0b1ff      add   eax, ecx
       ,==< 0x00c0b201      jmp   0xc0b20c
       |`-> 0x00c0b203      lea   eax, dword [esi-0x04]
       |    0x00c0b206      shl   eax, 0x04
       |    0x00c0b209      add   eax, dword [ecx+0x40]
       `--> 0x00c0b20c      movss xmm0, dword [eax]
            0x00c0b210      movss dword [ebp-0x38], xmm0
            0x00c0b215      movss xmm0, dword [eax+0x04]
            0x00c0b21a      movss dword [ebp-0x34], xmm0
            0x00c0b21f      movss xmm0, dword [eax+0x08]
            0x00c0b224      movss dword [ebp-0x30], xmm0
            0x00c0b229      mov   eax, dword [eax+0x0c]
            0x00c0b22c      cmp   eax, 0x02                            ; 2
            0x00c0b22f      mov   dword [ebp-0x2c], eax
            0x00c0b232      mov   eax, dword [edi+0x90]
            0x00c0b238      setz  byte [ebp-0x101]
            0x00c0b23f      mov   dword [ebp-0x28], 0x3f800000
            0x00c0b246      mov   dword [ebp-0x24], 0x00
            0x00c0b24d      mov   dword [ebp-0x20], 0x00
            0x00c0b254      cmp   eax, 0x02                            ; 2
        ,=< 0x00c0b257      jnz   0xc0b3ae
        |   0x00c0b25d      mov   ecx, dword [ebp-0x14]
        |   0x00c0b260      mov   dword [ebp-0x12c], eax
        |   0x00c0b266      mov   esi, dword [ecx+0x38]
        |   0x00c0b269      lea   ecx, dword [edi+0x0c]
        |   0x00c0b26c      call  0xbcf930
        |   0x00c0b271      push  eax
        |   0x00c0b272      call  0xcc08a0
        |   0x00c0b277      add   esp, 0x04
        |   0x00c0b27a      mov   byte [ebp-0x14], al
        |   0x00c0b27d      lea   ecx, dword [edi+0x0c]
        |   0x00c0b280      call  0xbcf930
        |   0x00c0b285      mov   edx, dword [edi+0x08]
        |   0x00c0b288      lea   ecx, dword [ebp-0x12c]
        |   0x00c0b28e      push  ecx
        |   0x00c0b28f      push  dword [ebp-0x14]
        |   0x00c0b292      add   edx, 0x20                            ; 32
        |   0x00c0b295      mov   ecx, esi
        |   0x00c0b297      push  eax
        |   0x00c0b298      push  edx
        |   0x00c0b299      lea   eax, dword [ebp-0x38]
        |   0x00c0b29c      push  eax
        |   0x00c0b29d      lea   eax, dword [ebp-0x44]
        |   0x00c0b2a0      push  eax
        |   0x00c0b2a1      call  0xaa31e0
        |   0x00c0b2a6      mov   dword [ebp-0x1c], 0x7f800000
        |   0x00c0b2ad      xor   ecx, ecx
        |   0x00c0b2af      mov   dword [ebp-0x18], 0x7f800000
        |   0x00c0b2b6      mov   dword [ebp-0x14], 0x7f800000
        |   0x00c0b2bd      nop   dword [eax], eax
       .--> 0x00c0b2c0      movss xmm0, dword [ebp+ecx*1-0x44]
       :|   0x00c0b2c6      ucomiss xmm0, dword [ebp+ecx*1-0x1c]
       :|   0x00c0b2cb      lahf
       :|   0x00c0b2cc      test  ah, 0x44                             ; 68
      ,===< 0x00c0b2cf      jp    0xc0b2e0
      |:|   0x00c0b2d1      add   ecx, 0x04
      |:|   0x00c0b2d4      cmp   ecx, 0x0c                            ; 0xc ; 12
      |`==< 0x00c0b2d7      jb    0xc0b2c0
      | |   0x00c0b2d9      xor   eax, eax
      |,==< 0x00c0b2db      jmp   0xc0be9a
      `---> 0x00c0b2e0      cmp   dword [ebp-0x12c], 0x02
       ||   0x00c0b2e7      mov   ecx, dword [edi+0x0c]
       ||   0x00c0b2ea      setz  byte [ebp-0x101]
       ||   0x00c0b2f1      call  0xb9e1d0
       ||   0x00c0b2f6      mov   esi, dword [ebp+0x0c]
       ||   0x00c0b2f9      test  byte [eax], 0x10
      ,===< 0x00c0b2fc      jnz   0xc0b40b
      |||   0x00c0b302      movss xmm3, dword [ebp-0x38]
      |||   0x00c0b307      movss xmm5, dword [ebp-0x34]
      |||   0x00c0b30c      movss xmm1, dword [ebp-0x40]
      |||   0x00c0b311      movss xmm2, dword [ebp-0x44]
      |||   0x00c0b316      subss xmm5, xmm1
      |||   0x00c0b31a      movss xmm4, dword [ebp-0x30]
      |||   0x00c0b31f      subss xmm3, xmm2
      |||   0x00c0b323      movss xmm0, dword [ebp-0x3c]
      |||   0x00c0b328      subss xmm4, xmm0
      |||   0x00c0b32c      movss dword [ebp-0x30], xmm0
      |||   0x00c0b331      movss dword [ebp-0x34], xmm1
      |||   0x00c0b336      movaps xmm1, xmm5
      |||   0x00c0b339      movss dword [ebp-0x24], xmm5
      |||   0x00c0b33e      movaps xmm0, xmm3
      |||   0x00c0b341      mulss xmm1, xmm5
      |||   0x00c0b345      mulss xmm0, xmm3
      |||   0x00c0b349      movss dword [ebp-0x28], xmm3
      |||   0x00c0b34e      movss dword [ebp-0x20], xmm4
      |||   0x00c0b353      addss xmm1, xmm0
      |||   0x00c0b357      movss dword [ebp-0x38], xmm2
      |||   0x00c0b35c      movaps xmm0, xmm4
      |||   0x00c0b35f      mulss xmm0, xmm4
      |||   0x00c0b363      addss xmm1, xmm0
      |||   0x00c0b367      xorps xmm0, xmm0
      |||   0x00c0b36a      ucomiss xmm1, xmm0
      |||   0x00c0b36d      lahf
      |||   0x00c0b36e      test  ah, 0x44                             ; 68
     ,====< 0x00c0b371      jnp   0xc0b40b
     ||||   0x00c0b377      movaps xmm0, xmm1
     ||||   0x00c0b37a      movss xmm1, dword [0x1933890]              ; [0x1933890:4]=0x3f800000
     ||||   0x00c0b382      sqrtss xmm0, xmm0
     ||||   0x00c0b386      divss xmm1, xmm0
     ||||   0x00c0b38a      movaps xmm0, xmm1
     ||||   0x00c0b38d      mulss xmm3, xmm1
     ||||   0x00c0b391      mulss xmm0, xmm5
     ||||   0x00c0b395      mulss xmm4, xmm1
     ||||   0x00c0b399      unpcklps xmm3, xmm0
     ||||   0x00c0b39c      movq  qword [ebp-0x28], xmm3
     ||||   0x00c0b3a1      movss dword [ebp-0x3c], xmm4
     ||||   0x00c0b3a6      mov   eax, dword [ebp-0x3c]
     ||||   0x00c0b3a9      mov   dword [ebp-0x20], eax
    ,=====< 0x00c0b3ac      jmp   0xc0b40b
    ||||`-> 0x00c0b3ae      cmp   eax, 0x01                            ; 1
    ||||,=< 0x00c0b3b1      jnz   0xc0b40b
    |||||   0x00c0b3b3      mov   ecx, dword [ebp-0x14]
    |||||   0x00c0b3b6      call  0xab0f80
    |||||   0x00c0b3bb      lea   ecx, dword [ebp-0x38]
    |||||   0x00c0b3be      push  ecx
    |||||   0x00c0b3bf      lea   ecx, dword [ebp-0x18]
    |||||   0x00c0b3c2      push  ecx
    |||||   0x00c0b3c3      mov   ecx, eax
    |||||   0x00c0b3c5      call  0xbcdd20
    |||||   0x00c0b3ca      mov   edx, eax
    |||||   0x00c0b3cc      xor   ecx, ecx
    |||||   0x00c0b3ce      nop
   .------> 0x00c0b3d0      cmp   ecx, 0x03                            ; 3
  ,=======< 0x00c0b3d3      jnb   0xc0b3f0
  |:|||||   0x00c0b3d5      mov   eax, dword [edx+ecx*4]
  |:|||||   0x00c0b3d8      mov   dword [ebp+ecx*4-0x44], eax
  |:|||||   0x00c0b3dc      inc   ecx
  |:|||||   0x00c0b3dd      cmp   ecx, 0x02                            ; 2
  |`======< 0x00c0b3e0      jb    0xc0b3d0
  | |||||   0x00c0b3e2      nop   dword [eax], eax
  | |||||   0x00c0b3e6      nop   word [eax+eax*1], ax
  `-------> 0x00c0b3f0      movss xmm0, dword [ebp-0x44]
    |||||   0x00c0b3f5      movss dword [ebp-0x28], xmm0
    |||||   0x00c0b3fa      movss xmm0, dword [ebp-0x40]
    |||||   0x00c0b3ff      movss dword [ebp-0x24], xmm0
    |||||   0x00c0b404      mov   dword [ebp-0x20], 0x00
    ```-`-> 0x00c0b40b      lea   ecx, dword [ebp-0x124]
       |    0x00c0b411      call  0x4f6c50
       |    0x00c0b416      lea   ecx, dword [ebp-0x48]
       |    0x00c0b419      mov   dword [ebp-0x04], 0x00
       |    0x00c0b420      call  0x598730
       |    0x00c0b425      push  0xffffffff                           ; 255
       |    0x00c0b427      lea   eax, dword [ebp-0x38]
       |    0x00c0b42a      mov   byte [ebp-0x04], 0x01
       |    0x00c0b42e      push  eax
       |    0x00c0b42f      lea   ecx, dword [ebp-0x48]
       |    0x00c0b432      call  0xaf5040
       |    0x00c0b437      push  0xffffffff                           ; 255
       |    0x00c0b439      lea   eax, dword [ebp-0x28]
       |    0x00c0b43c      push  eax
       |    0x00c0b43d      lea   ecx, dword [ebp-0x48]
       |    0x00c0b440      call  0xaf5150
       |    0x00c0b445      lea   eax, dword [edi+0x18]
       |    0x00c0b448      push  0xffffffff                           ; 255
       |    0x00c0b44a      push  eax
       |    0x00c0b44b      lea   ecx, dword [ebp-0x48]
       |    0x00c0b44e      call  0xaf51e0
       |    0x00c0b453      lea   eax, dword [edi+0x6c]
       |    0x00c0b456      push  0xffffffff                           ; 255
       |    0x00c0b458      push  eax
       |    0x00c0b459      lea   ecx, dword [ebp-0x48]
       |    0x00c0b45c      call  0xaf5260
       |    0x00c0b461      cmp   esi, 0x04                            ; 4
       |,=< 0x00c0b464      jnb   0xc0b46e
       ||   0x00c0b466      lea   eax, dword [edi+0x74]
       ||   0x00c0b469      lea   eax, dword [eax+esi*4]
      ,===< 0x00c0b46c      jmp   0xc0b47a
      ||`-> 0x00c0b46e      mov   eax, dword [edi+0x84]
      ||    0x00c0b474      lea   eax, dword [eax+esi*4]
      ||    0x00c0b477      add   eax, 0xfffffff0                      ; 4294967280
      `---> 0x00c0b47a      push  0xffffffff                           ; 255
       |    0x00c0b47c      push  eax
       |    0x00c0b47d      lea   ecx, dword [ebp-0x48]
       |    0x00c0b480      call  0xc07290
       |    0x00c0b485      push  0xffffffff                           ; 255
       |    0x00c0b487      lea   eax, dword [ebp-0x14]
       |    0x00c0b48a      mov   dword [ebp-0x14], 0x00
       |    0x00c0b491      push  eax
       |    0x00c0b492      lea   ecx, dword [ebp-0x48]
       |    0x00c0b495      call  0xaf53e0
       |    0x00c0b49a      mov   eax, dword [edi+0x08]
       |    0x00c0b49d      lea   ecx, dword [ebp-0x48]
       |    0x00c0b4a0      push  0xffffffff                           ; 255
       |    0x00c0b4a2      add   eax, 0x20                            ; 32
       |    0x00c0b4a5      push  eax
       |    0x00c0b4a6      call  0xaf50d0
       |    0x00c0b4ab      push  0xffffffff                           ; 255
       |    0x00c0b4ad      push  dword [edi+0x10]
       |    0x00c0b4b0      lea   ecx, dword [ebp-0x48]
       |    0x00c0b4b3      call  0xc07310
       |    0x00c0b4b8      mov   edx, dword [ebp-0x3c]
       |    0x00c0b4bb      mov   eax, dword [edi+0x14]
       |    0x00c0b4be      imul  ecx, edx, 0xb4
       |    0x00c0b4c4      mov   dword [ebp-0x14], eax
       |    0x00c0b4c7      mov   eax, dword [ebp-0x40]
       |    0x00c0b4ca      mov   dword [ebp-0x12c], edx
       |    0x00c0b4d0      add   ecx, eax
       |    0x00c0b4d2      cmp   eax, ecx
       |,=< 0x00c0b4d4      jz    0xc0b4ee
       ||   0x00c0b4d6      cmp   dword [eax], 0x6a                    ; 'j'
      ,===< 0x00c0b4d9      jnz   0xc0b4e1
      |||   0x00c0b4db      cmp   dword [eax+0x04], 0xffffffff
      |||   0x00c0b4df      invalid
            0x00bcf930      mov   eax, dword [ecx+0x08]
            0x00bcf933      test  eax, eax
        ,=< 0x00bcf935      jnz   0xbcf940
        |   0x00bcf937      mov   eax, dword [ecx+0x04]
        |   0x00bcf93a      test  eax, eax
       ,==< 0x00bcf93c      jnz   0xbcf940
       ||   0x00bcf93e      mov   eax, dword [ecx]
       ``-> 0x00bcf940      ret
            0x00bcf941      int3
            0x00bcf942      int3
            0x00bcf943      int3
            0x00bcf944      int3
            0x00bcf945      int3
            0x00bcf946      int3
            0x00bcf947      int3
            0x00bcf948      int3
            0x00bcf949      int3
            0x00bcf94a      int3
            0x00bcf94b      int3
            0x00bcf94c      int3
            0x00bcf94d      int3
            0x00bcf94e      int3
            0x00bcf94f      int3
            0x00bcf950      sub   esp, 0x08
            0x00bcf953      push  ebx
            0x00bcf954      push  ebp
            0x00bcf955      push  esi
            0x00bcf956      push  edi
            0x00bcf957      push  0x01                                 ; 1
            0x00bcf959      mov   ebx, ecx
            0x00bcf95b      call  0xbb77d0
            0x00bcf960      mov   eax, dword [ebx+0x18]
            0x00bcf963      mov   edx, dword [ebx+0x0c]
            0x00bcf966      and   edx, 0x7ffffff
            0x00bcf96c      mov   ebp, dword [eax+0x0c]
            0x00bcf96f      mov   eax, dword [ebx+0x10]
            0x00bcf972      mov   esi, eax
            0x00bcf974      lea   edi, dword [eax+edx*8]
            0x00bcf977      cmp   esi, edi
        ,=< 0x00bcf979      jz    0xbcf9dd
        |   0x00bcf97b      nop   dword [eax+eax*1], eax
       .--> 0x00bcf980      mov   ecx, dword [ebx+0x08]
       :|   0x00bcf983      push  0x01                                 ; 1
       :|   0x00bcf985      push  ebp
       :|   0x00bcf986      push  dword [esi]
       :|   0x00bcf988      call  0x954010
       :|   0x00bcf98d      mov   ecx, dword [ebx+0x08]
       :|   0x00bcf990      lea   eax, dword [esp+0x10]
       :|   0x00bcf994      push  eax
       :|   0x00bcf995      push  dword [esi]
       :|   0x00bcf997      mov   dword [esp+0x18], 0x00
       :|   0x00bcf99f      call  0x95dea0
       :|   0x00bcf9a4      movzx eax, byte [0x20274ca]                ; [0x20274ca:1]=0
       :|   0x00bcf9ab      mov   ecx, dword [ebx+0x08]
       :|   0x00bcf9ae      mov   byte [esp+0x14], al
       :|   0x00bcf9b2      mov   eax, dword [0x20274c8]               ; [0x20274c8:4]=0
       :|   0x00bcf9b7      mov   byte [esp+0x15], ah
       :|   0x00bcf9bb      mov   byte [esp+0x16], al
       :|   0x00bcf9bf      movzx eax, byte [0x20274cb]                ; [0x20274cb:1]=0
       :|   0x00bcf9c6      mov   byte [esp+0x17], al
       :|   0x00bcf9ca      lea   eax, dword [esp+0x14]
       :|   0x00bcf9ce      push  eax
       :|   0x00bcf9cf      push  dword [esi]
       :|   0x00bcf9d1      call  0x95de50
       :|   0x00bcf9d6      add   esi, 0x08
       :|   0x00bcf9d9      cmp   esi, edi
       `==< 0x00bcf9db      jnz   0xbcf980
        `-> 0x00bcf9dd      pop   edi
            0x00bcf9de      pop   esi
            0x00bcf9df      pop   ebp
            0x00bcf9e0      pop   ebx
            0x00bcf9e1      add   esp, 0x08
            0x00bcf9e4      ret
            0x00bcf9e5      int3
            0x00bcf9e6      int3
            0x00bcf9e7      int3
            0x00bcf9e8      int3
            0x00bcf9e9      int3
            0x00bcf9ea      int3
            0x00bcf9eb      int3
            0x00bcf9ec      int3
            0x00bcf9ed      int3
            0x00bcf9ee      int3
            0x00bcf9ef      int3
            0x00bcf9f0      push  esi
            0x00bcf9f1      call  0xbcd0a0
            0x00bcf9f6      mov   ecx, dword [0x203d9c4]               ; [0x203d9c4:4]=0
            0x00bcf9fc      mov   esi, eax
            0x00bcf9fe      cmp   byte [ecx+0x80], 0x00
        ,=< 0x00bcfa05      jnz   0xbcfa13
        |   0x00bcfa07      push  0x00
        |   0x00bcfa09      push  0x04                                 ; 4
        |   0x00bcfa0b      call  0xc02080
        |   0x00bcfa10      add   esp, 0x08
        `-> 0x00bcfa13      push  dword [esp+0x0c]
            0x00bcfa17      mov   ecx, esi
            0x00bcfa19      push  dword [esp+0x0c]
            0x00bcfa1d      push  0xbcfab0
            0x00bcfa22      call  0x56d330
            0x00bcfa27      pop   esi
            0x00bcfa28      ret
            0x00bcfa29      int3
            0x00bcfa2a      int3
            0x00bcfa2b      int3
            0x00bcfa2c      int3
            0x00bcfa2d      int3
            0x00bcfa2e      int3
            0x00bcfa2f      int3
            0x00bcfa30      push  esi
            0x00bcfa31      call  0xbcd150
            0x00bcfa36      mov   ecx, dword [0x203cb44]               ; [0x203cb44:4]=0
            0x00bcfa3c      mov   esi, eax
            0x00bcfa3e      cmp   byte [ecx+0x80], 0x00
        ,=< 0x00bcfa45      jnz   0xbcfa53
        |   0x00bcfa47      push  0x00
        |   0x00bcfa49      push  0x04                                 ; 4
        |   0x00bcfa4b      call  0xbb63d0
        |   0x00bcfa50      add   esp, 0x08
        `-> 0x00bcfa53      push  dword [esp+0x0c]
            0x00bcfa57      mov   ecx, esi
            0x00bcfa59      push  dword [esp+0x0c]
            0x00bcfa5d      push  0xbcfb30
            0x00bcfa62      call  0x56d330
            0x00bcfa67      pop   esi
            0x00bcfa68      ret
            0x00bcfa69      int3
            0x00bcfa6a      int3
            0x00bcfa6b      int3
            0x00bcfa6c      int3
            0x00bcfa6d      int3
            0x00bcfa6e      int3
            0x00bcfa6f      int3
            0x00bcfa70      push  esi
            0x00bcfa71      call  0xbcd200
            0x00bcfa76      mov   ecx, dword [0x2003014]               ; [0x2003014:4]=0
            0x00bcfa7c      mov   esi, eax
            0x00bcfa7e      cmp   byte [ecx+0x80], 0x00
        ,=< 0x00bcfa85      jnz   0xbcfa93
        |   0x00bcfa87      push  0x00
        |   0x00bcfa89      push  0x04                                 ; 4
        |   0x00bcfa8b      call  0x564460
        |   0x00bcfa90      add   esp, 0x08
        `-> 0x00bcfa93      push  dword [esp+0x0c]
            0x00bcfa97      mov   ecx, esi
            0x00bcfa99      push  dword [esp+0x0c]
            0x00bcfa9d      invalid
            0x00bcfa9e      invalid
            0x00bcfa9f      cld
            0x00c0ce90      push  ebx
            0x00c0ce91      push  ebp
            0x00c0ce92      push  esi
            0x00c0ce93      push  edi
            0x00c0ce94      push  dword [0x202731c]
            0x00c0ce9a      mov   edi, ecx
            0x00c0ce9c      xor   esi, esi
            0x00c0ce9e      lea   ecx, dword [edi+0x0c]
            0x00c0cea1      call  0xbcdcd0
            0x00c0cea6      mov   ebx, dword [edi+0x70]
            0x00c0cea9      mov   ebp, eax
            0x00c0ceab      xor   eax, eax
            0x00c0cead      test  ebx, ebx
        ,=< 0x00c0ceaf      jz    0xc0ced7
        |   0x00c0ceb1      lea   edx, dword [esi-0x10]
       .--> 0x00c0ceb4      lea   ecx, dword [edi+0x84]
       :|   0x00c0ceba      cmp   eax, 0x04                            ; 4
      ,===< 0x00c0cebd      jb    0xc0cec5
      |:|   0x00c0cebf      mov   ecx, dword [edi+0x84]
      `---> 0x00c0cec5      mov   ecx, dword [edx+ecx*1]
       :|   0x00c0cec8      inc   eax
       :|   0x00c0cec9      imul  ecx, ebp
       :|   0x00c0cecc      add   edx, 0x04
       :|   0x00c0cecf      add   esi, ecx
       :|   0x00c0ced1      cmp   eax, ebx
       `==< 0x00c0ced3      jnz   0xc0ceb4
        |   0x00c0ced5      mov   eax, esi
        `-> 0x00c0ced7      pop   edi
            0x00c0ced8      pop   esi
            0x00c0ced9      pop   ebp
            0x00c0ceda      pop   ebx
            0x00c0cedb      ret
            0x00c0cedc      int3
            0x00c0cedd      int3
            0x00c0cede      int3
            0x00c0cedf      int3
            0x00c0cee0      push  ebp
            0x00c0cee1      mov   ebp, esp
            0x00c0cee3      push  0xffffffff                           ; 255
            0x00c0cee5      push  0x1876798
            0x00c0ceea      mov   eax, dword fs:[0x0]
            0x00c0cef0      push  eax
            0x00c0cef1      sub   esp, 0x3c
            0x00c0cef4      push  ebx
            0x00c0cef5      push  esi
            0x00c0cef6      push  edi
            0x00c0cef7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0cefc      xor   eax, ebp
            0x00c0cefe      push  eax
            0x00c0ceff      lea   eax, dword [ebp-0x0c]
            0x00c0cf02      mov   dword fs:[0x0], eax
            0x00c0cf08      mov   dword [ebp-0x14], ecx
            0x00c0cf0b      mov   eax, dword [ebp+0x08]
            0x00c0cf0e      xor   edx, edx
            0x00c0cf10      xor   ebx, ebx
            0x00c0cf12      mov   dword [ebp-0x44], 0x00
            0x00c0cf19      mov   dword [ebp-0x3c], edx
            0x00c0cf1c      mov   dword [ebp-0x38], ebx
            0x00c0cf1f      mov   byte [eax], 0x01
            0x00c0cf22      mov   dword [ebp-0x04], ebx
            0x00c0cf25      xor   esi, esi
        .-> 0x00c0cf27      mov   edi, dword [ecx+0x44]
        :   0x00c0cf2a      xor   eax, eax
        :   0x00c0cf2c      test  edi, edi
       ,==< 0x00c0cf2e      jz    0xc0cf3f
       |:   0x00c0cf30      mov   ecx, dword [ecx+0x40]
      .---> 0x00c0cf33      cmp   dword [ecx], esi
     ,====< 0x00c0cf35      jz    0xc0cf41
     |:|:   0x00c0cf37      inc   eax
     |:|:   0x00c0cf38      add   ecx, 0x04
     |:|:   0x00c0cf3b      cmp   eax, edi
     |`===< 0x00c0cf3d      jb    0xc0cf33
     | `--> 0x00c0cf3f      mov   eax, edi
     `----> 0x00c0cf41      cmp   eax, edi
       ,==< 0x00c0cf43      jnz   0xc0cf77
       |:   0x00c0cf45      xor   eax, eax
       |:   0x00c0cf47      test  ebx, ebx
      ,===< 0x00c0cf49      jz    0xc0cf60
      ||:   0x00c0cf4b      nop   dword [eax+eax*1], eax
     .----> 0x00c0cf50      cmp   dword [edx+eax*4], esi
    ,=====< 0x00c0cf53      jz    0xc0cf5c
    |:||:   0x00c0cf55      inc   eax
    |:||:   0x00c0cf56      cmp   eax, ebx
    |`====< 0x00c0cf58      jb    0xc0cf50
    |,====< 0x00c0cf5a      jmp   0xc0cf60
    `-----> 0x00c0cf5c      cmp   eax, ebx
    ,=====< 0x00c0cf5e      jnz   0xc0cf77
    |``---> 0x00c0cf60      cmp   ebx, dword [ebp-0x44]
    | ,===< 0x00c0cf63      jnz   0xc0cf70
    | ||:   0x00c0cf65      lea   ecx, dword [ebp-0x48]
    | ||:   0x00c0cf68      call  0x58f930
    | ||:   0x00c0cf6d      mov   edx, dword [ebp-0x3c]
    | `---> 0x00c0cf70      mov   dword [edx+ebx*4], esi
    |  |:   0x00c0cf73      inc   ebx
    |  |:   0x00c0cf74      mov   dword [ebp-0x38], ebx
    `--`--> 0x00c0cf77      mov   ecx, dword [ebp-0x14]
        :   0x00c0cf7a      inc   esi
        :   0x00c0cf7b      cmp   esi, 0x04                            ; 4
        `=< 0x00c0cf7e      jl    0xc0cf27
            0x00c0cf80      push  0x04                                 ; 4
            0x00c0cf82      lea   ecx, dword [ebp-0x34]
            0x00c0cf85      call  0xaf5e10
            0x00c0cf8a      movss xmm0, dword [0x19338f0]              ; [0x19338f0:4]=0xbf800000
            0x00c0cf92      movss dword [ebp-0x10], xmm0
            0x00c0cf97      mov   dword [ebp-0x28], 0x00
            0x00c0cf9e      mov   dword [ebp-0x24], 0x00
            0x00c0cfa5      mov   esi, dword [ebp-0x34]
            0x00c0cfa8      mov   eax, dword [ebp-0x30]
            0x00c0cfab      mov   byte [ebp-0x04], 0x02
            0x00c0cfaf      lea   edi, dword [esi+eax*4]
            0x00c0cfb2      cmp   esi, edi
        ,=< 0x00c0cfb4      jz    0xc0d084
        |   0x00c0cfba      nop   word [eax+eax*1], ax
       .--> 0x00c0cfc0      push  esi
       :|   0x00c0cfc1      call  0xd7ca50
       :|   0x00c0cfc6      mov   edx, eax
       :|   0x00c0cfc8      add   esp, 0x04
       :|   0x00c0cfcb      cmp   edx, 0x03                            ; 3
      ,===< 0x00c0cfce      jz    0xc0d079
      |:|   0x00c0cfd4      xor   ecx, ecx
      |:|   0x00c0cfd6      test  ebx, ebx
     ,====< 0x00c0cfd8      jz    0xc0d079
     ||:|   0x00c0cfde      mov   eax, dword [ebp-0x3c]
    .-----> 0x00c0cfe1      cmp   dword [eax+ecx*4], edx
   ,======< 0x00c0cfe4      jz    0xc0cff0
   |:||:|   0x00c0cfe6      inc   ecx
   |:||:|   0x00c0cfe7      cmp   ecx, ebx
   |`=====< 0x00c0cfe9      jb    0xc0cfe1
   |,=====< 0x00c0cfeb      jmp   0xc0d079
   `------> 0x00c0cff0      cmp   ecx, ebx
   ,======< 0x00c0cff2      jz    0xc0d079
   ||||:|   0x00c0cff8      test  dword [ebp-0x28], 0x7ffffff
  ,=======< 0x00c0cfff      jz    0xc0d03f
  |||||:|   0x00c0d001      mov   eax, dword [esi]
  |||||:|   0x00c0d003      mov   ecx, eax
  |||||:|   0x00c0d005      shl   eax, 0x04
  |||||:|   0x00c0d008      xor   ecx, 0xdeadbeef
  |||||:|   0x00c0d00e      add   ecx, eax
  |||||:|   0x00c0d010      mov   eax, ecx
  |||||:|   0x00c0d012      shr   eax, 0x0a
  |||||:|   0x00c0d015      xor   ecx, eax
  |||||:|   0x00c0d017      mov   eax, ecx
  |||||:|   0x00c0d019      shr   eax, 0x18
  |||||:|   0x00c0d01c      add   eax, ecx
  |||||:|   0x00c0d01e      imul  eax, eax, 0x81
  |||||:|   0x00c0d024      mov   ecx, eax
  |||||:|   0x00c0d026      shr   ecx, 0x0d
  |||||:|   0x00c0d029      xor   ecx, eax
  |||||:|   0x00c0d02b      lea   eax, dword [ebp-0x18]
  |||||:|   0x00c0d02e      push  eax
  |||||:|   0x00c0d02f      push  ecx
  |||||:|   0x00c0d030      push  esi
  |||||:|   0x00c0d031      lea   ecx, dword [ebp-0x28]
  |||||:|   0x00c0d034      call  0x4dc510
  |||||:|   0x00c0d039      cmp   dword [ebp-0x18], 0x00
  ========< 0x00c0d03d      jnz   0xc0d079
  `-------> 0x00c0d03f      mov   ecx, dword [ebp-0x14]
   ||||:|   0x00c0d042      push  esi
   ||||:|   0x00c0d043      call  0xc0d110
   ||||:|   0x00c0d048      push  esi
   ||||:|   0x00c0d049      lea   ecx, dword [ebp-0x28]
   ||||:|   0x00c0d04c      fstp  dword [ebp-0x1c]
   ||||:|   0x00c0d04f      call  0xc07c60
   ||||:|   0x00c0d054      movss xmm0, dword [ebp-0x1c]
   ||||:|   0x00c0d059      comiss xmm0, dword [ebp-0x10]
   ||||:|   0x00c0d05d      mov   dword [eax], 0xffffffff              ; [0xffffffff:4]=-1 ; -1
   ||||:|   0x00c0d063      mov   ecx, dword [esi]
   ||||:|   0x00c0d065      mov   dword [eax], ecx
   ||||:|   0x00c0d067      movss dword [eax+0x04], xmm0
  ,=======< 0x00c0d06c      jbe   0xc0d079
  |||||:|   0x00c0d06e      mov   eax, dword [ebp+0x08]
  |||||:|   0x00c0d071      movss dword [ebp-0x10], xmm0
  |||||:|   0x00c0d076      mov   byte [eax], 0x00
  `````---> 0x00c0d079      add   esi, 0x04
       :|   0x00c0d07c      cmp   esi, edi
       `==< 0x00c0d07e      jnz   0xc0cfc0
        `-> 0x00c0d084      lea   ecx, dword [ebp-0x28]
            0x00c0d087      call  0x902070
            0x00c0d08c      lea   ecx, dword [ebp-0x34]
            0x00c0d08f      invalid
            0x00b245c0      push  ebp
            0x00b245c1      mov   ebp, esp
            0x00b245c3      push  0xffffffff                           ; 255
            0x00b245c5      push  0x18686c8
            0x00b245ca      mov   eax, dword fs:[0x0]
            0x00b245d0      push  eax
            0x00b245d1      sub   esp, 0x1c
            0x00b245d4      push  esi
            0x00b245d5      push  edi
            0x00b245d6      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b245db      xor   eax, ebp
            0x00b245dd      push  eax
            0x00b245de      lea   eax, dword [ebp-0x0c]
            0x00b245e1      mov   dword fs:[0x0], eax
            0x00b245e7      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00b245ec      xor   edi, edi
            0x00b245ee      xor   edx, edx
            0x00b245f0      mov   eax, dword [eax+0xe0]
            0x00b245f6      mov   dword [ebp-0x14], edi
            0x00b245f9      mov   dword [ebp-0x10], edx
            0x00b245fc      mov   ecx, dword [eax*4+0x20286d8]
            0x00b24603      mov   dword [ebp-0x18], ecx
            0x00b24606      test  ecx, ecx
        ,=< 0x00b24608      jz    0xb2461d
        |   0x00b2460a      mov   eax, dword [ecx]
        |   0x00b2460c      push  edx
        |   0x00b2460d      lea   edx, dword [ebp-0x14]
        |   0x00b24610      push  edx
        |   0x00b24611      call  dword [eax+0x3c]                     ; 60
        |   0x00b24614      mov   edx, dword [ebp-0x10]
        |   0x00b24617      mov   edi, dword [ebp-0x14]
        |   0x00b2461a      mov   ecx, dword [ebp-0x18]
        `-> 0x00b2461d      mov   dword [ebp-0x04], 0x00
            0x00b24624      test  ecx, ecx
        ,=< 0x00b24626      jz    0xb24638
        |   0x00b24628      mov   eax, dword [ebp+0x08]
        |   0x00b2462b      movzx eax, word [eax+0x20]
        |   0x00b2462f      cmp   eax, edx
       ,==< 0x00b24631      jnb   0xb24638
       ||   0x00b24633      mov   edi, dword [edi+eax*4]
      ,===< 0x00b24636      jmp   0xb2463a
      |``-> 0x00b24638      xor   edi, edi
      `---> 0x00b2463a      mov   esi, dword [ebp+0x0c]
            0x00b2463d      mov   ecx, esi
            0x00b2463f      call  0xb9ce40
            0x00b24644      push  eax
            0x00b24645      mov   ecx, edi
            0x00b24647      call  0xc182a0
            0x00b2464c      mov   ecx, dword [ebp+0x10]
            0x00b2464f      mov   edi, eax
            0x00b24651      lea   eax, dword [ebp-0x28]
            0x00b24654      mov   dword [ebp-0x1c], ecx
            0x00b24657      push  eax
            0x00b24658      mov   ecx, edi
            0x00b2465a      mov   dword [ebp-0x28], 0x19a1778
            0x00b24661      mov   dword [ebp-0x24], 0x00
            0x00b24668      mov   dword [ebp-0x20], esi
            0x00b2466b      call  0xba90a0
            0x00b24670      mov   eax, dword [ebp-0x24]
            0x00b24673      test  eax, eax
        ,=< 0x00b24675      jz    0xb24692
        |   0x00b24677      push  eax
        |   0x00b24678      mov   ecx, edi
        |   0x00b2467a      call  0xba5990
        |   0x00b2467f      mov   ecx, dword [ebp-0x0c]
        |   0x00b24682      mov   dword fs:[0x0], ecx
        |   0x00b24689      pop   ecx
        |   0x00b2468a      pop   edi
        |   0x00b2468b      pop   esi
        |   0x00b2468c      mov   esp, ebp
        |   0x00b2468e      pop   ebp
        |   0x00b2468f      ret   0x0c
        `-> 0x00b24692      mov   ecx, dword [ebp-0x0c]
            0x00b24695      mov   dword fs:[0x0], ecx
            0x00b2469c      pop   ecx
            0x00b2469d      pop   edi
            0x00b2469e      pop   esi
            0x00b2469f      mov   esp, ebp
            0x00b246a1      pop   ebp
            0x00b246a2      ret   0x0c
            0x00b246a5      int3
            0x00b246a6      int3
            0x00b246a7      int3
            0x00b246a8      int3
            0x00b246a9      int3
            0x00b246aa      int3
            0x00b246ab      int3
            0x00b246ac      int3
            0x00b246ad      int3
            0x00b246ae      int3
            0x00b246af      int3
            0x00b246b0      push  ebp
            0x00b246b1      mov   ebp, esp
            0x00b246b3      push  0xffffffff                           ; 255
            0x00b246b5      push  0x1860bf8
            0x00b246ba      mov   eax, dword fs:[0x0]
            0x00b246c0      push  eax
            0x00b246c1      sub   esp, 0x0c
            0x00b246c4      push  esi
            0x00b246c5      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b246ca      xor   eax, ebp
            0x00b246cc      push  eax
            0x00b246cd      lea   eax, dword [ebp-0x0c]
            0x00b246d0      mov   dword fs:[0x0], eax
            0x00b246d6      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00b246db      xor   edx, edx
            0x00b246dd      xor   esi, esi
            0x00b246df      mov   eax, dword [eax+0xe0]
            0x00b246e5      mov   dword [ebp-0x14], edx
            0x00b246e8      mov   dword [ebp-0x10], esi
            0x00b246eb      mov   ecx, dword [eax*4+0x20286d8]
            0x00b246f2      mov   dword [ebp-0x18], ecx
            0x00b246f5      test  ecx, ecx
        ,=< 0x00b246f7      jz    0xb2470c
        |   0x00b246f9      mov   eax, dword [ecx]
        |   0x00b246fb      lea   edx, dword [ebp-0x14]
        |   0x00b246fe      push  esi
        |   0x00b246ff      push  edx
        |   0x00b24700      call  dword [eax+0x3c]                     ; 60
        |   0x00b24703      mov   esi, dword [ebp-0x10]
        |   0x00b24706      mov   edx, dword [ebp-0x14]
        |   0x00b24709      mov   ecx, dword [ebp-0x18]
        `-> 0x00b2470c      invalid
            0x00b2470d      inc   ebp
            0x00b2470e      cld
            0x00b2470f      invalid
            0x00b2ced0      push  ebp
            0x00b2ced1      mov   ebp, esp
            0x00b2ced3      push  0xffffffff                           ; 255
            0x00b2ced5      push  0x1869098
            0x00b2ceda      mov   eax, dword fs:[0x0]
            0x00b2cee0      push  eax
            0x00b2cee1      sub   esp, 0x20
            0x00b2cee4      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2cee9      xor   eax, ebp
            0x00b2ceeb      mov   dword [ebp-0x10], eax
            0x00b2ceee      push  ebx
            0x00b2ceef      push  esi
            0x00b2cef0      push  edi
            0x00b2cef1      push  eax
            0x00b2cef2      lea   eax, dword [ebp-0x0c]
            0x00b2cef5      mov   dword fs:[0x0], eax
            0x00b2cefb      mov   esi, ecx
            0x00b2cefd      mov   ebx, dword [ebp+0x08]
            0x00b2cf00      lea   eax, dword [esi+0x28]
            0x00b2cf03      mov   edi, dword [ebp+0x0c]
            0x00b2cf06      lea   ecx, dword [ebp-0x24]
            0x00b2cf09      push  eax
            0x00b2cf0a      call  0x4e6c30
            0x00b2cf0f      movss xmm0, dword [esi+0x18]
            0x00b2cf14      sub   esp, 0x14
            0x00b2cf17      mov   eax, dword [esi+0x24]
            0x00b2cf1a      mov   ecx, esp
            0x00b2cf1c      movss dword [ebp-0x1c], xmm0
            0x00b2cf21      movss xmm0, dword [esi+0x1c]
            0x00b2cf26      movss dword [ebp-0x18], xmm0
            0x00b2cf2b      movss xmm0, dword [esi+0x20]
            0x00b2cf30      mov   dword [ebp-0x2c], eax
            0x00b2cf33      mov   eax, dword [esi+0x04]
            0x00b2cf36      movss dword [ebp-0x14], xmm0
            0x00b2cf3b      mov   dword [ecx], eax
            0x00b2cf3d      add   ecx, 0x04
            0x00b2cf40      lea   eax, dword [esi+0x08]
            0x00b2cf43      mov   dword [ebp-0x04], 0x00
            0x00b2cf4a      push  eax
            0x00b2cf4b      call  0x4f70d0
            0x00b2cf50      push  edi
            0x00b2cf51      push  ebx
            0x00b2cf52      call  0xb2e4f0
            0x00b2cf57      add   esp, 0x1c
            0x00b2cf5a      mov   esi, dword [eax+0x124]
            0x00b2cf60      test  esi, esi
        ,=< 0x00b2cf62      jz    0xb2cfc9
        |   0x00b2cf64      lea   eax, dword [ebp-0x24]
        |   0x00b2cf67      push  eax
        |   0x00b2cf68      lea   eax, dword [ebp-0x20]
        |   0x00b2cf6b      push  eax
        |   0x00b2cf6c      call  0x5288e0
        |   0x00b2cf71      add   esp, 0x08
        |   0x00b2cf74      push  0x00
        |   0x00b2cf76      push  0x0a                                 ; 0xa ; 10
        |   0x00b2cf78      lea   ecx, dword [ebp-0x20]
        |   0x00b2cf7b      mov   byte [ebp-0x04], 0x01
        |   0x00b2cf7f      call  0x523620
        |   0x00b2cf84      cmp   eax, 0xffffffff                      ; -1
       ,==< 0x00b2cf87      jz    0xb2cfaf
       ||   0x00b2cf89      push  eax
       ||   0x00b2cf8a      lea   eax, dword [ebp-0x28]
       ||   0x00b2cf8d      push  eax
       ||   0x00b2cf8e      lea   ecx, dword [ebp-0x20]
       ||   0x00b2cf91      call  0x51d390
       ||   0x00b2cf96      push  eax
       ||   0x00b2cf97      lea   ecx, dword [ebp-0x20]
       ||   0x00b2cf9a      mov   byte [ebp-0x04], 0x02
       ||   0x00b2cf9e      call  0x4fcce0
       ||   0x00b2cfa3      lea   ecx, dword [ebp-0x28]
       ||   0x00b2cfa6      mov   byte [ebp-0x04], 0x01
       ||   0x00b2cfaa      call  0x4f94d0
       `--> 0x00b2cfaf      lea   eax, dword [ebp-0x20]
        |   0x00b2cfb2      mov   ecx, esi
        |   0x00b2cfb4      push  eax
        |   0x00b2cfb5      push  dword [ebp-0x2c]
        |   0x00b2cfb8      lea   eax, dword [ebp-0x1c]
        |   0x00b2cfbb      push  eax
        |   0x00b2cfbc      call  0xaa3d00
        |   0x00b2cfc1      lea   ecx, dword [ebp-0x20]
        |   0x00b2cfc4      call  0x4f94d0
        `-> 0x00b2cfc9      lea   ecx, dword [ebp-0x24]
            0x00b2cfcc      call  0x4f94a0
            0x00b2cfd1      mov   ecx, dword [ebp-0x0c]
            0x00b2cfd4      mov   dword fs:[0x0], ecx
            0x00b2cfdb      pop   ecx
            0x00b2cfdc      pop   edi
            0x00b2cfdd      pop   esi
            0x00b2cfde      pop   ebx
            0x00b2cfdf      mov   ecx, dword [ebp-0x10]
            0x00b2cfe2      xor   ecx, ebp
            0x00b2cfe4      call  0x18075f6
            0x00b2cfe9      mov   esp, ebp
            0x00b2cfeb      pop   ebp
            0x00b2cfec      ret   0x08
            0x00b2cfef      int3
            0x00b2cff0      sub   esp, 0x1c
            0x00b2cff3      push  ebx
            0x00b2cff4      push  ebp
            0x00b2cff5      push  esi
            0x00b2cff6      push  edi
            0x00b2cff7      mov   edi, ecx
            0x00b2cff9      push  ecx
            0x00b2cffa      mov   esi, esp
            0x00b2cffc      lea   ecx, dword [esp+0x20]
            0x00b2d000      mov   eax, dword [edi+0x04]
            0x00b2d003      mov   ebx, dword [edi+0x0c]
            0x00b2d006      mov   ebp, dword [edi+0x08]
            0x00b2d009      mov   dword [esp+0x14], eax
            0x00b2d00d      mov   eax, dword [edi+0x10]
            0x00b2d010      mov   dword [esp+0x1c], eax
            0x00b2d014      lea   eax, dword [edi+0x14]
            0x00b2d017      push  eax
            0x00b2d018      call  0x4f70d0
            0x00b2d01d      mov   eax, dword [esp+0x1c]
            0x00b2d021      sub   esp, 0x14
            0x00b2d024      mov   ecx, esp
            0x00b2d026      mov   dword [ecx], eax
            0x00b2d028      lea   eax, dword [esp+0x34]
            0x00b2d02c      push  eax
            0x00b2d02d      add   ecx, 0x04
            0x00b2d030      call  0x4f70d0
            0x00b2d035      push  dword [esp+0x4c]
            0x00b2d039      push  dword [esp+0x4c]
            0x00b2d03d      call  0xb28a70
            0x00b2d042      add   esp, 0x1c
            0x00b2d045      test  eax, eax
        ,=< 0x00b2d047      jz    0xb2d056
        |   0x00b2d049      mov   dword [esi], 0xffffffff              ; [0xffffffff:4]=-1 ; -1
        |   0x00b2d04f      mov   eax, dword [eax+0x20]
        |   0x00b2d052      mov   dword [esi], eax
       ,==< 0x00b2d054      jmp   0xb2d05d
       |`-> 0x00b2d056      mov   ecx, esi
       |    0x00b2d058      call  0x4f6c50
       `--> 0x00b2d05d      push  ebx
            0x00b2d05e      push  ebp
            0x00b2d05f      push  dword [esp+0x1c]
            0x00b2d063      mov   ecx, edi
            0x00b2d065      call  0xcfd2b0
            0x00b2d06a      pop   edi
            0x00b2d06b      pop   esi
            0x00b2d06c      pop   ebp
            0x00b2d06d      pop   ebx
            0x00b2d06e      add   esp, 0x1c
            0x00b2d071      ret   0x08
            0x00b2d074      int3
            0x00b2d075      int3
            0x00b2d076      int3
            0x00b2d077      int3
            0x00b2d078      int3
            0x00b2d079      int3
            0x00b2d07a      int3
            0x00b2d07b      int3
            0x00b2d07c      int3
            0x00b2d07d      int3
            0x00b2d07e      int3
            0x00b2d07f      int3
            0x00b2d080      push  dword [ecx+0x0c]
            0x00b2d083      push  dword [ecx+0x08]
            0x00b2d086      push  dword [ecx+0x04]
            0x00b2d089      call  0xb7a5c0
            0x00b2d08e      ret   0x08
            0x00b2d091      int3
            0x00b2d092      int3
            0x00b2d093      int3
            0x00b2d094      int3
            0x00b2d095      int3
            0x00b2d096      int3
            0x00b2d097      int3
            0x00b2d098      int3
            0x00b2d099      int3
            0x00b2d09a      int3
            0x00b2d09b      int3
            0x00b2d09c      int3
            0x00b2d09d      int3
            0x00b2d09e      int3
            0x00b2d09f      int3
            0x00b2d0a0      push  esi
            0x00b2d0a1      mov   esi, dword [ecx+0x04]
            0x00b2d0a4      mov   ecx, esi
            0x00b2d0a6      mov   eax, dword [esi]
            0x00b2d0a8      mov   eax, dword [eax+0x24]
            0x00b2d0ab      call  eax
            0x00b2d0ad      test  al, al
        ,=< 0x00b2d0af      jz    0xb2d0cc
        |   0x00b2d0b1      mov   eax, dword [esi]
        |   0x00b2d0b3      mov   ecx, esi
        |   0x00b2d0b5      call  dword [eax+0x20]                     ; 32
        |   0x00b2d0b8      push  0x00
        |   0x00b2d0ba      push  0x00
        |   0x00b2d0bc      push  esi
        |   0x00b2d0bd      mov   ecx, eax
        |   0x00b2d0bf      call  0xba5520
        |   0x00b2d0c4      mov   eax, dword [esi]
        |   0x00b2d0c6      mov   ecx, esi
        |   0x00b2d0c8      push  0x01                                 ; 1
        |   0x00b2d0ca      call  dword [eax]
        `-> 0x00b2d0cc      pop   esi
            0x00b2d0cd      ret   0x08
            0x00b2c6c0      push  ebp
            0x00b2c6c1      lea   ebp, dword [esp-0x64]
            0x00b2c6c5      sub   esp, 0x64
            0x00b2c6c8      push  0xffffffff                           ; 255
            0x00b2c6ca      push  0x1868f4e
            0x00b2c6cf      mov   eax, dword fs:[0x0]
            0x00b2c6d5      push  eax
            0x00b2c6d6      sub   esp, 0xb4
            0x00b2c6dc      push  ebx
            0x00b2c6dd      push  esi
            0x00b2c6de      push  edi
            0x00b2c6df      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2c6e4      xor   eax, ebp
            0x00b2c6e6      push  eax
            0x00b2c6e7      lea   eax, dword [ebp-0x0c]
            0x00b2c6ea      mov   dword fs:[0x0], eax
            0x00b2c6f0      mov   esi, ecx
            0x00b2c6f2      mov   eax, dword [esi+0x04]
            0x00b2c6f5      lea   ecx, dword [ebp+0x50]
            0x00b2c6f8      mov   dword [ebp+0x4c], eax
            0x00b2c6fb      lea   eax, dword [esi+0x08]
            0x00b2c6fe      push  eax
            0x00b2c6ff      call  0x4f70d0
            0x00b2c704      mov   eax, dword [ebp+0x4c]
            0x00b2c707      sub   esp, 0x14
            0x00b2c70a      mov   ecx, esp
            0x00b2c70c      mov   dword [ecx], eax
            0x00b2c70e      lea   eax, dword [ebp+0x50]
            0x00b2c711      add   ecx, 0x04
            0x00b2c714      push  eax
            0x00b2c715      call  0x4f70d0
            0x00b2c71a      mov   edi, dword [ebp+0x70]
            0x00b2c71d      mov   ebx, dword [ebp+0x6c]
            0x00b2c720      push  edi
            0x00b2c721      push  ebx
            0x00b2c722      call  0xb28a70
            0x00b2c727      mov   ecx, dword [esi+0x104]
            0x00b2c72d      add   esp, 0x1c
            0x00b2c730      mov   dword [ebp+0x38], ecx
            0x00b2c733      lea   ecx, dword [esi+0x108]
            0x00b2c739      mov   dword [ebp+0x70], eax
            0x00b2c73c      push  ecx
            0x00b2c73d      lea   ecx, dword [ebp+0x3c]
            0x00b2c740      call  0x4f70d0
            0x00b2c745      mov   eax, dword [ebp+0x38]
            0x00b2c748      sub   esp, 0x14
            0x00b2c74b      mov   ecx, esp
            0x00b2c74d      mov   dword [ecx], eax
            0x00b2c74f      lea   eax, dword [ebp+0x3c]
            0x00b2c752      add   ecx, 0x04
            0x00b2c755      push  eax
            0x00b2c756      call  0x4f70d0
            0x00b2c75b      push  edi
            0x00b2c75c      push  ebx
            0x00b2c75d      call  0xb28a70
            0x00b2c762      add   esp, 0x1c
            0x00b2c765      test  eax, eax
        ,=< 0x00b2c767      jz    0xb2c778
        |   0x00b2c769      mov   dword [ebp+0x60], 0xffffffff         ; -1
        |   0x00b2c770      mov   eax, dword [eax+0x20]
        |   0x00b2c773      mov   dword [ebp+0x60], eax
       ,==< 0x00b2c776      jmp   0xb2c780
       |`-> 0x00b2c778      lea   ecx, dword [ebp+0x60]
       |    0x00b2c77b      call  0x4f6c50
       `--> 0x00b2c780      sub   esp, 0x1c
            0x00b2c783      mov   dword [ebp-0x04], 0x00
            0x00b2c78a      lea   eax, dword [esi+0xe8]
            0x00b2c790      mov   ecx, esp
            0x00b2c792      push  eax
            0x00b2c793      call  0xb2a260
            0x00b2c798      push  edi
            0x00b2c799      lea   eax, dword [ebp-0x28]
            0x00b2c79c      push  ebx
            0x00b2c79d      push  eax
            0x00b2c79e      call  0xb2e590
            0x00b2c7a3      sub   esp, 0x24
            0x00b2c7a6      mov   byte [ebp-0x04], 0x01
            0x00b2c7aa      lea   eax, dword [esi+0x9c]
            0x00b2c7b0      mov   ecx, esp
            0x00b2c7b2      push  eax
            0x00b2c7b3      call  0xb2a2f0
            0x00b2c7b8      push  edi
            0x00b2c7b9      lea   eax, dword [ebp-0xc0]
            0x00b2c7bf      push  ebx
            0x00b2c7c0      push  eax
            0x00b2c7c1      call  0xb2e600
            0x00b2c7c6      add   esp, 0x0c
            0x00b2c7c9      mov   byte [ebp-0x04], 0x02
            0x00b2c7cd      lea   eax, dword [esi+0x50]
            0x00b2c7d0      mov   ecx, esp
            0x00b2c7d2      push  eax
            0x00b2c7d3      call  0xb2a2f0
            0x00b2c7d8      push  edi
            0x00b2c7d9      lea   eax, dword [ebp-0x74]
            0x00b2c7dc      push  ebx
            0x00b2c7dd      push  eax
            0x00b2c7de      call  0xb2e600
            0x00b2c7e3      add   esp, 0x3c
            0x00b2c7e6      mov   byte [ebp-0x04], 0x03
            0x00b2c7ea      lea   eax, dword [esi+0x34]
            0x00b2c7ed      mov   ecx, esp
            0x00b2c7ef      push  eax
            0x00b2c7f0      call  0xb2a260
            0x00b2c7f5      push  edi
            0x00b2c7f6      lea   eax, dword [ebp]
            0x00b2c7f9      push  ebx
            0x00b2c7fa      push  eax
            0x00b2c7fb      call  0xb2e590
            0x00b2c800      add   esp, 0x0c
            0x00b2c803      mov   byte [ebp-0x04], 0x04
            0x00b2c807      lea   eax, dword [esi+0x18]
            0x00b2c80a      mov   ecx, esp
            0x00b2c80c      push  eax
            0x00b2c80d      call  0xb2a260
            0x00b2c812      push  edi
            0x00b2c813      lea   eax, dword [ebp+0x1c]
            0x00b2c816      push  ebx
            0x00b2c817      push  eax
            0x00b2c818      call  0xb2e590
            0x00b2c81d      lea   eax, dword [ebp+0x60]
            0x00b2c820      mov   dword [ebp-0x04], 0x0a
            0x00b2c827      push  eax
            0x00b2c828      lea   eax, dword [ebp-0x28]
            0x00b2c82b      push  eax
            0x00b2c82c      lea   eax, dword [ebp-0xc0]
            0x00b2c832      push  eax
            0x00b2c833      lea   eax, dword [ebp-0x74]
            0x00b2c836      push  eax
            0x00b2c837      lea   eax, dword [ebp]
            0x00b2c83a      push  eax
            0x00b2c83b      lea   eax, dword [ebp+0x1c]
            0x00b2c83e      push  eax
            0x00b2c83f      push  dword [ebp+0x70]
            0x00b2c842      call  0xba59b0
            0x00b2c847      add   esp, 0x44
            0x00b2c84a      mov   eax, dword [ebp+0x2c]
            0x00b2c84d      mov   byte [ebp-0x04], 0x0b                ; 0xb ; 11
            0x00b2c851      mov   dword [ebp+0x30], 0x00
            0x00b2c858      test  eax, eax
        ,=< 0x00b2c85a      jz    0xb2c867
        |   0x00b2c85c      push  eax
        |   0x00b2c85d      push  0x00
        |   0x00b2c85f      call  0x5291c0
        |   0x00b2c864      add   esp, 0x08
        `-> 0x00b2c867      mov   eax, dword [ebp+0x10]
            0x00b2c86a      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
            0x00b2c86e      mov   dword [ebp+0x14], 0x00
            0x00b2c875      test  eax, eax
        ,=< 0x00b2c877      jz    0xb2c884
        |   0x00b2c879      push  eax
        |   0x00b2c87a      push  0x00
        |   0x00b2c87c      call  0x5291c0
        |   0x00b2c881      add   esp, 0x08
        `-> 0x00b2c884      mov   eax, dword [ebp-0x34]
            0x00b2c887      mov   byte [ebp-0x04], 0x0d                ; 0xd ; 13
            0x00b2c88b      mov   dword [ebp-0x30], 0x00
            0x00b2c892      test  eax, eax
        ,=< 0x00b2c894      jz    0xb2c8a1
        |   0x00b2c896      push  eax
        |   0x00b2c897      push  0x00
        |   0x00b2c899      call  0x5291c0
        |   0x00b2c89e      add   esp, 0x08
        `-> 0x00b2c8a1      mov   eax, dword [ebp-0x80]
            0x00b2c8a4      mov   byte [ebp-0x04], 0x0e                ; 0xe ; 14
            0x00b2c8a8      mov   dword [ebp-0x7c], 0x00
            0x00b2c8af      test  eax, eax
        ,=< 0x00b2c8b1      jz    0xb2c8be
        |   0x00b2c8b3      push  eax
        |   0x00b2c8b4      push  0x00
        |   0x00b2c8b6      call  0x5291c0
        |   0x00b2c8bb      add   esp, 0x08
        `-> 0x00b2c8be      mov   eax, dword [ebp-0x18]
            0x00b2c8c1      mov   byte [ebp-0x04], 0x0f                ; 0xf ; 15
            0x00b2c8c5      mov   dword [ebp-0x14], 0x00
            0x00b2c8cc      test  eax, eax
        ,=< 0x00b2c8ce      jz    0xb2c8db
        |   0x00b2c8d0      push  eax
        |   0x00b2c8d1      push  0x00
        |   0x00b2c8d3      call  0x5291c0
        |   0x00b2c8d8      add   esp, 0x08
        `-> 0x00b2c8db      lea   ecx, dword [ebp+0x60]
            0x00b2c8de      call  0x4dc500
            0x00b2c8e3      mov   ecx, dword [ebp-0x0c]
            0x00b2c8e6      mov   dword fs:[0x0], ecx
            0x00b2c8ed      pop   ecx
            0x00b2c8ee      pop   edi
            0x00b2c8ef      pop   esi
            0x00b2c8f0      pop   ebx
            0x00b2c8f1      lea   esp, dword [ebp+0x64]
            0x00b2c8f4      pop   ebp
            0x00b2c8f5      ret   0x08
            0x00b2c8f8      int3
            0x00b2c8f9      int3
            0x00b2c8fa      int3
            0x00b2c8fb      int3
            0x00b2c8fc      int3
            0x00b2c8fd      int3
            0x00b2c8fe      int3
            0x00b2c8ff      int3
            0x00b2c900      push  esi
            0x00b2c901      mov   edx, ecx
            0x00b2c903      sub   esp, 0x14
            0x00b2c906      mov   ecx, esp
            0x00b2c908      mov   eax, dword [edx+0x04]
            0x00b2c90b      mov   esi, dword [edx+0x18]
            0x00b2c90e      mov   dword [ecx], eax
            0x00b2c910      lea   eax, dword [edx+0x08]
            0x00b2c913      push  eax
            0x00b2c914      add   ecx, 0x04
            0x00b2c917      call  0x4f70d0
            0x00b2c91c      push  dword [esp+0x20]
            0x00b2c920      push  dword [esp+0x20]
            0x00b2c924      call  0xb2e4f0
            0x00b2c929      add   esp, 0x1c
            0x00b2c92c      mov   ecx, eax
            0x00b2c92e      push  esi
            0x00b2c92f      call  0xa78ba0
            0x00b2c934      pop   esi
            0x00b2c935      ret   0x08
            0x00b2c938      int3
            0x00b2c939      int3
            0x00b2c93a      int3
            0x00b2c93b      int3
            0x00b2c93c      int3
            0x00b2c93d      int3
            0x00b2c93e      int3
            0x00b2c93f      int3
            0x00b2c940      push  ebp
            0x00b2c941      mov   ebp, esp
            0x00b2c943      push  0xffffffff                           ; 255
            0x00b2c945      push  0x1868f83
            0x00b2c94a      mov   eax, dword fs:[0x0]
            0x00b2c950      push  eax
            0x00b2c951      sub   esp, 0xa4
            0x00b2c957      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2c95c      xor   eax, ebp
            0x00b2c95e      mov   dword [ebp-0x10], eax
            0x00b2c961      push  ebx
            0x00b2c962      push  esi
            0x00b2c963      push  edi
            0x00b2c964      push  eax
            0x00b2c965      lea   eax, dword [ebp-0x0c]
            0x00b2c968      mov   dword fs:[0x0], eax
            0x00b2c96e      mov   ebx, ecx
            0x00b2c970      mov   dword [ebp-0x20], ebx
            0x00b2c973      mov   eax, dword [ebx+0xec]
            0x00b2c979      lea   ecx, dword [ebp-0x48]
            0x00b2c97c      mov   edi, dword [ebp+0x08]
            0x00b2c97f      mov   esi, dword [ebp+0x0c]
            0x00b2c982      mov   dword [ebp-0x24], eax
            0x00b2c985      lea   eax, dword [ebx+0xc8]
            0x00b2c98b      push  eax
            0x00b2c98c      call  0xabb0d0
            0x00b2c991      lea   eax, dword [ebx+0x6c]
            0x00b2c994      push  eax
            0x00b2c995      push  esi
            0x00b2c996      lea   eax, dword [ebp-0xb0]
            0x00b2c99c      push  edi
            0x00b2c99d      push  eax
            0x00b2c99e      call  0xb2e330
            0x00b2c9a3      mov   ebx, eax
            0x00b2c9a5      mov   ecx, dword [ebp-0x20]
            0x00b2c9a8      lea   eax, dword [ebp-0x7c]
            0x00b2c9ab      add   ecx, 0x10                            ; 16
            0x00b2c9ae      mov   dword [ebp-0x04], 0x00
            0x00b2c9b5      push  ecx
            0x00b2c9b6      push  esi
            0x00b2c9b7      push  edi
            0x00b2c9b8      push  eax
            0x00b2c9b9      call  0xb2e330
            0x00b2c9be      mov   ecx, dword [ebp-0x20]
            0x00b2c9c1      push  0x00
            0x00b2c9c3      push  0x00
            0x00b2c9c5      push  0x01                                 ; 1
            0x00b2c9c7      movss xmm0, dword [ecx+0x04]
            0x00b2c9cc      push  0x00
            0x00b2c9ce      movss dword [ebp-0x1c], xmm0
            0x00b2c9d3      movss xmm0, dword [ecx+0x08]
            0x00b2c9d8      push  0x00
            0x00b2c9da      push  dword [ebp-0x24]
            0x00b2c9dd      movss dword [ebp-0x18], xmm0
            0x00b2c9e2      movss xmm0, dword [ecx+0x0c]
            0x00b2c9e7      lea   ecx, dword [ebp-0x48]
            0x00b2c9ea      push  ecx
            0x00b2c9eb      push  ebx
            0x00b2c9ec      push  eax
            0x00b2c9ed      lea   eax, dword [ebp-0x1c]
            0x00b2c9f0      mov   byte [ebp-0x04], 0x01
            0x00b2c9f4      push  eax
            0x00b2c9f5      movss dword [ebp-0x14], xmm0
            0x00b2c9fa      call  0xb349c0
            0x00b2c9ff      add   esp, 0x48
            0x00b2ca02      lea   ecx, dword [ebp-0x7c]
            0x00b2ca05      call  0xa6bea0
            0x00b2ca0a      lea   ecx, dword [ebp-0xb0]
            0x00b2ca10      call  0xa6bea0
            0x00b2ca15      mov   ecx, dword [ebp-0x0c]
            0x00b2ca18      mov   dword fs:[0x0], ecx
            0x00b2ca1f      pop   ecx
            0x00b2ca20      pop   edi
            0x00b2ca21      pop   esi
            0x00b2ca22      pop   ebx
            0x00b2ca23      mov   ecx, dword [ebp-0x10]
            0x00b2ca26      xor   ecx, ebp
            0x00b2ca28      call  0x18075f6
            0x00b2ca2d      mov   esp, ebp
            0x00b2ca2f      pop   ebp
            0x00b2ca30      ret   0x08
            0x00b2ca33      int3
            0x00b2ca34      int3
            0x00b2ca35      int3
            0x00b2ca36      int3
            0x00b2ca37      int3
            0x00b2ca38      int3
            0x00b2ca39      int3
            0x00b2ca3a      int3
            0x00b2ca3b      int3
            0x00b2ca3c      int3
            0x00b2ca3d      int3
            0x00b2ca3e      int3
            0x00b2ca3f      int3
            0x00c095d0      push  ebp
            0x00c095d1      mov   ebp, esp
            0x00c095d3      push  0xffffffff                           ; 255
            0x00c095d5      push  0x18762e0
            0x00c095da      mov   eax, dword fs:[0x0]
            0x00c095e0      push  eax
            0x00c095e1      sub   esp, 0x24
            0x00c095e4      push  ebx
            0x00c095e5      push  esi
            0x00c095e6      push  edi
            0x00c095e7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c095ec      xor   eax, ebp
            0x00c095ee      push  eax
            0x00c095ef      lea   eax, dword [ebp-0x0c]
            0x00c095f2      mov   dword fs:[0x0], eax
            0x00c095f8      mov   ebx, ecx
            0x00c095fa      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c095ff      xor   edx, edx
            0x00c09601      mov   edi, dword [ebx+0x08]
            0x00c09604      xor   esi, esi
            0x00c09606      mov   eax, dword [eax+0xd8]
            0x00c0960c      mov   dword [ebp-0x20], edx
            0x00c0960f      mov   dword [ebp-0x1c], esi
            0x00c09612      mov   ecx, dword [eax*4+0x20286d8]
            0x00c09619      mov   dword [ebp-0x24], ecx
            0x00c0961c      test  ecx, ecx
        ,=< 0x00c0961e      jz    0xc09633
        |   0x00c09620      mov   eax, dword [ecx]
        |   0x00c09622      lea   edx, dword [ebp-0x20]
        |   0x00c09625      push  esi
        |   0x00c09626      push  edx
        |   0x00c09627      call  dword [eax+0x40]                     ; 64
        |   0x00c0962a      mov   esi, dword [ebp-0x1c]
        |   0x00c0962d      mov   edx, dword [ebp-0x20]
        |   0x00c09630      mov   ecx, dword [ebp-0x24]
        `-> 0x00c09633      mov   dword [ebp-0x04], 0x00
            0x00c0963a      test  ecx, ecx
        ,=< 0x00c0963c      jz    0xc0964b
        |   0x00c0963e      movzx ecx, word [edi+0x20]
        |   0x00c09642      cmp   ecx, esi
       ,==< 0x00c09644      jnb   0xc0964b
       ||   0x00c09646      mov   ecx, dword [edx+ecx*4]
      ,===< 0x00c09649      jmp   0xc0964d
      |``-> 0x00c0964b      xor   ecx, ecx
      `---> 0x00c0964d      mov   eax, dword [0x203cfa8]               ; [0x203cfa8:4]=0
            0x00c09652      mov   dword [ebp-0x10], ecx
            0x00c09655      mov   eax, dword [eax+0x1c]
            0x00c09658      push  eax
            0x00c09659      mov   dword [ebp-0x18], eax
            0x00c0965c      call  0xb7d600
            0x00c09661      push  dword [0x202731c]
            0x00c09667      lea   ecx, dword [ebx+0x0c]
            0x00c0966a      mov   edi, eax
            0x00c0966c      call  0xbcdcd0
            0x00c09671      mov   ecx, edi
            0x00c09673      mov   esi, eax
            0x00c09675      call  0xb47e90
            0x00c0967a      cmp   eax, esi
        ,=< 0x00c0967c      jnl   0xc09699
        |   0x00c0967e      mov   ecx, ebx
        |   0x00c09680      call  0xc0eb40
        |   0x00c09685      mov   ecx, dword [ebp-0x0c]
        |   0x00c09688      mov   dword fs:[0x0], ecx
        |   0x00c0968f      pop   ecx
        |   0x00c09690      pop   edi
        |   0x00c09691      pop   esi
        |   0x00c09692      pop   ebx
        |   0x00c09693      mov   esp, ebp
        |   0x00c09695      pop   ebp
        |   0x00c09696      ret   0x08
        `-> 0x00c09699      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c0969e      xor   edx, edx
            0x00c096a0      xor   esi, esi
            0x00c096a2      mov   eax, dword [eax+0x210]
            0x00c096a8      mov   dword [ebp-0x2c], edx
            0x00c096ab      mov   dword [ebp-0x28], esi
            0x00c096ae      mov   ecx, dword [eax*4+0x20286d8]
            0x00c096b5      mov   dword [ebp-0x30], ecx
            0x00c096b8      test  ecx, ecx
        ,=< 0x00c096ba      jz    0xc096cf
        |   0x00c096bc      mov   eax, dword [ecx]
        |   0x00c096be      lea   edx, dword [ebp-0x2c]
        |   0x00c096c1      push  esi
        |   0x00c096c2      push  edx
        |   0x00c096c3      call  dword [eax+0x3c]                     ; 60
        |   0x00c096c6      mov   esi, dword [ebp-0x28]
        |   0x00c096c9      mov   edx, dword [ebp-0x2c]
        |   0x00c096cc      mov   ecx, dword [ebp-0x30]
        `-> 0x00c096cf      mov   eax, dword [ebx+0x08]
            0x00c096d2      lea   edi, dword [ebx+0x0c]
            0x00c096d5      mov   byte [ebp-0x04], 0x02
            0x00c096d9      test  ecx, ecx
        ,=< 0x00c096db      jz    0xc09713
        |   0x00c096dd      movzx ecx, word [eax+0x20]
        |   0x00c096e1      cmp   ecx, esi
       ,==< 0x00c096e3      jnb   0xc09713
       ||   0x00c096e5      mov   ecx, dword [edx+ecx*4]
       ||   0x00c096e8      test  ecx, ecx
      ,===< 0x00c096ea      jz    0xc09713
      |||   0x00c096ec      push  0x01                                 ; 1
      |||   0x00c096ee      push  edi
      |||   0x00c096ef      call  0xbf29f0
      |||   0x00c096f4      test  al, al
     ,====< 0x00c096f6      jnz   0xc09713
     ||||   0x00c096f8      mov   ecx, ebx
     ||||   0x00c096fa      call  0xc0eb40
     ||||   0x00c096ff      mov   ecx, dword [ebp-0x0c]
     ||||   0x00c09702      mov   dword fs:[0x0], ecx
     ||||   0x00c09709      pop   ecx
     ||||   0x00c0970a      pop   edi
     ||||   0x00c0970b      pop   esi
     ||||   0x00c0970c      pop   ebx
     ||||   0x00c0970d      mov   esp, ebp
     ||||   0x00c0970f      pop   ebp
     ||||   0x00c09710      ret   0x08
     ````-> 0x00c09713      mov   eax, dword [0x201e2d8]               ; [0x201e2d8:4]=0
            0x00c09718      mov   esi, dword [ebx+0x20]
            0x00c0971b      mov   byte [ebp-0x04], 0x00
            0x00c0971f      mov   ecx, dword [eax+0x38]
            0x00c09722      call  0xaa3020
            0x00c09727      cmp   esi, eax
        ,=< 0x00c09729      jnz   0xc097c7
        |   0x00c0972f      invalid
            0x00ba5520      push  ebp
            0x00ba5521      mov   ebp, esp
            0x00ba5523      push  0xffffffff                           ; 255
            0x00ba5525      push  0x18363d8
            0x00ba552a      mov   eax, dword fs:[0x0]
            0x00ba5530      push  eax
            0x00ba5531      sub   esp, 0x24
            0x00ba5534      push  ebx
            0x00ba5535      push  esi
            0x00ba5536      push  edi
            0x00ba5537      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00ba553c      xor   eax, ebp
            0x00ba553e      push  eax
            0x00ba553f      lea   eax, dword [ebp-0x0c]
            0x00ba5542      mov   dword fs:[0x0], eax
            0x00ba5548      mov   esi, ecx
            0x00ba554a      mov   dword [ebp-0x10], esi
            0x00ba554d      mov   dword [ebp-0x2c], 0x00
            0x00ba5554      mov   dword [ebp-0x24], 0x00
            0x00ba555b      mov   dword [ebp-0x20], 0x00
            0x00ba5562      mov   ecx, dword [ebp+0x08]
            0x00ba5565      lea   edx, dword [ebp-0x30]
            0x00ba5568      push  dword [ebp+0x10]
            0x00ba556b      mov   dword [ebp-0x04], 0x00
            0x00ba5572      push  edx
            0x00ba5573      mov   eax, dword [ecx]
            0x00ba5575      call  dword [eax+0x28]                     ; 40
            0x00ba5578      mov   eax, dword [ebp-0x20]
            0x00ba557b      test  eax, eax
        ,=< 0x00ba557d      jz    0xba5625
        |   0x00ba5583      mov   edi, dword [ebp-0x24]
        |   0x00ba5586      mov   dword [ebp+0x08], edi
        |   0x00ba5589      lea   eax, dword [edi+eax*4]
        |   0x00ba558c      mov   dword [ebp-0x18], eax
        |   0x00ba558f      cmp   edi, eax
       ,==< 0x00ba5591      jz    0xba5615
       ||   0x00ba5597      lea   ebx, dword [esi+0x0c]
       ||   0x00ba559a      mov   dword [ebp-0x1c], ebx
       ||   0x00ba559d      nop   dword [eax], eax
      .---> 0x00ba55a0      mov   esi, dword [ebx+0x10]
      :||   0x00ba55a3      mov   eax, dword [edi]
      :||   0x00ba55a5      mov   dword [ebp+0x10], eax
      :||   0x00ba55a8      cmp   esi, dword [ebx+0x04]
     ,====< 0x00ba55ab      jnz   0xba55b4
     |:||   0x00ba55ad      mov   ecx, ebx
     |:||   0x00ba55af      call  0x58f930
     `----> 0x00ba55b4      mov   eax, dword [ebx+0x0c]
      :||   0x00ba55b7      mov   ecx, dword [ebp+0x10]
      :||   0x00ba55ba      mov   dword [eax+esi*4], ecx
      :||   0x00ba55bd      lea   eax, dword [esi+0x01]
      :||   0x00ba55c0      mov   dword [ebx+0x10], eax
      :||   0x00ba55c3      mov   eax, dword [ebp-0x10]
      :||   0x00ba55c6      cmp   dword [eax+0x1c], 0x00
      :||   0x00ba55ca      mov   ecx, dword [eax+0x34]
      :||   0x00ba55cd      mov   esi, dword [eax+0x30]
      :||   0x00ba55d0      setnz byte [ebp-0x14]
      :||   0x00ba55d4      shl   ecx, 0x02
      :||   0x00ba55d7      xor   edx, edx
      :||   0x00ba55d9      xor   ebx, ebx
      :||   0x00ba55db      lea   eax, dword [ecx+esi*1]
      :||   0x00ba55de      add   ecx, 0x03
      :||   0x00ba55e1      shr   ecx, 0x02
      :||   0x00ba55e4      cmp   esi, eax
      :||   0x00ba55e6      cmovnbe ecx, edx
      :||   0x00ba55e9      test  ecx, ecx
     ,====< 0x00ba55eb      jz    0xba5604
     |:||   0x00ba55ed      mov   edi, ecx
     |:||   0x00ba55ef      nop
    .-----> 0x00ba55f0      mov   ecx, dword [esi]
    :|:||   0x00ba55f2      push  dword [ebp-0x14]
    :|:||   0x00ba55f5      mov   eax, dword [ecx]
    :|:||   0x00ba55f7      call  dword [eax]
    :|:||   0x00ba55f9      inc   ebx
    :|:||   0x00ba55fa      lea   esi, dword [esi+0x04]
    :|:||   0x00ba55fd      cmp   ebx, edi
    `=====< 0x00ba55ff      jnz   0xba55f0
     |:||   0x00ba5601      mov   edi, dword [ebp+0x08]
     `----> 0x00ba5604      mov   ebx, dword [ebp-0x1c]
      :||   0x00ba5607      add   edi, 0x04
      :||   0x00ba560a      mov   dword [ebp+0x08], edi
      :||   0x00ba560d      cmp   edi, dword [ebp-0x18]
      `===< 0x00ba5610      jnz   0xba55a0
       ||   0x00ba5612      mov   esi, dword [ebp-0x10]
       `--> 0x00ba5615      mov   ecx, esi
        |   0x00ba5617      call  0xbaa890
        |   0x00ba561c      mov   eax, dword [ebp-0x20]
        |   0x00ba561f      mov   byte [ebp+0x0b], 0x01
       ,==< 0x00ba5623      jmp   0xba5629
       |`-> 0x00ba5625      mov   byte [ebp+0x0b], 0x00
       `--> 0x00ba5629      mov   ebx, dword [ebp+0x0c]
            0x00ba562c      test  ebx, ebx
        ,=< 0x00ba562e      jz    0xba566e
        |   0x00ba5630      mov   esi, dword [ebp-0x24]
        |   0x00ba5633      lea   edi, dword [esi+eax*4]
        |   0x00ba5636      cmp   esi, edi
       ,==< 0x00ba5638      jz    0xba566e
       ||   0x00ba563a      mov   ecx, dword [ebx+0x10]
       ||   0x00ba563d      mov   dword [ebp+0x10], ecx
      .---> 0x00ba5640      mov   eax, dword [esi]
      :||   0x00ba5642      mov   eax, dword [eax+0x08]
      :||   0x00ba5645      mov   dword [ebp+0x0c], eax
      :||   0x00ba5648      cmp   ecx, dword [ebx+0x04]
     ,====< 0x00ba564b      jnz   0xba5657
     |:||   0x00ba564d      mov   ecx, ebx
     |:||   0x00ba564f      call  0x92a100
     |:||   0x00ba5654      mov   ecx, dword [ebp+0x10]
     `----> 0x00ba5657      mov   eax, dword [ebx+0x0c]
      :||   0x00ba565a      add   esi, 0x04
      :||   0x00ba565d      mov   edx, dword [ebp+0x0c]
      :||   0x00ba5660      mov   dword [eax+ecx*4], edx
      :||   0x00ba5663      inc   ecx
      :||   0x00ba5664      mov   dword [ebp+0x10], ecx
      :||   0x00ba5667      mov   dword [ebx+0x10], ecx
      :||   0x00ba566a      cmp   esi, edi
      `===< 0x00ba566c      jnz   0xba5640
       ``-> 0x00ba566e      cmp   dword [ebp-0x2c], 0x00
            0x00ba5672      mov   dword [ebp-0x04], 0x01
            0x00ba5679      mov   dword [ebp-0x20], 0x00
        ,=< 0x00ba5680      jz    0xba5696
        |   0x00ba5682      mov   esi, dword [ebp-0x24]
        |   0x00ba5685      test  esi, esi
       ,==< 0x00ba5687      jz    0xba5696
       ||   0x00ba5689      call  0x52b950
       ||   0x00ba568e      push  esi
       ||   0x00ba568f      mov   ecx, eax
       ||   0x00ba5691      call  0x52b8b0
       ``-> 0x00ba5696      mov   al, byte [ebp+0x0b]
            0x00ba5699      mov   ecx, dword [ebp-0x0c]
            0x00ba569c      invalid
            0x00ba569d      invalid
            0x00ba569e      invalid
            0x00ba569f      invalid
