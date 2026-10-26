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
        `-> 0x00b2470c      mov   dword [ebp-0x04], 0x00
            0x00b24713      test  ecx, ecx
        ,=< 0x00b24715      jz    0xb24727
        |   0x00b24717      mov   eax, dword [ebp+0x08]
        |   0x00b2471a      movzx ecx, word [eax+0x20]
        |   0x00b2471e      cmp   ecx, esi
       ,==< 0x00b24720      jnb   0xb24727
       ||   0x00b24722      mov   ecx, dword [edx+ecx*4]
      ,===< 0x00b24725      jmp   0xb24729
      |``-> 0x00b24727      xor   ecx, ecx
      `---> 0x00b24729      push  dword [ebp+0x0c]
            0x00b2472c      call  0xc182a0
            0x00b24731      mov   esi, eax
            0x00b24733      push  dword [ebp+0x10]
            0x00b24736      mov   ecx, esi
            0x00b24738      mov   dword [ebp-0x18], 0x00
            0x00b2473f      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b24746      call  0xba6310
            0x00b2474b      test  eax, eax
        ,=< 0x00b2474d      jz    0xb24757
        |   0x00b2474f      push  eax
        |   0x00b24750      mov   ecx, esi
        |   0x00b24752      call  0xba5990
        `-> 0x00b24757      mov   ecx, dword [ebp-0x0c]
            0x00b2475a      mov   dword fs:[0x0], ecx
            0x00b24761      pop   ecx
            0x00b24762      pop   esi
            0x00b24763      mov   esp, ebp
            0x00b24765      pop   ebp
            0x00b24766      ret   0x0c
            0x00b24769      int3
            0x00b2476a      int3
            0x00b2476b      int3
            0x00b2476c      int3
            0x00b2476d      int3
            0x00b2476e      int3
            0x00b2476f      int3
            0x00b24770      mov   edx, dword [esp+0x08]
            0x00b24774      mov   eax, dword [esp+0x04]
            0x00b24778      mov   ecx, dword [edx]
            0x00b2477a      mov   dword [eax], ecx
            0x00b2477c      mov   ecx, dword [edx+0x04]
            0x00b2477f      mov   dword [eax+0x04], ecx
            0x00b24782      mov   dword [eax+0x08], 0xffff03ff         ; [0xffff03ff:4]=-1
            0x00b24789      ret
            0x00b2478a      int3
            0x00b2478b      int3
            0x00b2478c      int3
            0x00b2478d      int3
            0x00b2478e      int3
            0x00b2478f      int3
            0x00b24790      mov   dword [ecx+0x160], 0x00
            0x00b2479a      ret
            0x00b2479b      int3
            0x00b2479c      int3
            0x00b2479d      int3
            0x00b2479e      int3
            0x00b2479f      int3
            0x00b247a0      sub   esp, 0x1c
            0x00b247a3      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b247a8      xor   eax, esp
            0x00b247aa      mov   dword [esp+0x18], eax
            0x00b247ae      push  esi
            0x00b247af      mov   esi, dword [esp+0x24]
            0x00b247b3      push  edi
            0x00b247b4      mov   edi, ecx
            0x00b247b6      mov   eax, dword [edi]
            0x00b247b8      call  dword [eax+0xb4]                     ; 180
            0x00b247be      mov   ecx, eax
            0x00b247c0      test  ecx, ecx
        ,=< 0x00b247c2      jz    0xb24809
        |   0x00b247c4      mov   eax, dword [ecx]
        |   0x00b247c6      lea   edx, dword [esp+0x08]
        |   0x00b247ca      push  edx
        |   0x00b247cb      call  dword [eax+0x04]                     ; 4
        |   0x00b247ce      mov   dword [esp+0x14], 0x7f800000         ; [0x7f800000:4]=-1
        |   0x00b247d6      xor   ecx, ecx
        |   0x00b247d8      mov   dword [esp+0x18], 0x7f800000         ; [0x7f800000:4]=-1
        |   0x00b247e0      mov   dword [esp+0x1c], 0x7f800000         ; [0x7f800000:4]=-1
        |   0x00b247e8      nop   dword [eax+eax*1], eax
       .--> 0x00b247f0      movss xmm0, dword [esp+ecx*1+0x08]
       :|   0x00b247f6      ucomiss xmm0, dword [esp+ecx*1+0x14]
       :|   0x00b247fb      lahf
       :|   0x00b247fc      test  ah, 0x44                             ; 68
      ,===< 0x00b247ff      jp    0xb2483b
      |:|   0x00b24801      add   ecx, 0x04
      |:|   0x00b24804      cmp   ecx, 0x0c                            ; 0xc ; 12
      |`==< 0x00b24807      jb    0xb247f0
      | `-> 0x00b24809      movss xmm0, dword [edi+0x4c]
      |     0x00b2480e      mov   eax, esi
      |     0x00b24810      movss xmm1, dword [edi+0x50]
      |     0x00b24815      movss xmm2, dword [edi+0x54]
      |     0x00b2481a      pop   edi
      |     0x00b2481b      movss dword [esi], xmm0
      |     0x00b2481f      movss dword [esi+0x04], xmm1
      |     0x00b24824      movss dword [esi+0x08], xmm2
      |     0x00b24829      pop   esi
      |     0x00b2482a      mov   ecx, dword [esp+0x18]
      |     0x00b2482e      xor   ecx, esp
      |     0x00b24830      call  0x18075f6
      |     0x00b24835      add   esp, 0x1c
      |     0x00b24838      ret   0x04
      `---> 0x00b2483b      movss xmm0, dword [esp+0x08]
            0x00b24841      mov   eax, esi
            0x00b24843      mov   ecx, dword [esp+0x20]
            0x00b24847      movss dword [esi], xmm0
            0x00b2484b      movss xmm0, dword [esp+0x0c]
            0x00b24851      movss dword [esi+0x04], xmm0
            0x00b24856      movss xmm0, dword [esp+0x10]
            0x00b2485c      pop   edi
            0x00b2485d      movss dword [esi+0x08], xmm0
            0x00b24862      pop   esi
            0x00b24863      xor   ecx, esp
            0x00b24865      call  0x18075f6
            0x00b2486a      add   esp, 0x1c
            0x00b2486d      ret   0x04
            0x00b24870      sub   esp, 0x0c
            0x00b24873      movzx eax, word [esp+0x10]
            0x00b24878      push  esi
            0x00b24879      mov   esi, ecx
            0x00b2487b      mov   dword [esp+0x08], eax
            0x00b2487f      shr   ax, 0x04
            0x00b24883      movzx edx, ax
            0x00b24886      push  edi
            0x00b24887      mov   eax, dword [esi+0x168]
            0x00b2488d      cmp   byte [eax+edx*1], 0x00
        ,=< 0x00b24891      jnz   0xb248d2
        |   0x00b24893      mov   byte [edx+eax*1], 0x01
        |   0x00b24897      mov   ecx, dword [esi+0x158]
        |   0x00b2489d      mov   edi, dword [esi+0x154]
        |   0x00b248a3      shl   edx, 0x04
        |   0x00b248a6      lea   eax, dword [edx+0x10]
        |   0x00b248a9      cmp   eax, ecx
       ,==< 0x00b248ab      jnbe  0xb248c5
       ||   0x00b248ad      xorps xmm0, xmm0
       ||   0x00b248b0      movups xmmword [edi+edx*4], xmm0
       ||   0x00b248b4      movups xmmword [edi+edx*4+0x10], xmm0
       ||   0x00b248b9      movups xmmword [edi+edx*4+0x20], xmm0
       ||   0x00b248be      movups xmmword [edi+edx*4+0x30], xmm0
      ,===< 0x00b248c3      jmp   0xb248d2
      |`--> 0x00b248c5      cmp   edx, ecx
      |,==< 0x00b248c7      jnb   0xb248d2
      |||   0x00b248c9      sub   ecx, edx
      |||   0x00b248cb      lea   edi, dword [edi+edx*4]
      |||   0x00b248ce      xor   eax, eax
      |||   0x00b248d0      rep   stosd
      ```-> 0x00b248d2      mov   eax, dword [esp+0x0c]
            0x00b248d6      movzx edi, ax
            0x00b248d9      mov   eax, dword [esi+0x154]
            0x00b248df      invalid
            0x00b2e760      push  ebp
            0x00b2e761      mov   ebp, esp
            0x00b2e763      push  0xffffffff                           ; 255
            0x00b2e765      push  0x186932b
            0x00b2e76a      mov   eax, dword fs:[0x0]
            0x00b2e770      push  eax
            0x00b2e771      push  ecx
            0x00b2e772      push  ebx
            0x00b2e773      push  esi
            0x00b2e774      push  edi
            0x00b2e775      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2e77a      xor   eax, ebp
            0x00b2e77c      push  eax
            0x00b2e77d      lea   eax, dword [ebp-0x0c]
            0x00b2e780      mov   dword fs:[0x0], eax
            0x00b2e786      push  dword [0x1d6c084]
            0x00b2e78c      push  0x01                                 ; 1
            0x00b2e78e      push  0x2c                                 ; ',' ; 44
            0x00b2e790      push  0x01                                 ; 1
            0x00b2e792      call  0x529280
            0x00b2e797      mov   esi, eax
            0x00b2e799      add   esp, 0x10
            0x00b2e79c      mov   dword [ebp-0x10], esi
            0x00b2e79f      mov   dword [ebp-0x04], 0x00
            0x00b2e7a6      test  esi, esi
        ,=< 0x00b2e7a8      jz    0xb2e7d4
        |   0x00b2e7aa      mov   ecx, esi
        |   0x00b2e7ac      call  0xb21f60
        |   0x00b2e7b1      mov   dword [esi], 0x19a1908               ; [0x19a1908:4]=0x561c50
        |   0x00b2e7b7      lea   ecx, dword [esi+0x08]
        |   0x00b2e7ba      mov   byte [ebp-0x04], 0x01
        |   0x00b2e7be      mov   dword [esi+0x04], 0x00
        |   0x00b2e7c5      call  0x4f71f0
        |   0x00b2e7ca      lea   ecx, dword [esi+0x18]
        |   0x00b2e7cd      call  0x4f71f0
       ,==< 0x00b2e7d2      jmp   0xb2e7d6
       |`-> 0x00b2e7d4      xor   esi, esi
       `--> 0x00b2e7d6      mov   edi, dword [ebp+0x08]
            0x00b2e7d9      lea   ebx, dword [esi+0x04]
            0x00b2e7dc      push  0x04                                 ; 4
            0x00b2e7de      push  ebx
            0x00b2e7df      mov   ecx, edi
            0x00b2e7e1      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b2e7e8      mov   eax, dword [edi]
            0x00b2e7ea      mov   eax, dword [eax+0x04]
            0x00b2e7ed      call  eax
            0x00b2e7ef      test  al, al
        ,=< 0x00b2e7f1      jz    0xb2e840
        |   0x00b2e7f3      mov   eax, dword [edi]
        |   0x00b2e7f5      mov   ecx, edi
        |   0x00b2e7f7      push  0x10                                 ; 16
        |   0x00b2e7f9      mov   edx, dword [eax+0x04]
        |   0x00b2e7fc      lea   eax, dword [ebx+0x04]
        |   0x00b2e7ff      push  eax
        |   0x00b2e800      call  edx
        |   0x00b2e802      test  al, al
       ,==< 0x00b2e804      jz    0xb2e840
       ||   0x00b2e806      mov   eax, dword [edi]
       ||   0x00b2e808      mov   ecx, edi
       ||   0x00b2e80a      push  0x10                                 ; 16
       ||   0x00b2e80c      mov   edx, dword [eax+0x04]
       ||   0x00b2e80f      lea   eax, dword [esi+0x18]
       ||   0x00b2e812      push  eax
       ||   0x00b2e813      call  edx
       ||   0x00b2e815      test  al, al
      ,===< 0x00b2e817      jz    0xb2e840
      |||   0x00b2e819      mov   eax, dword [edi]
      |||   0x00b2e81b      mov   ecx, edi
      |||   0x00b2e81d      push  0x04                                 ; 4
      |||   0x00b2e81f      mov   edx, dword [eax+0x04]
      |||   0x00b2e822      lea   eax, dword [esi+0x28]
      |||   0x00b2e825      push  eax
      |||   0x00b2e826      call  edx
      |||   0x00b2e828      test  al, al
     ,====< 0x00b2e82a      jz    0xb2e840
     ||||   0x00b2e82c      mov   eax, esi
     ||||   0x00b2e82e      mov   ecx, dword [ebp-0x0c]
     ||||   0x00b2e831      mov   dword fs:[0x0], ecx
     ||||   0x00b2e838      pop   ecx
     ||||   0x00b2e839      pop   edi
     ||||   0x00b2e83a      pop   esi
     ||||   0x00b2e83b      pop   ebx
     ||||   0x00b2e83c      mov   esp, ebp
     ||||   0x00b2e83e      pop   ebp
     ||||   0x00b2e83f      ret
     ````-> 0x00b2e840      test  esi, esi
        ,=< 0x00b2e842      jz    0xb2e84d
        |   0x00b2e844      mov   eax, dword [esi]
        |   0x00b2e846      mov   ecx, esi
        |   0x00b2e848      push  0x01                                 ; 1
        |   0x00b2e84a      call  dword [eax+0x08]                     ; 8
        `-> 0x00b2e84d      xor   eax, eax
            0x00b2e84f      mov   ecx, dword [ebp-0x0c]
            0x00b2e852      mov   dword fs:[0x0], ecx
            0x00b2e859      pop   ecx
            0x00b2e85a      pop   edi
            0x00b2e85b      pop   esi
            0x00b2e85c      pop   ebx
            0x00b2e85d      mov   esp, ebp
            0x00b2e85f      pop   ebp
            0x00b2e860      ret
            0x00b2e861      int3
            0x00b2e862      int3
            0x00b2e863      int3
            0x00b2e864      int3
            0x00b2e865      int3
            0x00b2e866      int3
            0x00b2e867      int3
            0x00b2e868      int3
            0x00b2e869      int3
            0x00b2e86a      int3
            0x00b2e86b      int3
            0x00b2e86c      int3
            0x00b2e86d      int3
            0x00b2e86e      int3
            0x00b2e86f      int3
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
        |   0x00b2e8bc      invalid
        |   0x00b2e8bd      lahf
        |   0x00b2e8be      invalid
        |   0x00b2e8bf      invalid
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
        |   0x00c0972f      mov   ecx, dword [ebx+0x08]
        |   0x00c09732      call  0xb7ba40
        |   0x00c09737      test  al, al
       ,==< 0x00c09739      jnz   0xc097c7
       ||   0x00c0973f      push  0x00
       ||   0x00c09741      push  0x00
       ||   0x00c09743      push  dword [0x202731c]
       ||   0x00c09749      mov   ecx, edi
       ||   0x00c0974b      call  0xbcdcd0
       ||   0x00c09750      mov   ecx, dword [ebp-0x10]
       ||   0x00c09753      neg   eax
       ||   0x00c09755      push  eax
       ||   0x00c09756      push  dword [ebp-0x18]
       ||   0x00c09759      call  0xb78c30
       ||   0x00c0975e      lea   ecx, dword [ebp-0x14]
       ||   0x00c09761      call  0x4f6c50
       ||   0x00c09766      mov   eax, dword [ebx]
       ||   0x00c09768      mov   ecx, ebx
       ||   0x00c0976a      mov   byte [ebp-0x04], 0x09
       ||   0x00c0976e      call  dword [eax+0x20]                     ; 32
       ||   0x00c09771      mov   ecx, eax
       ||   0x00c09773      call  0xba8ff0
       ||   0x00c09778      lea   ecx, dword [ebp-0x14]
       ||   0x00c0977b      push  ecx
       ||   0x00c0977c      push  eax
       ||   0x00c0977d      mov   ecx, ebx
       ||   0x00c0977f      call  0xc0bec0
       ||   0x00c09784      mov   dword [ebp-0x18], eax
       ||   0x00c09787      test  eax, eax
      ,===< 0x00c09789      jz    0xc097ab
      |||   0x00c0978b      mov   ecx, dword [ebp+0x08]
      |||   0x00c0978e      test  ecx, ecx
     ,====< 0x00c09790      jz    0xc0979b
     ||||   0x00c09792      lea   eax, dword [ebp-0x18]
     ||||   0x00c09795      push  eax
     ||||   0x00c09796      call  0x750590
     `----> 0x00c0979b      mov   ecx, dword [ebp+0x0c]
      |||   0x00c0979e      test  ecx, ecx
     ,====< 0x00c097a0      jz    0xc097ab
     ||||   0x00c097a2      lea   eax, dword [ebp-0x14]
     ||||   0x00c097a5      push  eax
     ||||   0x00c097a6      call  0xac3200
     ``---> 0x00c097ab      lea   ecx, dword [ebp-0x14]
       ||   0x00c097ae      call  0x4dc500
       ||   0x00c097b3      mov   ecx, dword [ebp-0x0c]
       ||   0x00c097b6      mov   dword fs:[0x0], ecx
       ||   0x00c097bd      pop   ecx
       ||   0x00c097be      pop   edi
       ||   0x00c097bf      pop   esi
       ||   0x00c097c0      pop   ebx
       ||   0x00c097c1      mov   esp, ebp
       ||   0x00c097c3      pop   ebp
       ||   0x00c097c4      ret   0x08
       ``-> 0x00c097c7      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c097cc      mov   eax, dword [eax+0xd8]
            0x00c097d2      mov   dword [ebp-0x2c], 0x00
            0x00c097d9      mov   dword [ebp-0x28], 0x00
            0x00c097e0      mov   ecx, dword [eax*4+0x20286d8]
            0x00c097e7      mov   dword [ebp-0x30], ecx
            0x00c097ea      test  ecx, ecx
        ,=< 0x00c097ec      jz    0xc097f9
        |   0x00c097ee      mov   eax, dword [ecx]
        |   0x00c097f0      lea   edx, dword [ebp-0x2c]
        |   0x00c097f3      push  0x00
        |   0x00c097f5      push  edx
        |   0x00c097f6      call  dword [eax+0x40]                     ; 64
        `-> 0x00c097f9      mov   ecx, ebx
            0x00c097fb      mov   byte [ebp-0x04], 0x06
            0x00c097ff      call  0xc0eb40
            0x00c09804      mov   ecx, dword [ebp-0x0c]
            0x00c09807      mov   dword fs:[0x0], ecx
            0x00c0980e      pop   ecx
            0x00c0980f      pop   edi
            0x00c09810      pop   esi
            0x00c09811      pop   ebx
            0x00c09812      mov   esp, ebp
            0x00c09814      pop   ebp
            0x00c09815      ret   0x08
            0x00c09818      int3
            0x00c09819      int3
            0x00c0981a      int3
            0x00c0981b      int3
            0x00c0981c      int3
            0x00c0981d      int3
            0x00c0981e      int3
            0x00c0981f      int3
            0x00c09820      push  ebp
            0x00c09821      mov   ebp, esp
            0x00c09823      push  0xffffffff                           ; 255
            0x00c09825      push  0x1876328
            0x00c0982a      mov   eax, dword fs:[0x0]
            0x00c09830      push  eax
            0x00c09831      sub   esp, 0x60
            0x00c09834      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c09839      xor   eax, ebp
            0x00c0983b      mov   dword [ebp-0x10], eax
            0x00c0983e      push  ebx
            0x00c0983f      push  esi
            0x00c09840      push  edi
            0x00c09841      push  eax
            0x00c09842      lea   eax, dword [ebp-0x0c]
            0x00c09845      mov   dword fs:[0x0], eax
            0x00c0984b      mov   edi, ecx
            0x00c0984d      mov   dword [ebp-0x64], edi
            0x00c09850      mov   eax, dword [ebp+0x08]
            0x00c09853      xor   edx, edx
            0x00c09855      mov   ebx, dword [edi+0x08]
            0x00c09858      xor   esi, esi
            0x00c0985a      mov   dword [ebp-0x4c], eax
            0x00c0985d      mov   eax, dword [ebp+0x0c]
            0x00c09860      mov   dword [ebp-0x50], eax
            0x00c09863      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c09868      mov   eax, dword [eax+0xd8]
            0x00c0986e      mov   dword [ebp-0x58], edx
            0x00c09871      mov   dword [ebp-0x54], esi
            0x00c09874      mov   ecx, dword [eax*4+0x20286d8]
            0x00c0987b      mov   dword [ebp-0x5c], ecx
            0x00c0987e      test  ecx, ecx
        ,=< 0x00c09880      jz    0xc09895
        |   0x00c09882      mov   eax, dword [ecx]
        |   0x00c09884      lea   edx, dword [ebp-0x58]
        |   0x00c09887      push  esi
        |   0x00c09888      push  edx
        |   0x00c09889      call  dword [eax+0x40]                     ; 64
        |   0x00c0988c      mov   esi, dword [ebp-0x54]
        |   0x00c0988f      mov   edx, dword [ebp-0x58]
        |   0x00c09892      mov   ecx, dword [ebp-0x5c]
        `-> 0x00c09895      mov   dword [ebp-0x04], 0x00
            0x00c0989c      test  ecx, ecx
        ,=< 0x00c0989e      jz    0xc098ad
        |   0x00c098a0      movzx eax, word [ebx+0x20]
        |   0x00c098a4      cmp   eax, esi
       ,==< 0x00c098a6      jnb   0xc098ad
       ||   0x00c098a8      mov   ecx, dword [edx+eax*4]
      ,===< 0x00c098ab      jmp   0xc098af
      |``-> 0x00c098ad      xor   ecx, ecx
      `---> 0x00c098af      mov   eax, dword [0x203cfa8]               ; [0x203cfa8:4]=0
            0x00c098b4      mov   dword [ebp-0x38], ecx
            0x00c098b7      mov   eax, dword [eax+0x1c]
            0x00c098ba      push  eax
            0x00c098bb      mov   dword [ebp-0x48], eax
            0x00c098be      call  0xb7d600
            0x00c098c3      cmp   byte [edi+0x95], 0x00
            0x00c098ca      mov   ebx, eax
        ,=< 0x00c098cc      jnz   0xc098ee
        |   0x00c098ce      mov   ecx, edi
        |   0x00c098d0      call  0xc0ce90
        |   0x00c098d5      mov   ecx, ebx
        |   0x00c098d7      mov   esi, eax
        |   0x00c098d9      call  0xb47e90
        |   0x00c098de      cmp   eax, esi
       ,==< 0x00c098e0      jnl   0xc098ee
       ||   0x00c098e2      mov   ecx, edi
       ||   0x00c098e4      call  0xc0ec40
      ,===< 0x00c098e9      jmp   0xc09bdd
      |``-> 0x00c098ee      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
      |     0x00c098f3      xor   edx, edx
      |     0x00c098f5      xor   esi, esi
      |     0x00c098f7      mov   eax, dword [eax+0x210]
      |     0x00c098fd      mov   dword [ebp-0x18], edx
      |     0x00c09900      mov   dword [ebp-0x14], esi
      |     0x00c09903      mov   ecx, dword [eax*4+0x20286d8]
      |     0x00c0990a      mov   dword [ebp-0x1c], ecx
      |     0x00c0990d      test  ecx, ecx
      | ,=< 0x00c0990f      jz    0xc09924
      | |   0x00c09911      mov   eax, dword [ecx]
      | |   0x00c09913      lea   edx, dword [ebp-0x18]
      | |   0x00c09916      push  esi
      | |   0x00c09917      push  edx
      | |   0x00c09918      call  dword [eax+0x3c]                     ; 60
      | |   0x00c0991b      mov   esi, dword [ebp-0x14]
      | |   0x00c0991e      mov   edx, dword [ebp-0x18]
      | |   0x00c09921      mov   ecx, dword [ebp-0x1c]
      | `-> 0x00c09924      mov   eax, dword [edi+0x08]
      |     0x00c09927      mov   byte [ebp-0x04], 0x02
      |     0x00c0992b      test  ecx, ecx
      | ,=< 0x00c0992d      jz    0xc0998e
      | |   0x00c0992f      movzx eax, word [eax+0x20]
      | |   0x00c09933      cmp   eax, esi
      |,==< 0x00c09935      jnb   0xc0998e
      |||   0x00c09937      mov   ecx, dword [edx+eax*4]
      |||   0x00c0993a      mov   dword [ebp-0x3c], ecx
      |||   0x00c0993d      test  ecx, ecx
     ,====< 0x00c0993f      jz    0xc0998e
     ||||   0x00c09941      xor   eax, eax
     ||||   0x00c09943      xor   esi, esi
     ||||   0x00c09945      cmp   dword [edi+0x70], eax
    ,=====< 0x00c09948      jz    0xc0996b
    |||||   0x00c0994a      lea   edx, dword [esi-0x10]
    |||||   0x00c0994d      lea   ebx, dword [edi+0x84]
   .------> 0x00c09953      mov   ecx, ebx
   :|||||   0x00c09955      cmp   eax, 0x04                            ; 4
  ,=======< 0x00c09958      jb    0xc0995c
  |:|||||   0x00c0995a      mov   ecx, dword [ebx]
  `-------> 0x00c0995c      add   esi, dword [ecx+edx*1]
   :|||||   0x00c0995f      inc   eax
   :|||||   0x00c09960      add   edx, 0x04
   :|||||   0x00c09963      cmp   eax, dword [edi+0x70]
   `======< 0x00c09966      jnz   0xc09953
    |||||   0x00c09968      mov   ecx, dword [ebp-0x3c]
    `-----> 0x00c0996b      cmp   byte [edi+0x96], 0x00
    ,=====< 0x00c09972      jz    0xc0998e
    |||||   0x00c09974      push  esi
    |||||   0x00c09975      lea   eax, dword [edi+0x0c]
    |||||   0x00c09978      push  eax
    |||||   0x00c09979      call  0xbf29f0
    |||||   0x00c0997e      test  al, al
   ,======< 0x00c09980      jnz   0xc0998e
   ||||||   0x00c09982      mov   ecx, edi
   ||||||   0x00c09984      call  0xc0ec40
  ,=======< 0x00c09989      jmp   0xc09bdd
  |```-``-> 0x00c0998e      cmp   dword [edi+0x90], 0x02
  |   |     0x00c09995      mov   bl, 0x01
  |   |     0x00c09997      mov   byte [ebp-0x04], 0x00
  |   |     0x00c0999b      mov   byte [ebp-0x31], bl
  |   | ,=< 0x00c0999e      jnz   0xc09a62
  |   | |   0x00c099a4      mov   eax, dword [edi+0x70]
  |   | |   0x00c099a7      xor   esi, esi
  |   | |   0x00c099a9      mov   edx, dword [0x201e2d8]               ; [0x201e2d8:4]=0
  |   | |   0x00c099af      mov   dword [ebp-0x44], edx
  |   | |   0x00c099b2      mov   dword [ebp-0x68], eax
  |   | |   0x00c099b5      test  eax, eax
  |   |,==< 0x00c099b7      jz    0xc09a62
  |   |||   0x00c099bd      mov   dword [ebp-0x1c], 0x7f800000
  |   |||   0x00c099c4      mov   dword [ebp-0x18], 0x7f800000
  |   |||   0x00c099cb      mov   dword [ebp-0x14], 0x7f800000
  |   |||   0x00c099d2      mov   dword [ebp-0x3c], 0xffffffc0         ; 4294967232
  |   |||   0x00c099d9      mov   ebx, dword [edx+0x38]
  |   |||   0x00c099dc      lea   ecx, dword [edi+0x0c]
  |   |||   0x00c099df      call  0xbcf930
  |   |||   0x00c099e4      push  eax
  |   |||   0x00c099e5      call  0xcc08a0
  |   |||   0x00c099ea      add   esp, 0x04
  |   |||   0x00c099ed      mov   byte [ebp-0x60], al
  |   |||   0x00c099f0      lea   ecx, dword [edi+0x0c]
  |   |||   0x00c099f3      call  0xbcf930
  |   |||   0x00c099f8      mov   edx, dword [edi+0x08]
  |   |||   0x00c099fb      lea   ecx, dword [edi+0x5c]
  |   |||   0x00c099fe      add   edx, 0x20                            ; 32
  |   |||   0x00c09a01      cmp   esi, 0x04                            ; 4
  |  ,====< 0x00c09a04      jb    0xc09a09
  |  ||||   0x00c09a06      mov   ecx, dword [edi+0x5c]
  |  `----> 0x00c09a09      lea   edi, dword [ebp-0x6c]
  |   |||   0x00c09a0c      push  edi
  |   |||   0x00c09a0d      push  dword [ebp-0x60]
  |   |||   0x00c09a10      push  eax
  |   |||   0x00c09a11      mov   eax, dword [ebp-0x3c]
  |   |||   0x00c09a14      add   eax, ecx
  |   |||   0x00c09a16      mov   ecx, ebx
  |   |||   0x00c09a18      push  edx
  |   |||   0x00c09a19      push  eax
  |   |||   0x00c09a1a      lea   eax, dword [ebp-0x28]
  |   |||   0x00c09a1d      push  eax
  |   |||   0x00c09a1e      invalid
  |   |||   0x00c09a1f      invalid
            0x00c07310      push  ebx
            0x00c07311      push  esi
            0x00c07312      mov   esi, ecx
            0x00c07314      push  edi
            0x00c07315      mov   edi, dword [esp+0x14]
            0x00c07319      mov   ebx, dword [esi+0x0c]
            0x00c0731c      mov   eax, dword [esi+0x08]
            0x00c0731f      imul  edx, ebx, 0xb4
            0x00c07325      add   edx, eax
            0x00c07327      cmp   eax, edx
        ,=< 0x00c07329      jz    0xc07343
        |   0x00c0732b      nop   dword [eax+eax*1], eax
       .--> 0x00c07330      cmp   dword [eax], 0x69                    ; 'i'
      ,===< 0x00c07333      jnz   0xc0733a
      |:|   0x00c07335      cmp   dword [eax+0x04], edi
     ,====< 0x00c07338      jz    0xc07371
     |`---> 0x00c0733a      add   eax, 0xb4                            ; 180
     | :|   0x00c0733f      cmp   eax, edx
     | `==< 0x00c07341      jnz   0xc07330
     | .`-> 0x00c07343      cmp   ebx, dword [esi]
     | :,=< 0x00c07345      jnz   0xc0734c
     | :|   0x00c07347      call  0x9d6ad0
     | :`-> 0x00c0734c      imul  ecx, ebx, 0xb4
     | :    0x00c07352      lea   eax, dword [ebx+0x01]
     | :    0x00c07355      mov   dword [esi+0x0c], eax
     | :    0x00c07358      mov   eax, dword [esp+0x10]
     | :    0x00c0735c      add   ecx, dword [esi+0x08]
     | :    0x00c0735f      mov   dword [ecx+0x04], edi
     | :    0x00c07362      pop   edi
     | :    0x00c07363      pop   esi
     | :    0x00c07364      mov   dword [ecx], 0x69                    ; 'i'
     | :                                                               ; [0x69:4]=-1 ; 105
     | :    0x00c0736a      mov   dword [ecx+0x08], eax
     | :    0x00c0736d      pop   ebx
     | :    0x00c0736e      ret   0x08
     `----> 0x00c07371      cmp   eax, edx
       `==< 0x00c07373      jz    0xc07343
            0x00c07375      mov   ecx, dword [esp+0x10]
            0x00c07379      pop   edi
            0x00c0737a      pop   esi
            0x00c0737b      mov   dword [eax+0x08], ecx
            0x00c0737e      pop   ebx
            0x00c0737f      ret   0x08
            0x00c07382      int3
            0x00c07383      int3
            0x00c07384      int3
            0x00c07385      int3
            0x00c07386      int3
            0x00c07387      int3
            0x00c07388      int3
            0x00c07389      int3
            0x00c0738a      int3
            0x00c0738b      int3
            0x00c0738c      int3
            0x00c0738d      int3
            0x00c0738e      int3
            0x00c0738f      int3
            0x00c07390      push  ebx
            0x00c07391      push  esi
            0x00c07392      mov   esi, ecx
            0x00c07394      push  edi
            0x00c07395      mov   edi, dword [esp+0x14]
            0x00c07399      mov   ebx, dword [esi+0x0c]
            0x00c0739c      mov   eax, dword [esi+0x08]
            0x00c0739f      imul  edx, ebx, 0xb4
            0x00c073a5      add   edx, eax
            0x00c073a7      cmp   eax, edx
        ,=< 0x00c073a9      jz    0xc073c3
        |   0x00c073ab      nop   dword [eax+eax*1], eax
       .--> 0x00c073b0      cmp   dword [eax], 0x6b                    ; 'k'
      ,===< 0x00c073b3      jnz   0xc073ba
      |:|   0x00c073b5      cmp   dword [eax+0x04], edi
     ,====< 0x00c073b8      jz    0xc073f1
     |`---> 0x00c073ba      add   eax, 0xb4                            ; 180
     | :|   0x00c073bf      cmp   eax, edx
     | `==< 0x00c073c1      jnz   0xc073b0
     | .`-> 0x00c073c3      cmp   ebx, dword [esi]
     | :,=< 0x00c073c5      jnz   0xc073cc
     | :|   0x00c073c7      call  0x9d6ad0
     | :`-> 0x00c073cc      imul  ecx, ebx, 0xb4
     | :    0x00c073d2      lea   eax, dword [ebx+0x01]
     | :    0x00c073d5      mov   dword [esi+0x0c], eax
     | :    0x00c073d8      mov   eax, dword [esp+0x10]
     | :    0x00c073dc      add   ecx, dword [esi+0x08]
     | :    0x00c073df      mov   dword [ecx+0x04], edi
     | :    0x00c073e2      pop   edi
     | :    0x00c073e3      pop   esi
     | :    0x00c073e4      mov   dword [ecx], 0x6b                    ; 'k'
     | :                                                               ; [0x6b:4]=-1 ; 107
     | :    0x00c073ea      mov   dword [ecx+0x08], eax
     | :    0x00c073ed      pop   ebx
     | :    0x00c073ee      ret   0x08
     `----> 0x00c073f1      cmp   eax, edx
       `==< 0x00c073f3      jz    0xc073c3
            0x00c073f5      mov   ecx, dword [esp+0x10]
            0x00c073f9      pop   edi
            0x00c073fa      pop   esi
            0x00c073fb      mov   dword [eax+0x08], ecx
            0x00c073fe      pop   ebx
            0x00c073ff      ret   0x08
            0x00c07402      int3
            0x00c07403      int3
            0x00c07404      int3
            0x00c07405      int3
            0x00c07406      int3
            0x00c07407      int3
            0x00c07408      int3
            0x00c07409      int3
            0x00c0740a      int3
            0x00c0740b      int3
            0x00c0740c      int3
            0x00c0740d      int3
            0x00c0740e      int3
            0x00c0740f      int3
            0x00c07410      push  ebp
            0x00c07411      mov   ebp, esp
            0x00c07413      push  0xffffffff                           ; 255
            0x00c07415      push  0x1876168
            0x00c0741a      mov   eax, dword fs:[0x0]
            0x00c07420      push  eax
            0x00c07421      sub   esp, 0x30
            0x00c07424      push  esi
            0x00c07425      push  edi
            0x00c07426      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0742b      xor   eax, ebp
            0x00c0742d      push  eax
            0x00c0742e      lea   eax, dword [ebp-0x0c]
            0x00c07431      mov   dword fs:[0x0], eax
            0x00c07437      mov   edi, ecx
            0x00c07439      mov   dword [ebp-0x24], edi
            0x00c0743c      mov   eax, dword [edi]
            0x00c0743e      mov   esi, eax
            0x00c07440      mov   edx, dword [ebp+0x08]
            0x00c07443      mov   ecx, eax
            0x00c07445      mov   dword [ebp-0x1c], eax
            0x00c07448      and   esi, 0x7ffffff
            0x00c0744e      shr   ecx, 0x1b
            0x00c07451      mov   eax, 0x01
            0x00c07456      shl   eax, cl
            0x00c07458      sar   eax, 0x01
            0x00c0745a      cmp   edx, eax
        ,=< 0x00c0745c      jz    0xc076a6
        |   0x00c07462      test  edx, edx
       ,==< 0x00c07464      jnz   0xc07481
       ||   0x00c07466      push  edx
       ||   0x00c07467      mov   ecx, edi
       ||   0x00c07469      call  0xc0ffc0
       ||   0x00c0746e      mov   ecx, dword [ebp-0x0c]
       ||   0x00c07471      mov   dword fs:[0x0], ecx
       ||   0x00c07478      pop   ecx
       ||   0x00c07479      pop   edi
       ||   0x00c0747a      pop   esi
       ||   0x00c0747b      mov   esp, ebp
       ||   0x00c0747d      pop   ebp
       ||   0x00c0747e      invalid
       ||   0x00c0747f      invalid
            0x00b2eeb0      push  ebp
            0x00b2eeb1      mov   ebp, esp
            0x00b2eeb3      push  0xffffffff                           ; 255
            0x00b2eeb5      push  0x18693a8
            0x00b2eeba      mov   eax, dword fs:[0x0]
            0x00b2eec0      push  eax
            0x00b2eec1      push  ecx
            0x00b2eec2      push  ebx
            0x00b2eec3      push  esi
            0x00b2eec4      push  edi
            0x00b2eec5      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2eeca      xor   eax, ebp
            0x00b2eecc      push  eax
            0x00b2eecd      lea   eax, dword [ebp-0x0c]
            0x00b2eed0      mov   dword fs:[0x0], eax
            0x00b2eed6      push  dword [0x1d6c084]
            0x00b2eedc      push  0x01                                 ; 1
            0x00b2eede      push  0x118                                ; 280
            0x00b2eee3      push  0x01                                 ; 1
            0x00b2eee5      call  0x529280
            0x00b2eeea      mov   esi, eax
            0x00b2eeec      add   esp, 0x10
            0x00b2eeef      mov   dword [ebp-0x10], esi
            0x00b2eef2      mov   dword [ebp-0x04], 0x00
            0x00b2eef9      test  esi, esi
        ,=< 0x00b2eefb      jz    0xb2efc0
        |   0x00b2ef01      mov   ecx, esi
        |   0x00b2ef03      call  0xb21f60
        |   0x00b2ef08      mov   dword [esi], 0x19a191c               ; [0x19a191c:4]=0x561c50
        |   0x00b2ef0e      lea   ecx, dword [esi+0x08]
        |   0x00b2ef11      mov   byte [ebp-0x04], 0x01
        |   0x00b2ef15      mov   dword [esi+0x04], 0x00
        |   0x00b2ef1c      call  0x4f71f0
        |   0x00b2ef21      mov   dword [esi+0x28], 0x00
        |   0x00b2ef28      mov   dword [esi+0x2c], 0x00
        |   0x00b2ef2f      mov   dword [esi+0x30], 0x00
        |   0x00b2ef36      mov   dword [esi+0x44], 0x00
        |   0x00b2ef3d      mov   dword [esi+0x48], 0x00
        |   0x00b2ef44      mov   dword [esi+0x4c], 0x00
        |   0x00b2ef4b      mov   dword [esi+0x90], 0x00
        |   0x00b2ef55      mov   dword [esi+0x94], 0x00
        |   0x00b2ef5f      mov   dword [esi+0x98], 0x00
        |   0x00b2ef69      mov   dword [esi+0xdc], 0x00
        |   0x00b2ef73      mov   dword [esi+0xe0], 0x00
        |   0x00b2ef7d      mov   dword [esi+0xe4], 0x00
        |   0x00b2ef87      mov   dword [esi+0xf8], 0x00
        |   0x00b2ef91      mov   dword [esi+0xfc], 0x00
        |   0x00b2ef9b      mov   dword [esi+0x100], 0x00
        |   0x00b2efa5      lea   ecx, dword [esi+0x108]
        |   0x00b2efab      mov   byte [ebp-0x04], 0x06
        |   0x00b2efaf      mov   dword [esi+0x104], 0x00
        |   0x00b2efb9      call  0x4f71f0
       ,==< 0x00b2efbe      jmp   0xb2efc2
       |`-> 0x00b2efc0      xor   esi, esi
       `--> 0x00b2efc2      mov   edi, dword [ebp+0x08]
            0x00b2efc5      lea   ebx, dword [esi+0x04]
            0x00b2efc8      push  0x04                                 ; 4
            0x00b2efca      push  ebx
            0x00b2efcb      mov   ecx, edi
            0x00b2efcd      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b2efd4      mov   eax, dword [edi]
            0x00b2efd6      mov   eax, dword [eax+0x04]
            0x00b2efd9      call  eax
            0x00b2efdb      test  al, al
        ,=< 0x00b2efdd      jz    0xb2f073
        |   0x00b2efe3      mov   eax, dword [edi]
        |   0x00b2efe5      mov   ecx, edi
        |   0x00b2efe7      push  0x10                                 ; 16
        |   0x00b2efe9      mov   edx, dword [eax+0x04]
        |   0x00b2efec      lea   eax, dword [ebx+0x04]
        |   0x00b2efef      push  eax
        |   0x00b2eff0      call  edx
        |   0x00b2eff2      test  al, al
       ,==< 0x00b2eff4      jz    0xb2f073
       ||   0x00b2eff6      lea   eax, dword [esi+0x18]
       ||   0x00b2eff9      push  eax
       ||   0x00b2effa      push  edi
       ||   0x00b2effb      call  0xb35cd0
       ||   0x00b2f000      add   esp, 0x08
       ||   0x00b2f003      test  al, al
      ,===< 0x00b2f005      jz    0xb2f073
      |||   0x00b2f007      lea   eax, dword [esi+0x34]
      |||   0x00b2f00a      push  eax
      |||   0x00b2f00b      push  edi
      |||   0x00b2f00c      call  0xb35fc0
      |||   0x00b2f011      add   esp, 0x08
      |||   0x00b2f014      test  al, al
     ,====< 0x00b2f016      jz    0xb2f073
     ||||   0x00b2f018      lea   eax, dword [esi+0x50]
     ||||   0x00b2f01b      mov   ecx, edi
     ||||   0x00b2f01d      push  eax
     ||||   0x00b2f01e      call  0xb290c0
     ||||   0x00b2f023      test  al, al
    ,=====< 0x00b2f025      jz    0xb2f073
    |||||   0x00b2f027      lea   eax, dword [esi+0x9c]
    |||||   0x00b2f02d      mov   ecx, edi
    |||||   0x00b2f02f      push  eax
    |||||   0x00b2f030      call  0xb290c0
    |||||   0x00b2f035      test  al, al
   ,======< 0x00b2f037      jz    0xb2f073
   ||||||   0x00b2f039      lea   eax, dword [esi+0xe8]
   ||||||   0x00b2f03f      push  eax
   ||||||   0x00b2f040      push  edi
   ||||||   0x00b2f041      call  0xb35cd0
   ||||||   0x00b2f046      add   esp, 0x08
   ||||||   0x00b2f049      test  al, al
  ,=======< 0x00b2f04b      jz    0xb2f073
  |||||||   0x00b2f04d      lea   eax, dword [esi+0x104]
  |||||||   0x00b2f053      mov   ecx, edi
  |||||||   0x00b2f055      push  eax
  |||||||   0x00b2f056      call  0xb29080
  |||||||   0x00b2f05b      test  al, al
  ========< 0x00b2f05d      jz    0xb2f073
  |||||||   0x00b2f05f      mov   eax, esi
  |||||||   0x00b2f061      mov   ecx, dword [ebp-0x0c]
  |||||||   0x00b2f064      mov   dword fs:[0x0], ecx
  |||||||   0x00b2f06b      pop   ecx
  |||||||   0x00b2f06c      pop   edi
  |||||||   0x00b2f06d      pop   esi
  |||||||   0x00b2f06e      pop   ebx
  |||||||   0x00b2f06f      mov   esp, ebp
  |||||||   0x00b2f071      pop   ebp
  |||||||   0x00b2f072      ret
  ```````-> 0x00b2f073      test  esi, esi
        ,=< 0x00b2f075      jz    0xb2f080
        |   0x00b2f077      mov   eax, dword [esi]
        |   0x00b2f079      mov   ecx, esi
        |   0x00b2f07b      push  0x01                                 ; 1
        |   0x00b2f07d      call  dword [eax+0x08]                     ; 8
        `-> 0x00b2f080      xor   eax, eax
            0x00b2f082      mov   ecx, dword [ebp-0x0c]
            0x00b2f085      mov   dword fs:[0x0], ecx
            0x00b2f08c      pop   ecx
            0x00b2f08d      pop   edi
            0x00b2f08e      pop   esi
            0x00b2f08f      pop   ebx
            0x00b2f090      mov   esp, ebp
            0x00b2f092      pop   ebp
            0x00b2f093      ret
            0x00b2f094      int3
            0x00b2f095      int3
            0x00b2f096      int3
            0x00b2f097      int3
            0x00b2f098      int3
            0x00b2f099      int3
            0x00b2f09a      int3
            0x00b2f09b      int3
            0x00b2f09c      int3
            0x00b2f09d      int3
            0x00b2f09e      int3
            0x00b2f09f      int3
            0x00b2f0a0      push  ebp
            0x00b2f0a1      mov   ebp, esp
            0x00b2f0a3      push  0xffffffff                           ; 255
            0x00b2f0a5      push  0x186932b
            0x00b2f0aa      mov   eax, dword fs:[0x0]
