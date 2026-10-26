            0x004f70f0      push  ebp
            0x004f70f1      mov   ebp, esp
            0x004f70f3      push  0xffffffff                           ; 255
            0x004f70f5      push  0x180c5a0
            0x004f70fa      mov   eax, dword fs:[0x0]
            0x004f7100      push  eax
            0x004f7101      sub   esp, 0x28
            0x004f7104      push  esi
            0x004f7105      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x004f710a      xor   eax, ebp
            0x004f710c      push  eax
            0x004f710d      lea   eax, dword [ebp-0x0c]
            0x004f7110      mov   dword fs:[0x0], eax
            0x004f7116      mov   esi, ecx
            0x004f7118      mov   eax, dword [ebp+0x08]
            0x004f711b      mov   ecx, dword [eax]
            0x004f711d      test  ecx, ecx
        ,=< 0x004f711f      jnz   0x4f7140
        |   0x004f7121      mov   dword [esi], ecx
        |   0x004f7123      mov   dword [esi+0x04], ecx
        |   0x004f7126      mov   dword [esi+0x08], ecx
        |   0x004f7129      mov   dword [esi+0x0c], ecx
       .--> 0x004f712c      mov   eax, esi
       :|   0x004f712e      mov   ecx, dword [ebp-0x0c]
       :|   0x004f7131      mov   dword fs:[0x0], ecx
       :|   0x004f7138      pop   ecx
       :|   0x004f7139      pop   esi
       :|   0x004f713a      mov   esp, ebp
       :|   0x004f713c      pop   ebp
       :|   0x004f713d      ret   0x04
       :`-> 0x004f7140      cmp   dword [ecx+0x1c], 0x23               ; '#'
       :,=< 0x004f7144      jnbe  0x4f719f
       :|   0x004f7146      add   ecx, 0x0c                            ; 0xc ; 12
       :|   0x004f7149      cmp   dword [ecx+0x14], 0x10
      ,===< 0x004f714d      jb    0x4f7151
      |:|   0x004f714f      mov   ecx, dword [ecx]
      `---> 0x004f7151      lea   eax, dword [esi+0x0c]
       :|   0x004f7154      push  eax
       :|   0x004f7155      lea   eax, dword [esi+0x08]
       :|   0x004f7158      push  eax
       :|   0x004f7159      lea   eax, dword [esi+0x04]
       :|   0x004f715c      push  eax
       :|   0x004f715d      push  esi
       :|   0x004f715e      push  str.x:_x:_x:_x                       ; 0x1931fb0 ; "%x:%x:%x:%x"
       :|   0x004f7163      push  ecx
       :|   0x004f7164      call  0x528f80
       :|   0x004f7169      add   esp, 0x18
       :|   0x004f716c      cmp   eax, 0x04                            ; 4
       `==< 0x004f716f      jz    0x4f712c
        |   0x004f7171      push  0x1931f8c                            ; u"Wrong GUID Format"
        |   0x004f7176      lea   ecx, dword [ebp+0x08]
        |   0x004f7179      call  0x4e6e90
        |   0x004f717e      lea   eax, dword [ebp+0x08]
        |   0x004f7181      mov   dword [ebp-0x04], 0x01
        |   0x004f7188      push  eax
        |   0x004f7189      lea   ecx, dword [ebp-0x34]
        |   0x004f718c      call  0x4e9850
        |   0x004f7191      push  0x1c6b664
        |   0x004f7196      lea   eax, dword [ebp-0x34]
        |   0x004f7199      push  eax
        |   0x004f719a      call  0x1809b26
        `-> 0x004f719f      push  0x1931f8c                            ; u"Wrong GUID Format"
            0x004f71a4      lea   ecx, dword [ebp+0x08]
            0x004f71a7      call  0x4e6e90
            0x004f71ac      lea   eax, dword [ebp+0x08]
            0x004f71af      mov   dword [ebp-0x04], 0x00
            0x004f71b6      push  eax
            0x004f71b7      lea   ecx, dword [ebp-0x20]
            0x004f71ba      call  0x4e9850
            0x004f71bf      push  0x1c6b664
            0x004f71c4      lea   eax, dword [ebp-0x20]
            0x004f71c7      push  eax
            0x004f71c8      call  0x1809b26
            0x004f71cd      int3
            0x004f71ce      int3
            0x004f71cf      int3
            0x004f71d0      mov   eax, dword [esp+0x04]
            0x004f71d4      mov   dword [ecx], eax
            0x004f71d6      mov   eax, dword [esp+0x08]
            0x004f71da      mov   dword [ecx+0x04], eax
            0x004f71dd      mov   eax, dword [esp+0x0c]
            0x004f71e1      mov   dword [ecx+0x08], eax
            0x004f71e4      mov   eax, dword [esp+0x10]
            0x004f71e8      mov   dword [ecx+0x0c], eax
            0x004f71eb      mov   eax, ecx
            0x004f71ed      ret   0x10
            0x004f71f0      mov   dword [ecx], 0x00
            0x004f71f6      mov   eax, ecx
            0x004f71f8      mov   dword [ecx+0x04], 0x00
            0x004f71ff      mov   dword [ecx+0x08], 0x00
            0x004f7206      mov   dword [ecx+0x0c], 0x00
            0x004f720d      ret
            0x004f720e      int3
            0x004f720f      int3
            0x004f7210      push  ebp
            0x004f7211      mov   ebp, esp
            0x004f7213      push  0xffffffff                           ; 255
            0x004f7215      push  0x180aba8
            0x004f721a      mov   eax, dword fs:[0x0]
            0x004f7220      push  eax
            0x004f7221      push  ecx
            0x004f7222      push  esi
            0x004f7223      push  edi
            0x004f7224      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x004f7229      xor   eax, ebp
            0x004f722b      push  eax
            0x004f722c      lea   eax, dword [ebp-0x0c]
            0x004f722f      mov   dword fs:[0x0], eax
            0x004f7235      mov   edi, ecx
            0x004f7237      mov   dword [ebp-0x10], edi
            0x004f723a      mov   byte [edi+0x04], 0x00
            0x004f723e      mov   dword [edi+0x08], 0x00
            0x004f7245      mov   dword [edi+0x0c], 0x00
            0x004f724c      mov   esi, dword [0x1fcfa1c]               ; [0x1fcfa1c:4]=0
            0x004f7252      mov   ecx, esi
            0x004f7254      mov   dword [edi], 0x1931e84               ; [0x1931e84:4]=0x4ffd60 ; "`\xfdO"
            0x004f725a      push  0x00
            0x004f725c      mov   dword [ebp-0x04], 0x00
            0x004f7263      mov   dword [0x1fcff64], edi
            0x004f7269      call  0x52ae00
            0x004f726e      mov   ecx, dword [0x1fcfa1c]               ; [0x1fcfa1c:4]=0
            0x004f7274      mov   eax, dword [ecx+0x18]
            0x004f7277      mov   dword [edi+0x0c], eax
            0x004f727a      mov   eax, dword [ecx+0x18]
            0x004f727d      test  eax, eax
        ,=< 0x004f727f      jz    0x4f7284
        |   0x004f7281      mov   dword [eax+0x08], edi
        `-> 0x004f7284      mov   dword [ecx+0x18], edi
            0x004f7287      mov   ecx, esi
            0x004f7289      mov   byte [ebp-0x04], 0x01
            0x004f728d      call  0x52aea0
            0x004f7292      mov   dword [edi], 0x1931e8c               ; [0x1931e8c:4]=0x500e50 ; "P\U0000000eP"
            0x004f7298      mov   eax, edi
            0x004f729a      mov   dword [edi+0x10], 0x00
            0x004f72a1      mov   ecx, dword [ebp-0x0c]
            0x004f72a4      mov   dword fs:[0x0], ecx
            0x004f72ab      pop   ecx
            0x004f72ac      pop   edi
            0x004f72ad      pop   esi
            0x004f72ae      mov   esp, ebp
            0x004f72b0      pop   ebp
            0x004f72b1      ret
            0x004f72b2      int3
            0x004f72b3      int3
            0x004f72b4      int3
            0x004f72b5      int3
            0x004f72b6      int3
            0x004f72b7      int3
            0x004f72b8      int3
            0x004f72b9      int3
            0x004f72ba      int3
            0x004f72bb      int3
            0x004f72bc      int3
            0x004f72bd      int3
            0x004f72be      int3
            0x004f72bf      int3
            0x0147a5d0      push  ebp
            0x0147a5d1      mov   ebp, esp
            0x0147a5d3      push  0xffffffff                           ; 255
            0x0147a5d5      push  0x182a5d8
            0x0147a5da      mov   eax, dword fs:[0x0]
            0x0147a5e0      push  eax
            0x0147a5e1      push  ecx
            0x0147a5e2      push  esi
            0x0147a5e3      push  edi
            0x0147a5e4      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x0147a5e9      xor   eax, ebp
            0x0147a5eb      push  eax
            0x0147a5ec      lea   eax, dword [ebp-0x0c]
            0x0147a5ef      mov   dword fs:[0x0], eax
            0x0147a5f5      mov   edx, dword [ebp+0x0c]
            0x0147a5f8      test  edx, edx
        ,=< 0x0147a5fa      jnz   0x147a60f
  ......--> 0x0147a5fc      xor   al, al
  ::::::|   0x0147a5fe      mov   ecx, dword [ebp-0x0c]
  ::::::|   0x0147a601      mov   dword fs:[0x0], ecx
  ::::::|   0x0147a608      pop   ecx
  ::::::|   0x0147a609      pop   edi
  ::::::|   0x0147a60a      pop   esi
  ::::::|   0x0147a60b      mov   esp, ebp
  ::::::|   0x0147a60d      pop   ebp
  ::::::|   0x0147a60e      ret
  ::::::`-> 0x0147a60f      mov   ecx, dword [ebp+0x08]
  ::::::    0x0147a612      test  ecx, ecx
  ========< 0x0147a614      jz    0x147a5fc
  ::::::    0x0147a616      mov   esi, dword [edx]
  ::::::    0x0147a618      lea   edi, dword [edx+0x04]
  ::::::    0x0147a61b      mov   eax, dword [ebp+0x10]
  ::::::    0x0147a61e      add   edx, eax
  ::::::    0x0147a620      mov   dword [ecx], esi
  ::::::    0x0147a622      mov   dword [ebp+0x0c], edx
  ::::::    0x0147a625      cmp   edi, edx
  ========< 0x0147a627      jnbe  0x147a5fc
  ::::::    0x0147a629      cmp   esi, 0x02                            ; 2
  ========< 0x0147a62c      jnbe  0x147a5fc
  ::::::    0x0147a62e      cmp   esi, 0x01                            ; 1
  ========< 0x0147a631      jb    0x147a5fc
  ::::::    0x0147a633      cmp   dword [edi], 0x00
  ::::::    0x0147a636      setnz al
  ::::::    0x0147a639      mov   byte [ecx+0x04], al
  ::::::    0x0147a63c      mov   eax, dword [edi+0x04]
  ::::::    0x0147a63f      add   edi, 0x08
  ::::::    0x0147a642      mov   dword [ecx+0x08], eax
  ::::::    0x0147a645      cmp   edi, edx
  `=======< 0x0147a647      jnbe  0x147a5fc
   :::::    0x0147a649      mov   eax, dword [edi]
   :::::    0x0147a64b      add   edi, 0x04
   :::::    0x0147a64e      mov   dword [ecx+0x0c], eax
   :::::    0x0147a651      cmp   edi, edx
   `======< 0x0147a653      jnbe  0x147a5fc
    ::::    0x0147a655      mov   eax, dword [edi]
    ::::    0x0147a657      add   edi, 0x04
    ::::    0x0147a65a      mov   dword [ecx+0x10], eax
    ::::    0x0147a65d      cmp   edi, edx
    `=====< 0x0147a65f      jnbe  0x147a5fc
     :::    0x0147a661      mov   eax, dword [edi]
     :::    0x0147a663      add   edi, 0x04
     :::    0x0147a666      mov   dword [ecx+0x14], eax
     :::    0x0147a669      cmp   edi, edx
     `====< 0x0147a66b      jnbe  0x147a5fc
      ::    0x0147a66d      movzx eax, word [edi]
      ::    0x0147a670      add   edi, 0x02
      ::    0x0147a673      mov   dword [ecx+0x18], eax
      ::    0x0147a676      cmp   edi, edx
      `===< 0x0147a678      jnbe  0x147a5fc
       :    0x0147a67a      movzx eax, word [edi]
       :    0x0147a67d      add   edi, 0x02
       :    0x0147a680      cmp   edi, edx
       `==< 0x0147a682      jnbe  0x147a5fc
            0x0147a688      mov   esi, eax
            0x0147a68a      lea   ecx, dword [ebp-0x10]
            0x0147a68d      push  esi
            0x0147a68e      push  edi
            0x0147a68f      call  0x4e6d80
            0x0147a694      add   esi, 0x03
            0x0147a697      mov   dword [ebp-0x04], 0x00
            0x0147a69e      and   esi, 0xfffffffc                      ; 4294967292
            0x0147a6a1      add   esi, edi
            0x0147a6a3      mov   edi, dword [ebp+0x08]
            0x0147a6a6      cmp   dword [edi], 0x01
        ,=< 0x0147a6a9      jbe   0x147a6d0
        |   0x0147a6ab      mov   eax, dword [esi]
        |   0x0147a6ad      mov   dword [edi+0x20], eax
        |   0x0147a6b0      mov   eax, dword [esi+0x04]
        |   0x0147a6b3      mov   dword [edi+0x24], eax
        |   0x0147a6b6      mov   eax, dword [esi+0x08]
        |   0x0147a6b9      mov   dword [edi+0x28], eax
        |   0x0147a6bc      mov   eax, dword [esi+0x0c]
        |   0x0147a6bf      add   esi, 0x10                            ; 16
        |   0x0147a6c2      mov   dword [edi+0x2c], eax
        |   0x0147a6c5      cmp   esi, dword [ebp+0x0c]
       ,==< 0x0147a6c8      jnbe  0x147a750
      ,===< 0x0147a6ce      jmp   0x147a6d7
      ||`-> 0x0147a6d0      xorps xmm0, xmm0
      ||    0x0147a6d3      movups xmmword [edi+0x20], xmm0
      `---> 0x0147a6d7      mov   eax, dword [edi+0x18]
       |    0x0147a6da      cmp   eax, 0x10                            ; 16
       |,=< 0x0147a6dd      jnb   0x147a750
       ||   0x0147a6df      lea   ecx, dword [edi+0x30]
       ||   0x0147a6e2      push  eax
       ||   0x0147a6e3      call  0x147ab90
       ||   0x0147a6e8      push  dword [edi+0x18]
       ||   0x0147a6eb      lea   ecx, dword [edi+0x74]
       ||   0x0147a6ee      call  0x147ab90
       ||   0x0147a6f3      mov   eax, dword [edi+0x18]
       ||   0x0147a6f6      xor   edx, edx
       ||   0x0147a6f8      test  eax, eax
      ,===< 0x0147a6fa      jz    0x147a716
      |||   0x0147a6fc      lea   ecx, dword [edi+0x30]
      |||   0x0147a6ff      nop
     .----> 0x0147a700      mov   eax, dword [esi]
     :|||   0x0147a702      mov   dword [ecx], eax
     :|||   0x0147a704      test  al, 0x03                             ; 3
    ,=====< 0x0147a706      jnz   0x147a750
    |:|||   0x0147a708      mov   eax, dword [edi+0x18]
    |:|||   0x0147a70b      inc   edx
    |:|||   0x0147a70c      add   esi, 0x04
    |:|||   0x0147a70f      add   ecx, 0x04
    |:|||   0x0147a712      cmp   edx, eax
    |`====< 0x0147a714      jb    0x147a700
    | `---> 0x0147a716      xor   ecx, ecx
    |  ||   0x0147a718      test  eax, eax
    | ,===< 0x0147a71a      jz    0x147a731
    | |||   0x0147a71c      lea   edx, dword [edi+0x74]
    | |||   0x0147a71f      nop
            0x00ae5320      invalid
            0x00ae5321      dec   dword [edi]
            0x00ae5323      push  edi
            0x00ae5324      ror   byte [edi], cl
            0x00ae5326      xchg  esp, eax
            0x00ae5327      rol   byte [eax+eax*8+0x101850f], 0x00
            0x00ae532f      add   byte [ebx-0x9f7b], cl
            0x00ae5335      dec   dword [edi]
            0x00ae5337      adc   byte [ebp-0xc0], cl
            0x00ae533d      comiss xmm1, xmm2
            0x00ae5340      movups xmm0, xmmword [eax]
            0x00ae5343      movups xmmword [edi], xmm0
        ,=< 0x00ae5346      jbe   0xae5431
        |   0x00ae534c      movss dword [ebp-0xa8], xmm2
        |   0x00ae5354      mov   edi, 0x05
        |   0x00ae5359      nop   dword [eax], eax
       .--> 0x00ae5360      cmp   byte [ebx+0x18], 0x00
       :|   0x00ae5364      lea   edx, dword [ebp-0x28]
       :|   0x00ae5367      mov   ecx, dword [ebx+0x0c]
       :|   0x00ae536a      movaps xmm0, xmm1
       :|   0x00ae536d      addss xmm0, xmm2
       :|   0x00ae5371      mov   dword [ebp-0x98], 0x00
       :|   0x00ae537b      movups xmm2, xmmword [ecx]
       :|   0x00ae537e      subps xmm2, xmmword [eax]
       :|   0x00ae5381      mulss xmm0, dword [0x193d168]
       :|   0x00ae5389      mov   ecx, dword [0x2027e34]               ; [0x2027e34:4]=0
       :|   0x00ae538f      movss dword [ebp-0xa4], xmm0
       :|   0x00ae5397      shufps xmm0, xmm0, 0x00
       :|   0x00ae539b      mulps xmm2, xmm0
       :|   0x00ae539e      addps xmm2, xmmword [eax]
       :|   0x00ae53a1      movaps xmm0, xmm2
       :|   0x00ae53a4      movss dword [ebp-0x28], xmm2
       :|   0x00ae53a9      shufps xmm0, xmm2, 0x55
       :|   0x00ae53ad      movss dword [ebp-0x24], xmm0
       :|   0x00ae53b2      mov   eax, dword [ecx]
       :|   0x00ae53b4      movaps xmmword [ebp-0x40], xmm2
      ,===< 0x00ae53b8      jz    0xae53c1
      |:|   0x00ae53ba      push  0x1400004
     ,====< 0x00ae53bf      jmp   0xae53c4
     |`---> 0x00ae53c1      push  dword [ebx+0x14]
     `----> 0x00ae53c4      push  edx
       :|   0x00ae53c5      lea   edx, dword [ebp-0x98]
       :|   0x00ae53cb      push  edx
       :|   0x00ae53cc      call  dword [eax+0x10]                     ; 16
       :|   0x00ae53cf      test  dword [ebp-0x98], esi
       :|   0x00ae53d5      setz  al
       :|   0x00ae53d8      test  al, al
      ,===< 0x00ae53da      jz    0xae5402
      |:|   0x00ae53dc      mov   eax, dword [ebp-0xac]
      |:|   0x00ae53e2      movss xmm2, dword [ebp-0xa4]
      |:|   0x00ae53ea      movaps xmm0, xmmword [ebp-0x40]
      |:|   0x00ae53ee      movups xmm1, xmmword [ebp-0xc0]
      |:|   0x00ae53f5      movss dword [ebp-0xa8], xmm2
      |:|   0x00ae53fd      movups xmmword [eax], xmm0
     ,====< 0x00ae5400      jmp   0xae5419
     |`---> 0x00ae5402      movss xmm1, dword [ebp-0xa4]
     | :|   0x00ae540a      movss xmm2, dword [ebp-0xa8]
     | :|   0x00ae5412      movups xmmword [ebp-0xc0], xmm1
     `----> 0x00ae5419      mov   eax, dword [ebp-0xa0]
       :|   0x00ae541f      sub   edi, 0x01
       `==< 0x00ae5422      jnz   0xae5360
        |   0x00ae5428      mov   edi, dword [ebp-0xac]
        |   0x00ae542e      xorps xmm2, xmm2
        `-> 0x00ae5431      mov   al, byte [ebp-0x91]
            0x00ae5437      test  al, al
        ,=< 0x00ae5439      jnz   0xae5451
        |   0x00ae543b      mov   ecx, dword [ebx+0x0c]
        |   0x00ae543e      movups xmm0, xmmword [ecx]
        |   0x00ae5441      movups xmmword [edi], xmm0
        |   0x00ae5444      movaps xmm0, xmm2
        |   0x00ae5447      shufps xmm0, xmm0, 0xa0
        |   0x00ae544b      movaps xmmword [ebp-0x40], xmm0
       ,==< 0x00ae544f      jmp   0xae545a
       |`-> 0x00ae5451      movsd xmm2, qword [ebp-0x1c]
       |    0x00ae5456      movaps xmmword [ebp-0x40], xmm2
       `--> 0x00ae545a      mov   edx, dword [ebp-0xd0]
            0x00ae5460      lea   ecx, dword [ebp-0x40]
            0x00ae5463      movups xmm0, xmmword [ecx]
            0x00ae5466      mov   ecx, dword [ebp-0xc4]
            0x00ae546c      movups xmmword [ecx], xmm0
            0x00ae546f      mov   ecx, dword [ebp-0xd8]
            0x00ae5475      mov   dword [ebp-0x04], 0x03
            0x00ae547c      mov   dword [ebp-0xcc], 0x00
            0x00ae5486      test  ecx, ecx
        ,=< 0x00ae5488      jz    0xae549b
        |   0x00ae548a      push  edx
        |   0x00ae548b      push  0x00
        |   0x00ae548d      call  0x5291c0
        |   0x00ae5492      mov   al, byte [ebp-0x91]
        |   0x00ae5498      add   esp, 0x08
        `-> 0x00ae549b      mov   ecx, dword [ebp-0x0c]
            0x00ae549e      mov   dword fs:[0x0], ecx
            0x00ae54a5      pop   ecx
            0x00ae54a6      pop   edi
            0x00ae54a7      pop   esi
            0x00ae54a8      mov   ecx, dword [ebp-0x14]
            0x00ae54ab      xor   ecx, ebp
            0x00ae54ad      call  0x18075f6
            0x00ae54b2      mov   esp, ebp
            0x00ae54b4      pop   ebp
            0x00ae54b5      mov   esp, ebx
            0x00ae54b7      pop   ebx
            0x00ae54b8      ret   0x1c
            0x00ae54bb      int3
            0x00ae54bc      int3
            0x00ae54bd      int3
            0x00ae54be      int3
            0x00ae54bf      int3
            0x00ae54c0      push  ebp
            0x00ae54c1      mov   ebp, esp
            0x00ae54c3      push  0xffffffff                           ; 255
            0x00ae54c5      push  0x1865beb
            0x00ae54ca      mov   eax, dword fs:[0x0]
            0x00ae54d0      push  eax
            0x00ae54d1      sub   esp, 0xc4
            0x00ae54d7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00ae54dc      xor   eax, ebp
            0x00ae54de      invalid
            0x00ae54df      inc   ebp
            0x00524ca0      mov   ecx, dword [esp+0x04]
            0x00524ca4      mov   eax, dword [ecx+0x0c]
            0x00524ca7      xor   eax, dword [ecx+0x08]
            0x00524caa      xor   eax, dword [ecx+0x04]
            0x00524cad      xor   eax, dword [ecx]
            0x00524caf      ret
            0x00524cb0      mov   eax, dword [esp+0x04]
            0x00524cb4      mov   ecx, dword [eax+0x14]
            0x00524cb7      and   ecx, 0xfffff9ff                      ; 4294965759
            0x00524cbd      or    ecx, 0x800                           ; 2048
            0x00524cc3      mov   dword [eax+0x14], ecx
            0x00524cc6      ret
            0x00524cc7      int3
            0x00524cc8      int3
            0x00524cc9      int3
            0x00524cca      int3
            0x00524ccb      int3
            0x00524ccc      int3
            0x00524ccd      int3
            0x00524cce      int3
            0x00524ccf      int3
            0x00524cd0      sub   esp, 0x08
            0x00524cd3      cmp   byte [0x1fd094d], 0x00               ; [0x1fd094d:1]=0
        ,=< 0x00524cda      jnz   0x524dee
        |   0x00524ce0      push  ebx
        |   0x00524ce1      xor   dh, dh
        |   0x00524ce3      push  esi
        |   0x00524ce4      mov   byte [esp+0x0b], dh
        |   0x00524ce8      push  edi
        |   0x00524ce9      nop   dword [eax], eax
       .--> 0x00524cf0      xor   esi, esi
       :|   0x00524cf2      mov   bh, 0x80                             ; 128
      .---> 0x00524cf4      mov   eax, esi
      ::|   0x00524cf6      mov   dl, bh
      ::|   0x00524cf8      xor   eax, 0x8000
      ::|   0x00524cfd      mov   bl, bh
      ::|   0x00524cff      movzx ecx, ax
      ::|   0x00524d02      and   dl, dh
      ::|   0x00524d04      movzx eax, si
      ::|   0x00524d07      cmovz ecx, eax
      ::|   0x00524d0a      movzx esi, cx
      ::|   0x00524d0d      lea   ecx, dword [esi+esi*1]
      ::|   0x00524d10      mov   eax, ecx
      ::|   0x00524d12      xor   eax, 0x8005
      ::|   0x00524d17      test  si, si
      ::|   0x00524d1a      movzx edx, ax
      ::|   0x00524d1d      movzx eax, cx
      ::|   0x00524d20      cmovns edx, eax
      ::|   0x00524d23      shr   bh, 0x01
      ::|   0x00524d25      movzx eax, dx
      ::|   0x00524d28      mov   dh, byte [esp+0x0f]
      ::|   0x00524d2c      mov   esi, eax
      ::|   0x00524d2e      cmp   bl, 0x02                             ; 2
      `===< 0x00524d31      jnb   0x524cf4
       :|   0x00524d33      xor   edi, edi
       :|   0x00524d35      mov   dword [esp+0x10], eax
       :|   0x00524d39      mov   cx, ax
       :|   0x00524d3c      lea   edx, dword [edi+0x0f]
       :|   0x00524d3f      lea   esi, dword [edi+0x10]
      .---> 0x00524d42      test  byte [esp+0x10], 0x01
     ,====< 0x00524d47      jz    0x524d52
     |::|   0x00524d49      movzx eax, di
     |::|   0x00524d4c      bts   eax, edx
     |::|   0x00524d4f      movzx edi, ax
     `----> 0x00524d52      shr   cx, 0x01
      ::|   0x00524d55      dec   edx
      ::|   0x00524d56      mov   word [esp+0x10], cx
      ::|   0x00524d5b      sub   esi, 0x01
      `===< 0x00524d5e      jnz   0x524d42
       :|   0x00524d60      mov   dh, byte [esp+0x0f]
       :|   0x00524d64      xor   cl, cl
       :|   0x00524d66      test  dh, 0x01                             ; 1
      ,===< 0x00524d69      jz    0x524d71
      |:|   0x00524d6b      xor   ecx, ecx
      |:|   0x00524d6d      bts   ecx, 0x07
      `---> 0x00524d71      mov   al, dh
       :|   0x00524d73      shr   al, 0x01
       :|   0x00524d75      test  al, 0x01                             ; 1
      ,===< 0x00524d77      jz    0x524d80
      |:|   0x00524d79      movzx ecx, cl
      |:|   0x00524d7c      bts   ecx, 0x06
      `---> 0x00524d80      shr   al, 0x01
       :|   0x00524d82      test  al, 0x01                             ; 1
      ,===< 0x00524d84      jz    0x524d8d
      |:|   0x00524d86      movzx ecx, cl
      |:|   0x00524d89      bts   ecx, 0x05
      `---> 0x00524d8d      shr   al, 0x01
       :|   0x00524d8f      test  al, 0x01                             ; 1
      ,===< 0x00524d91      jz    0x524d9a
      |:|   0x00524d93      movzx ecx, cl
      |:|   0x00524d96      bts   ecx, 0x04
      `---> 0x00524d9a      shr   al, 0x01
       :|   0x00524d9c      test  al, 0x01                             ; 1
      ,===< 0x00524d9e      jz    0x524da7
      |:|   0x00524da0      movzx ecx, cl
      |:|   0x00524da3      bts   ecx, 0x03
      `---> 0x00524da7      shr   al, 0x01
       :|   0x00524da9      test  al, 0x01                             ; 1
      ,===< 0x00524dab      jz    0x524db4
      |:|   0x00524dad      movzx ecx, cl
      |:|   0x00524db0      bts   ecx, 0x02
      `---> 0x00524db4      shr   al, 0x01
       :|   0x00524db6      test  al, 0x01                             ; 1
      ,===< 0x00524db8      jz    0x524dc1
      |:|   0x00524dba      movzx ecx, cl
      |:|   0x00524dbd      bts   ecx, 0x01
      `---> 0x00524dc1      cmp   al, 0x02                             ; 2
      ,===< 0x00524dc3      jb    0x524dcc
      |:|   0x00524dc5      movzx ecx, cl
      |:|   0x00524dc8      bts   ecx, 0x00
      `---> 0x00524dcc      movzx eax, cl
       :|   0x00524dcf      add   dh, 0x01
       :|   0x00524dd2      mov   byte [esp+0x0f], dh
       :|   0x00524dd6      mov   word [eax*2+0x1fd0320], di
       `==< 0x00524dde      jnz   0x524cf0
        |   0x00524de4      pop   edi
        |   0x00524de5      pop   esi
        |   0x00524de6      mov   byte [0x1fd094d], 0x01
        |   0x00524ded      pop   ebx
        `-> 0x00524dee      add   esp, 0x08
            0x00524df1      ret
            0x00524df2      int3
            0x00524df3      int3
            0x00524df4      int3
            0x00524df5      int3
            0x00524df6      int3
            0x00524df7      int3
            0x00524df8      int3
            0x00524df9      int3
            0x00524dfa      int3
            0x00524dfb      int3
            0x00524dfc      int3
            0x00524dfd      int3
            0x00524dfe      int3
            0x00524dff      int3
            0x00945d40      sub   esp, 0x14
            0x00945d43      mov   edx, dword [ecx]
            0x00945d45      mov   eax, 0x0e                            ; 0xe ; 14
            0x00945d4a      shr   edx, 0x1b
            0x00945d4d      push  ebx
            0x00945d4e      push  ebp
            0x00945d4f      mov   ebp, dword [ecx+0x04]
            0x00945d52      push  esi
            0x00945d53      lea   esi, dword [edx-0x01]
            0x00945d56      mov   dword [esp+0x1c], ebp
            0x00945d5a      cmp   esi, eax
            0x00945d5c      lea   ecx, dword [edx-0x01]
            0x00945d5f      mov   ebx, esi
            0x00945d61      cmovb ebx, eax
            0x00945d64      add   edx, 0xffffffe0                      ; 4294967264
            0x00945d67      push  edi
            0x00945d68      mov   edi, 0x01
            0x00945d6d      add   edx, ebx
            0x00945d6f      mov   eax, edi
            0x00945d71      shl   eax, cl
            0x00945d73      lea   ecx, dword [eax-0x01]
            0x00945d76      lea   eax, dword [eax*2-0x01]
            0x00945d7d      mov   dword [esp+0x1c], ecx
            0x00945d81      mov   dword [esp+0x10], eax
            0x00945d85      mov   ecx, esi
            0x00945d87      not   eax
            0x00945d89      mov   dword [esp+0x14], eax
            0x00945d8d      mov   eax, 0x14                            ; 20
            0x00945d92      shl   eax, cl
            0x00945d94      mov   ecx, 0x20                            ; 32
            0x00945d99      sub   ecx, ebx
            0x00945d9b      add   eax, ebp
            0x00945d9d      mov   ebp, dword [esp+0x2c]
            0x00945da1      shl   edi, cl
            0x00945da3      dec   edi
            0x00945da4      mov   dword [esp+0x18], eax
            0x00945da8      and   ebp, edi
            0x00945daa      mov   eax, 0x00
            0x00945daf      setz  al
            0x00945db2      xor   ecx, ecx
            0x00945db4      add   ebp, eax
            0x00945db6      mov   eax, dword [esp+0x30]
            0x00945dba      test  edx, edx
            0x00945dbc      mov   esi, ebp
            0x00945dbe      cmovnle ecx, edx
            0x00945dc1      shl   esi, cl
            0x00945dc3      mov   ecx, ebx
            0x00945dc5      and   esi, dword [esp+0x10]
            0x00945dc9      mov   ebx, dword [esp+0x18]
            0x00945dcd      shl   ebp, cl
            0x00945dcf      mov   ecx, dword [esp+0x14]
            0x00945dd3      and   ebp, ecx
            0x00945dd5      mov   dword [eax], 0x00
            0x00945ddb      nop   dword [eax+eax*1], eax
            0x00a95090      push  ebp
            0x00a95091      mov   ebp, esp
            0x00a95093      push  0xffffffff                           ; 255
            0x00a95095      push  0x186164c
            0x00a9509a      mov   eax, dword fs:[0x0]
            0x00a950a0      push  eax
            0x00a950a1      sub   esp, 0x14
            0x00a950a4      push  ebx
            0x00a950a5      push  esi
            0x00a950a6      push  edi
            0x00a950a7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00a950ac      xor   eax, ebp
            0x00a950ae      push  eax
            0x00a950af      lea   eax, dword [ebp-0x0c]
            0x00a950b2      mov   dword fs:[0x0], eax
            0x00a950b8      mov   eax, dword fs:[0x2c]
            0x00a950be      mov   ecx, dword [0x218e080]               ; [0x218e080:4]=0
            0x00a950c4      mov   ecx, dword [eax+ecx*4]
            0x00a950c7      mov   eax, dword [0x2027bec]               ; [0x2027bec:4]=0
            0x00a950cc      cmp   eax, dword [ecx+0x04]
        ,=< 0x00a950d2      jnle  0xa95180
      ..--> 0x00a950d8      mov   eax, dword [ebp+0x08]
      ::|   0x00a950db      xor   ebx, ebx
      ::|   0x00a950dd      xor   esi, esi
      ::|   0x00a950df      xor   edi, edi
      ::|   0x00a950e1      movzx edx, word [eax+0x02]
      ::|   0x00a950e5      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
      ::|   0x00a950ea      mov   ecx, dword [eax+0x74]
      ::|   0x00a950ed      imul  eax, edx, 0x404
      ::|   0x00a950f3      mov   dword [ebp-0x20], 0x00
      ::|   0x00a950fa      mov   dword [ebp-0x1c], 0x00
      ::|   0x00a95101      mov   dword [ebp-0x18], ebx
      ::|   0x00a95104      mov   dword [ebp-0x14], esi
      ::|   0x00a95107      mov   dword [ebp-0x10], edi
      ::|   0x00a9510a      mov   ecx, dword [eax+ecx*4+0x2027ed0]
      ::|   0x00a95111      mov   dword [ebp-0x20], ecx
      ::|   0x00a95114      test  ecx, ecx
     ,====< 0x00a95116      jz    0xa95169
     |::|   0x00a95118      mov   eax, dword [ecx]
     |::|   0x00a9511a      lea   edx, dword [ebp-0x14]
     |::|   0x00a9511d      push  edx
     |::|   0x00a9511e      lea   edx, dword [ebp-0x1c]
     |::|   0x00a95121      push  edx
     |::|   0x00a95122      call  dword [eax+0x3c]                     ; 60
     |::|   0x00a95125      mov   ecx, dword [ebp-0x20]
     |::|   0x00a95128      mov   edi, dword [ebp-0x10]
     |::|   0x00a9512b      mov   esi, dword [ebp-0x14]
     |::|   0x00a9512e      mov   ebx, dword [ebp-0x18]
     |::|   0x00a95131      test  ecx, ecx
    ,=====< 0x00a95133      jz    0xa95169
    ||::|   0x00a95135      mov   eax, dword [ebp+0x08]
    ||::|   0x00a95138      movzx ecx, word [eax]
    ||::|   0x00a9513b      cmp   ecx, ebx
   ,======< 0x00a9513d      jnb   0xa95169
   |||::|   0x00a9513f      mov   eax, dword [ebp-0x1c]
   |||::|   0x00a95142      mov   eax, dword [eax+ecx*4]
   |||::|   0x00a95145      test  eax, eax
  ,=======< 0x00a95147      jnz   0xa95154
  ||||::|   0x00a95149      cmp   ecx, edi
  ========< 0x00a9514b      jnb   0xa95169
  ||||::|   0x00a9514d      mov   eax, dword [esi+ecx*4]
  ||||::|   0x00a95150      test  eax, eax
  ========< 0x00a95152      jz    0xa95169
  `-------> 0x00a95154      add   eax, 0x10                            ; 16
   |||::|   0x00a95157      mov   ecx, dword [ebp-0x0c]
   |||::|   0x00a9515a      mov   dword fs:[0x0], ecx
   |||::|   0x00a95161      pop   ecx
   |||::|   0x00a95162      pop   edi
   |||::|   0x00a95163      pop   esi
   |||::|   0x00a95164      pop   ebx
   |||::|   0x00a95165      mov   esp, ebp
   |||::|   0x00a95167      pop   ebp
   |||::|   0x00a95168      ret
  -```----> 0x00a95169      mov   eax, 0x2027bdc
      ::|   0x00a9516e      mov   ecx, dword [ebp-0x0c]
      ::|   0x00a95171      mov   dword fs:[0x0], ecx
      ::|   0x00a95178      pop   ecx
      ::|   0x00a95179      pop   edi
      ::|   0x00a9517a      pop   esi
      ::|   0x00a9517b      pop   ebx
      ::|   0x00a9517c      mov   esp, ebp
      ::|   0x00a9517e      pop   ebp
      ::|   0x00a9517f      ret
      ::`-> 0x00a95180      push  0x2027bec
      ::    0x00a95185      call  0x1806ee7
      ::    0x00a9518a      add   esp, 0x04
      ::    0x00a9518d      cmp   dword [0x2027bec], 0xffffffff        ; [0x2027bec:4]=0
      `===< 0x00a95194      jnz   0xa950d8
       :    0x00a9519a      push  0x1908ad0
       :    0x00a9519f      mov   dword [ebp-0x04], 0x00
       :    0x00a951a6      call  0x18073e6
       :    0x00a951ab      push  0x2027bec
       :    0x00a951b0      mov   dword [ebp-0x04], 0xffffffff         ; -1
       :    0x00a951b7      call  0x1806e9d
       :    0x00a951bc      add   esp, 0x08
       `==< 0x00a951bf      jmp   0xa950d8
            0x00a951c4      int3
            0x00a951c5      int3
            0x00a951c6      int3
            0x00a951c7      int3
            0x00a951c8      int3
            0x00a951c9      int3
            0x00a951ca      int3
            0x00a951cb      int3
            0x00a951cc      int3
            0x00a951cd      int3
            0x00a951ce      int3
            0x00a951cf      int3
            0x00a951d0      push  ebp
            0x00a951d1      mov   ebp, esp
            0x00a951d3      push  0xffffffff                           ; 255
            0x00a951d5      push  0x186167c
            0x00a951da      mov   eax, dword fs:[0x0]
            0x00a951e0      push  eax
            0x00a951e1      sub   esp, 0x14
            0x00a951e4      push  ebx
            0x00a951e5      push  esi
            0x00a951e6      push  edi
            0x00a951e7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00a951ec      xor   eax, ebp
            0x00a951ee      push  eax
            0x00a951ef      lea   eax, dword [ebp-0x0c]
            0x00a951f2      mov   dword fs:[0x0], eax
            0x00a951f8      mov   eax, dword fs:[0x2c]
            0x00a951fe      mov   ecx, dword [0x218e080]               ; [0x218e080:4]=0
            0x00a95204      mov   ecx, dword [eax+ecx*4]
            0x00a95207      mov   eax, dword [0x2027c00]               ; [0x2027c00:4]=0
            0x00a9520c      cmp   eax, dword [ecx+0x04]
        ,=< 0x00a95212      jnle  0xa952c0
        |   0x00a95218      mov   eax, dword [ebp+0x08]
        |   0x00a9521b      xor   ebx, ebx
        |   0x00a9521d      xor   esi, esi
        |   0x00a9521f      xor   edi, edi
        |   0x00a95221      movzx edx, word [eax+0x02]
        |   0x00a95225      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
        |   0x00a9522a      mov   ecx, dword [eax+0x74]
        |   0x00a9522d      imul  eax, edx, 0x404
        |   0x00a95233      mov   dword [ebp-0x20], 0x00
        |   0x00a9523a      mov   dword [ebp-0x1c], 0x00
        |   0x00a95241      mov   dword [ebp-0x18], ebx
        |   0x00a95244      mov   dword [ebp-0x14], esi
        |   0x00a95247      mov   dword [ebp-0x10], edi
        |   0x00a9524a      mov   ecx, dword [eax+ecx*4+0x2027ed0]
        |   0x00a95251      mov   dword [ebp-0x20], ecx
        |   0x00a95254      test  ecx, ecx
       ,==< 0x00a95256      jz    0xa952a9
       ||   0x00a95258      mov   eax, dword [ecx]
       ||   0x00a9525a      lea   edx, dword [ebp-0x14]
       ||   0x00a9525d      push  edx
       ||   0x00a9525e      lea   edx, dword [ebp-0x1c]
       ||   0x00a95261      push  edx
       ||   0x00a95262      call  dword [eax+0x40]                     ; 64
       ||   0x00a95265      mov   ecx, dword [ebp-0x20]
       ||   0x00a95268      mov   edi, dword [ebp-0x10]
       ||   0x00a9526b      mov   esi, dword [ebp-0x14]
       ||   0x00a9526e      invalid
       ||   0x00a9526f      pop   ebp
        `=< 0x00cc0310      loopne 0xcc0297
            0x00cc0312      leave
        ,=< 0x00cc0313      jz    0xcc036b
        |   0x00cc0315      mov   eax, dword [ecx]
        |   0x00cc0317      lea   edx, dword [ebp-0x14]
        |   0x00cc031a      push  edx
        |   0x00cc031b      lea   edx, dword [ebp-0x1c]
        |   0x00cc031e      push  edx
        |   0x00cc031f      call  dword [eax+0x3c]                     ; 60
        |   0x00cc0322      mov   ecx, dword [ebp-0x20]
        |   0x00cc0325      mov   esi, dword [ebp-0x10]
        |   0x00cc0328      mov   edx, dword [ebp-0x14]
        |   0x00cc032b      mov   edi, dword [ebp-0x18]
        |   0x00cc032e      mov   ebx, dword [ebp-0x1c]
        |   0x00cc0331      test  ecx, ecx
       ,==< 0x00cc0333      jz    0xcc036b
       ||   0x00cc0335      mov   eax, dword [ebp+0x08]
       ||   0x00cc0338      movzx ecx, word [eax]
       ||   0x00cc033b      cmp   ecx, edi
      ,===< 0x00cc033d      jnb   0xcc036b
      |||   0x00cc033f      mov   eax, dword [ebx+ecx*4]
      |||   0x00cc0342      test  eax, eax
     ,====< 0x00cc0344      jnz   0xcc0351
     ||||   0x00cc0346      cmp   ecx, esi
    ,=====< 0x00cc0348      jnb   0xcc036b
    |||||   0x00cc034a      mov   eax, dword [edx+ecx*4]
    |||||   0x00cc034d      test  eax, eax
   ,======< 0x00cc034f      jz    0xcc036b
   ||`----> 0x00cc0351      cmp   dword [eax+0x28], 0x01
   ||,====< 0x00cc0355      jnz   0xcc036b
   ||||||   0x00cc0357      mov   al, 0x01
   ||||||   0x00cc0359      mov   ecx, dword [ebp-0x0c]
   ||||||   0x00cc035c      mov   dword fs:[0x0], ecx
   ||||||   0x00cc0363      pop   ecx
   ||||||   0x00cc0364      pop   edi
   ||||||   0x00cc0365      pop   esi
   ||||||   0x00cc0366      pop   ebx
   ||||||   0x00cc0367      mov   esp, ebp
   ||||||   0x00cc0369      pop   ebp
   ||||||   0x00cc036a      ret
   ``````-> 0x00cc036b      xor   al, al
            0x00cc036d      mov   ecx, dword [ebp-0x0c]
            0x00cc0370      mov   dword fs:[0x0], ecx
            0x00cc0377      pop   ecx
            0x00cc0378      pop   edi
            0x00cc0379      pop   esi
            0x00cc037a      pop   ebx
            0x00cc037b      mov   esp, ebp
            0x00cc037d      pop   ebp
            0x00cc037e      ret
            0x00cc037f      int3
            0x00cc0380      push  ebp
            0x00cc0381      mov   ebp, esp
            0x00cc0383      push  0xffffffff                           ; 255
            0x00cc0385      push  0x1880218
            0x00cc038a      mov   eax, dword fs:[0x0]
            0x00cc0390      push  eax
            0x00cc0391      sub   esp, 0x28
            0x00cc0394      push  ebx
            0x00cc0395      push  esi
            0x00cc0396      push  edi
            0x00cc0397      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00cc039c      xor   eax, ebp
            0x00cc039e      push  eax
            0x00cc039f      lea   eax, dword [ebp-0x0c]
            0x00cc03a2      mov   dword fs:[0x0], eax
            0x00cc03a8      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00cc03ad      xor   edi, edi
            0x00cc03af      xor   ebx, ebx
            0x00cc03b1      xor   edx, edx
            0x00cc03b3      xor   esi, esi
            0x00cc03b5      mov   eax, dword [eax+0x148]
            0x00cc03bb      mov   dword [ebp-0x1c], edi
            0x00cc03be      mov   dword [ebp-0x18], ebx
            0x00cc03c1      mov   dword [ebp-0x14], edx
            0x00cc03c4      mov   ecx, dword [eax*4+0x2027ed0]
            0x00cc03cb      mov   dword [ebp-0x10], esi
            0x00cc03ce      mov   dword [ebp-0x20], ecx
            0x00cc03d1      test  ecx, ecx
        ,=< 0x00cc03d3      jz    0xcc03f1
        |   0x00cc03d5      mov   eax, dword [ecx]
        |   0x00cc03d7      lea   edx, dword [ebp-0x14]
        |   0x00cc03da      push  edx
        |   0x00cc03db      lea   edx, dword [ebp-0x1c]
        |   0x00cc03de      push  edx
        |   0x00cc03df      call  dword [eax+0x3c]                     ; 60
        |   0x00cc03e2      mov   esi, dword [ebp-0x10]
        |   0x00cc03e5      mov   edx, dword [ebp-0x14]
        |   0x00cc03e8      mov   ebx, dword [ebp-0x18]
        |   0x00cc03eb      mov   edi, dword [ebp-0x1c]
        |   0x00cc03ee      mov   ecx, dword [ebp-0x20]
        `-> 0x00cc03f1      mov   dword [ebp-0x04], 0x00
            0x00cc03f8      test  ecx, ecx
        ,=< 0x00cc03fa      jz    0xcc0416
        |   0x00cc03fc      mov   eax, dword [ebp+0x08]
        |   0x00cc03ff      xor   ecx, ecx
        |   0x00cc0401      movzx eax, word [eax]
        |   0x00cc0404      cmp   eax, ebx
       ,==< 0x00cc0406      jnb   0xcc0416
       ||   0x00cc0408      mov   ecx, dword [edi+eax*4]
       ||   0x00cc040b      test  ecx, ecx
      ,===< 0x00cc040d      jnz   0xcc0416
      |||   0x00cc040f      cmp   eax, esi
     ,====< 0x00cc0411      jnb   0xcc0416
     ||||   0x00cc0413      mov   ecx, dword [edx+eax*4]
     ````-> 0x00cc0416      call  0x518880
            0x00cc041b      mov   ecx, dword [0x201f660]               ; [0x201f660:4]=0
            0x00cc0421      mov   ebx, eax
            0x00cc0423      xor   eax, eax
            0x00cc0425      xor   edi, edi
            0x00cc0427      xor   edx, edx
            0x00cc0429      xor   esi, esi
            0x00cc042b      mov   ecx, dword [ecx+0x108]
            0x00cc0431      mov   dword [ebp-0x30], eax
            0x00cc0434      mov   dword [ebp-0x2c], edi
            0x00cc0437      mov   dword [ebp-0x28], edx
            0x00cc043a      mov   ecx, dword [ecx*4+0x2027ed0]
            0x00cc0441      mov   dword [ebp-0x24], esi
            0x00cc0444      mov   dword [ebp-0x34], ecx
            0x00cc0447      test  ecx, ecx
        ,=< 0x00cc0449      jz    0xcc048e
        |   0x00cc044b      mov   eax, dword [ecx]
        |   0x00cc044d      lea   edx, dword [ebp-0x28]
        |   0x00cc0450      push  edx
        |   0x00cc0451      lea   edx, dword [ebp-0x30]
        |   0x00cc0454      push  edx
        |   0x00cc0455      call  dword [eax+0x3c]                     ; 60
        |   0x00cc0458      mov   ecx, dword [ebp-0x34]
        |   0x00cc045b      mov   esi, dword [ebp-0x24]
        |   0x00cc045e      invalid
        |   0x00cc045f      push  ebp
