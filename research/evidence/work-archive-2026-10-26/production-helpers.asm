            0x00b57f80      push  ebp
            0x00b57f81      mov   ebp, esp
            0x00b57f83      push  0xffffffff                           ; 255
            0x00b57f85      push  0x186bf2b
            0x00b57f8a      mov   eax, dword fs:[0x0]
            0x00b57f90      push  eax
            0x00b57f91      push  ecx
            0x00b57f92      push  esi
            0x00b57f93      push  edi
            0x00b57f94      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b57f99      xor   eax, ebp
            0x00b57f9b      push  eax
            0x00b57f9c      lea   eax, dword [ebp-0x0c]
            0x00b57f9f      mov   dword fs:[0x0], eax
            0x00b57fa5      mov   edi, ecx
            0x00b57fa7      mov   dword [ebp-0x10], edi
            0x00b57faa      mov   esi, dword [ebp+0x08]
            0x00b57fad      lea   ecx, dword [edi+0x18]
            0x00b57fb0      mov   eax, dword [esi+0x0c]
            0x00b57fb3      mov   dword [edi+0x04], 0x00
            0x00b57fba      mov   byte [edi+0x08], 0x00
            0x00b57fbe      mov   dword [edi+0x0c], eax
            0x00b57fc1      mov   word [edi+0x10], 0x00
            0x00b57fc7      mov   dword [edi], 0x19a31c8               ; [0x19a31c8:4]=0xb5ab20
            0x00b57fcd      call  0x4f7520
            0x00b57fd2      push  edi
            0x00b57fd3      mov   ecx, esi
            0x00b57fd5      mov   dword [ebp-0x04], 0x00
            0x00b57fdc      mov   dword [edi+0x28], esi
            0x00b57fdf      call  0xb599a0
            0x00b57fe4      mov   al, byte [esi+0x08]
            0x00b57fe7      mov   byte [edi+0x08], al
            0x00b57fea      mov   eax, edi
            0x00b57fec      mov   ecx, dword [ebp-0x0c]
            0x00b57fef      mov   dword fs:[0x0], ecx
            0x00b57ff6      pop   ecx
            0x00b57ff7      pop   edi
            0x00b57ff8      pop   esi
            0x00b57ff9      mov   esp, ebp
            0x00b57ffb      pop   ebp
            0x00b57ffc      ret   0x04
            0x00b57fff      int3
            0x00b58000      push  ebp
            0x00b58001      mov   ebp, esp
            0x00b58003      push  0xffffffff                           ; 255
            0x00b58005      push  0x186bf2b
            0x00b5800a      mov   eax, dword fs:[0x0]
            0x00b58010      push  eax
            0x00b58011      push  ecx
            0x00b58012      push  esi
            0x00b58013      push  edi
            0x00b58014      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b58019      xor   eax, ebp
            0x00b5801b      push  eax
            0x00b5801c      lea   eax, dword [ebp-0x0c]
            0x00b5801f      mov   dword fs:[0x0], eax
            0x00b58025      mov   esi, ecx
            0x00b58027      mov   dword [ebp-0x10], esi
            0x00b5802a      mov   edi, dword [ebp+0x08]
            0x00b5802d      lea   ecx, dword [esi+0x18]
            0x00b58030      mov   eax, dword [edi+0x0c]
            0x00b58033      mov   dword [esi+0x04], 0x00
            0x00b5803a      mov   byte [esi+0x08], 0x00
            0x00b5803e      mov   dword [esi+0x0c], eax
            0x00b58041      mov   word [esi+0x10], 0x00
            0x00b58047      mov   dword [esi], 0x19a31c8               ; [0x19a31c8:4]=0xb5ab20
            0x00b5804d      call  0x4f7520
            0x00b58052      mov   eax, dword [ebp+0x0c]
            0x00b58055      mov   dword [esi+0x28], edi
            0x00b58058      mov   dword [ebp-0x04], 0x00
            0x00b5805f      cmp   dword [edi+0x04], eax
        ,=< 0x00b58062      jnb   0xb5806d
        |   0x00b58064      mov   dword [esi+0x04], 0x00
       ,==< 0x00b5806b      jmp   0xb58078
       |`-> 0x00b5806d      push  esi
       |    0x00b5806e      mov   ecx, edi
       |    0x00b58070      mov   dword [esi+0x04], eax
       |    0x00b58073      call  0xb599a0
       `--> 0x00b58078      mov   al, byte [edi+0x08]
            0x00b5807b      mov   byte [esi+0x08], al
            0x00b5807e      mov   eax, esi
            0x00b58080      mov   ecx, dword [ebp-0x0c]
            0x00b58083      mov   dword fs:[0x0], ecx
            0x00b5808a      pop   ecx
            0x00b5808b      pop   edi
            0x00b5808c      pop   esi
            0x00b5808d      mov   esp, ebp
            0x00b5808f      pop   ebp
            0x00b58090      ret   0x08
            0x00b58093      int3
            0x00b58094      int3
            0x00b58095      int3
            0x00b58096      int3
            0x00b58097      int3
            0x00b58098      int3
            0x00b58099      int3
            0x00b5809a      int3
            0x00b5809b      int3
            0x00b5809c      int3
            0x00b5809d      int3
            0x00b5809e      int3
            0x00b5809f      int3
            0x00b580a0      push  ebp
            0x00b580a1      mov   ebp, esp
            0x00b580a3      push  0xffffffff                           ; 255
            0x00b580a5      push  0x186bf5b
            0x00b580aa      mov   eax, dword fs:[0x0]
            0x00b580b0      push  eax
            0x00b580b1      sub   esp, 0x10
            0x00b580b4      push  ebx
            0x00b580b5      push  esi
            0x00b580b6      push  edi
            0x00b580b7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b580bc      xor   eax, ebp
            0x00b580be      push  eax
            0x00b580bf      lea   eax, dword [ebp-0x0c]
            0x00b580c2      mov   dword fs:[0x0], eax
            0x00b580c8      mov   edi, ecx
            0x00b580ca      mov   dword [ebp-0x14], edi
            0x00b580cd      mov   esi, dword [ebp+0x08]
            0x00b580d0      lea   ecx, dword [edi+0x18]
            0x00b580d3      mov   eax, dword [esi+0x0c]
            0x00b580d6      mov   dword [edi+0x04], 0x00
            0x00b580dd      mov   byte [edi+0x08], 0x00
            0x00b580e1      mov   dword [edi+0x0c], eax
            0x00b580e4      mov   word [edi+0x10], 0x00
            0x00b580ea      mov   dword [edi], 0x19a31c8               ; [0x19a31c8:4]=0xb5ab20
            0x00b580f0      call  0x4f7520
            0x00b580f5      mov   dword [edi+0x28], esi
            0x00b580f8      mov   eax, dword [esi+0x04]
            0x00b580fb      mov   byte [edi+0x11], 0x01
            0x00b580ff      cmp   byte [esi+0x10], 0x00
            0x00b58103      mov   dword [ebp-0x04], 0x00
            0x00b5810a      mov   dword [ebp-0x1c], eax
            0x00b5810d      mov   dword [ebp-0x18], 0x00
        ,=< 0x00b58114      jz    0xb5811c
        |   0x00b58116      mov   byte [edi+0x10], 0x01
       ,==< 0x00b5811a      jmp   0xb58134
       |`-> 0x00b5811c      mov   ecx, dword [esi+0x14]
       |    0x00b5811f      lea   edx, dword [ebp-0x1c]
       |    0x00b58122      push  0x08                                 ; 8
       |    0x00b58124      push  edx
       |    0x00b58125      mov   eax, dword [ecx]
       |    0x00b58127      mov   eax, dword [eax+0x04]
       |    0x00b5812a      call  eax
       |    0x00b5812c      test  al, al
       |,=< 0x00b5812e      jnz   0xb58134
       ||   0x00b58130      mov   byte [esi+0x10], 0x01
       ``-> 0x00b58134      mov   ebx, dword [ebp-0x18]
            0x00b58137      mov   eax, dword [ebp-0x1c]
            0x00b5813a      mov   dword [edi+0x04], eax
            0x00b5813d      test  ebx, ebx
        ,=< 0x00b5813f      jz    0xb581bb
        |   0x00b58141      cmp   ebx, dword [esi+0x18]
       ,==< 0x00b58144      jz    0xb5818d
       ||   0x00b58146      mov   ecx, dword [esi+0x1c]
       ||   0x00b58149      mov   dword [ebp-0x10], ecx
       ||   0x00b5814c      test  ebx, ebx
      ,===< 0x00b5814e      jz    0xb58174
      |||   0x00b58150      push  ebx
      |||   0x00b58151      lea   ecx, dword [esi+0x18]
      |||   0x00b58154      call  0x51f740
      |||   0x00b58159      mov   dword [ebp+0x08], eax
      |||   0x00b5815c      test  eax, eax
     ,====< 0x00b5815e      jnz   0xb5816c
     ||||   0x00b58160      push  ebx
     ||||   0x00b58161      call  0x5291a0
     ||||   0x00b58166      mov   eax, dword [ebp+0x08]
     ||||   0x00b58169      add   esp, 0x04
     `----> 0x00b5816c      mov   ecx, dword [ebp-0x10]
      |||   0x00b5816f      mov   dword [esi+0x1c], eax
     ,====< 0x00b58172      jmp   0xb5817b
     |`---> 0x00b58174      mov   dword [esi+0x1c], 0x00
     `----> 0x00b5817b      test  ecx, ecx
      ,===< 0x00b5817d      jz    0xb5818a
      |||   0x00b5817f      push  ecx
      |||   0x00b58180      push  0x00
      |||   0x00b58182      call  0x5291c0
      |||   0x00b58187      add   esp, 0x08
      `---> 0x00b5818a      mov   dword [esi+0x18], ebx
       `--> 0x00b5818d      cmp   byte [esi+0x10], 0x00
       ,==< 0x00b58191      jnz   0xb581ab
       ||   0x00b58193      mov   ecx, dword [esi+0x14]
       ||   0x00b58196      push  dword [ebp-0x18]
       ||   0x00b58199      push  dword [esi+0x1c]
       ||   0x00b5819c      mov   eax, dword [ecx]
       ||   0x00b5819e      mov   eax, dword [eax+0x04]
       ||   0x00b581a1      call  eax
       ||   0x00b581a3      test  al, al
      ,===< 0x00b581a5      jnz   0xb581ab
      |||   0x00b581a7      mov   byte [esi+0x10], 0x01
      ``--> 0x00b581ab      push  0x01                                 ; 1
        |   0x00b581ad      push  dword [ebp-0x18]
        |   0x00b581b0      lea   ecx, dword [edi+0x18]
        |   0x00b581b3      push  dword [esi+0x1c]
        |   0x00b581b6      call  0x519a30
        `-> 0x00b581bb      mov   al, byte [esi+0x08]
            0x00b581be      mov   byte [edi+0x08], al
            0x00b581c1      mov   eax, edi
            0x00b581c3      mov   ecx, dword [ebp-0x0c]
            0x00b581c6      mov   dword fs:[0x0], ecx
            0x00b581cd      pop   ecx
            0x00b581ce      pop   edi
            0x00b581cf      pop   esi
            0x00b581d0      pop   ebx
            0x00b581d1      mov   esp, ebp
            0x00b581d3      pop   ebp
            0x00b581d4      ret   0x04
            0x00b581d7      int3
            0x00b581d8      int3
            0x00b581d9      int3
            0x00b581da      int3
            0x00b581db      int3
            0x00b581dc      int3
            0x00b581dd      int3
            0x00b581de      int3
            0x00b581df      int3
            0x00b581e0      push  ebp
            0x00b581e1      mov   ebp, esp
            0x00b581e3      push  0xffffffff                           ; 255
            0x00b581e5      push  0x186bf8b
            0x00b581ea      mov   eax, dword fs:[0x0]
            0x00b581f0      push  eax
            0x00b581f1      sub   esp, 0x14
            0x00b581f4      push  ebx
            0x00b581f5      push  esi
            0x00b581f6      push  edi
            0x00b581f7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b581fc      xor   eax, ebp
            0x00b581fe      push  eax
            0x00b581ff      invalid
            0x00c06070      push  ecx
            0x00c06071      push  ebx
            0x00c06072      push  ebp
            0x00c06073      push  esi
            0x00c06074      mov   esi, ecx
            0x00c06076      mov   dword [esp+0x0c], 0x00
            0x00c0607e      push  edi
            0x00c0607f      neg   ecx
            0x00c06081      lea   eax, dword [esp+0x10]
            0x00c06085      push  0x04                                 ; 4
            0x00c06087      push  eax
            0x00c06088      lea   eax, dword [esi-0x14]
            0x00c0608b      sbb   ecx, ecx
            0x00c0608d      and   ecx, eax
            0x00c0608f      call  0xb5abf0
            0x00c06094      mov   ebx, dword [esp+0x18]
            0x00c06098      mov   edi, dword [esp+0x10]
            0x00c0609c      mov   ecx, dword [ebx+0x14]
            0x00c0609f      cmp   edi, ecx
        ,=< 0x00c060a1      jb    0xc06103
        |   0x00c060a3      mov   ebp, 0x04
        |   0x00c060a8      cmp   ecx, ebp
       ,==< 0x00c060aa      jnb   0xc060c6
       ||   0x00c060ac      lea   edx, dword [ebx+ecx*4]
       ||   0x00c060af      nop
      .---> 0x00c060b0      mov   eax, ebp
      :||   0x00c060b2      cmp   edi, eax
      :||   0x00c060b4      cmovb eax, edi
      :||   0x00c060b7      cmp   ecx, eax
     ,====< 0x00c060b9      jnb   0xc060c6
     |:||   0x00c060bb      mov   dword [edx], 0x00
     |:||   0x00c060c1      inc   ecx
     |:||   0x00c060c2      add   edx, ebp
     |`===< 0x00c060c4      jmp   0xc060b0
     `-`--> 0x00c060c6      cmp   edi, ebp
       ,==< 0x00c060c8      jbe   0xc06103
       ||   0x00c060ca      push  edi
       ||   0x00c060cb      mov   ecx, ebx
       ||   0x00c060cd      call  0xc10ee0
       ||   0x00c060d2      cmp   dword [ebx+0x14], ebp
       ||   0x00c060d5      cmovnbe ebp, dword [ebx+0x14]
       ||   0x00c060d9      cmp   ebp, edi
      ,===< 0x00c060db      jnb   0xc06103
      |||   0x00c060dd      mov   edx, edi
      |||   0x00c060df      lea   ecx, dword [ebp*4-0x10]
      |||   0x00c060e6      sub   edx, ebp
      |||   0x00c060e8      nop   dword [eax+eax*1], eax
     .----> 0x00c060f0      mov   eax, dword [ebx+0x10]
     :|||   0x00c060f3      lea   ecx, dword [ecx+0x04]
     :|||   0x00c060f6      mov   dword [eax+ecx*1-0x04], 0x00
     :|||   0x00c060fe      sub   edx, 0x01
     `====< 0x00c06101      jnz   0xc060f0
      ```-> 0x00c06103      mov   dword [ebx+0x14], edi
            0x00c06106      xor   edi, edi
            0x00c06108      cmp   dword [esp+0x10], edi
        ,=< 0x00c0610c      jbe   0xc0613b
        |   0x00c0610e      lea   ebp, dword [edi-0x10]
       .--> 0x00c06111      lea   eax, dword [ebx+0x10]
       :|   0x00c06114      cmp   edi, 0x04                            ; 4
      ,===< 0x00c06117      jb    0xc0611c
      |:|   0x00c06119      mov   eax, dword [ebx+0x10]
      `---> 0x00c0611c      add   eax, ebp
       :|   0x00c0611e      mov   ecx, esi
       :|   0x00c06120      neg   ecx
       :|   0x00c06122      push  0x04                                 ; 4
       :|   0x00c06124      push  eax
       :|   0x00c06125      lea   eax, dword [esi-0x14]
       :|   0x00c06128      sbb   ecx, ecx
       :|   0x00c0612a      and   ecx, eax
       :|   0x00c0612c      call  0xb5abf0
       :|   0x00c06131      inc   edi
       :|   0x00c06132      add   ebp, 0x04
       :|   0x00c06135      cmp   edi, dword [esp+0x10]
       `==< 0x00c06139      jb    0xc06111
        `-> 0x00c0613b      lea   eax, dword [esi-0x14]
            0x00c0613e      neg   esi
            0x00c06140      pop   edi
            0x00c06141      sbb   esi, esi
            0x00c06143      and   eax, esi
            0x00c06145      pop   esi
            0x00c06146      pop   ebp
            0x00c06147      pop   ebx
            0x00c06148      pop   ecx
            0x00c06149      ret   0x04
            0x00c0614c      int3
            0x00c0614d      int3
            0x00c0614e      int3
            0x00c0614f      int3
            0x00c06150      sub   esp, 0x10
            0x00c06153      push  ebp
            0x00c06154      push  esi
            0x00c06155      push  edi
            0x00c06156      mov   edi, dword [esp+0x20]
            0x00c0615a      lea   ebp, dword [ecx-0x10]
            0x00c0615d      test  ecx, ecx
            0x00c0615f      mov   dword [esp+0x18], ecx
            0x00c06163      mov   edx, 0x18                            ; 24
            0x00c06168      push  0x04                                 ; 4
            0x00c0616a      mov   eax, dword [edi+0x14]
            0x00c0616d      mov   dword [esp+0x10], eax
            0x00c06171      mov   eax, 0xfffffff0                      ; 4294967280
            0x00c06176      cmovz ebp, eax
            0x00c06179      lea   eax, dword [ecx+0x08]
            0x00c0617c      cmovz eax, edx
            0x00c0617f      mov   dword [esp+0x18], ebp
            0x00c06183      mov   dword [esp+0x14], eax
            0x00c06187      lea   edx, dword [esp+0x10]
            0x00c0618b      push  edx
            0x00c0618c      mov   ecx, dword [eax]
            0x00c0618e      mov   eax, dword [ecx]
            0x00c06190      call  dword [eax+0x1c]                     ; 28
            0x00c06193      xor   esi, esi
            0x00c06195      cmp   dword [edi+0x14], esi
        ,=< 0x00c06198      jbe   0xc061d3
        |   0x00c0619a      mov   ebp, dword [esp+0x10]
        |   0x00c0619e      push  ebx
        |   0x00c0619f      lea   ebx, dword [esi-0x10]
       .--> 0x00c061a2      lea   eax, dword [edi+0x10]
       :|   0x00c061a5      cmp   esi, 0x04                            ; 4
      ,===< 0x00c061a8      jb    0xc061ad
      |:|   0x00c061aa      mov   eax, dword [edi+0x10]
      `---> 0x00c061ad      mov   ecx, dword [ebp]
       :|   0x00c061b0      lea   edx, dword [esp+0x14]
       :|   0x00c061b4      mov   eax, dword [ebx+eax*1]
       :|   0x00c061b7      mov   dword [esp+0x14], eax
       :|   0x00c061bb      push  0x04                                 ; 4
       :|   0x00c061bd      mov   eax, dword [ecx]
       :|   0x00c061bf      push  edx
       :|   0x00c061c0      call  dword [eax+0x1c]                     ; 28
       :|   0x00c061c3      mov   eax, edi
       :|   0x00c061c5      inc   esi
       :|   0x00c061c6      add   ebx, 0x04
       :|   0x00c061c9      cmp   esi, dword [eax+0x14]
       `==< 0x00c061cc      jb    0xc061a2
        |   0x00c061ce      mov   ebp, dword [esp+0x18]
        |   0x00c061d2      pop   ebx
        `-> 0x00c061d3      xor   eax, eax
            0x00c061d5      cmp   dword [esp+0x18], eax
            0x00c061d9      pop   edi
            0x00c061da      cmovz ebp, eax
            0x00c061dd      pop   esi
            0x00c061de      mov   eax, ebp
            0x00c061e0      pop   ebp
            0x00c061e1      add   esp, 0x10
            0x00c061e4      ret   0x04
            0x00c061e7      int3
            0x00c061e8      int3
            0x00c061e9      int3
            0x00c061ea      int3
            0x00c061eb      int3
            0x00c061ec      int3
            0x00c061ed      int3
            0x00c061ee      int3
            0x00c061ef      int3
            0x00c069a0      sub   esp, 0x18
            0x00c069a3      push  ebx
            0x00c069a4      push  ebp
            0x00c069a5      push  esi
            0x00c069a6      mov   ebp, ecx
            0x00c069a8      mov   dword [esp+0x0c], 0x00
            0x00c069b0      push  edi
            0x00c069b1      neg   ecx
            0x00c069b3      lea   eax, dword [esp+0x10]
            0x00c069b7      push  0x04                                 ; 4
            0x00c069b9      push  eax
            0x00c069ba      lea   eax, dword [ebp-0x14]
            0x00c069bd      sbb   ecx, ecx
            0x00c069bf      and   ecx, eax
            0x00c069c1      call  0xb5abf0
            0x00c069c6      mov   ebx, dword [esp+0x2c]
            0x00c069ca      mov   edi, dword [esp+0x10]
            0x00c069ce      mov   esi, dword [ebx+0x10]
            0x00c069d1      cmp   edi, esi
        ,=< 0x00c069d3      jbe   0xc06a0a
        |   0x00c069d5      push  edi
        |   0x00c069d6      mov   ecx, ebx
        |   0x00c069d8      call  0xac32b0
        |   0x00c069dd      lea   ecx, dword [esi+esi*4]
        |   0x00c069e0      mov   dword [ebx+0x10], edi
        |   0x00c069e3      shl   ecx, 0x02
       .--> 0x00c069e6      mov   eax, dword [ebx+0x0c]
       :|   0x00c069e9      inc   esi
       :|   0x00c069ea      add   eax, ecx
       :|   0x00c069ec      add   ecx, 0x14                            ; 20
       :|   0x00c069ef      mov   dword [eax+0x04], 0x00
       :|   0x00c069f6      mov   dword [eax+0x0c], 0x00
       :|   0x00c069fd      mov   dword [eax+0x10], 0x00
       :|   0x00c06a04      cmp   esi, edi
       `==< 0x00c06a06      jb    0xc069e6
       ,==< 0x00c06a08      jmp   0xc06a24
      ,=`-> 0x00c06a0a      jnb   0xc06a28
      ||    0x00c06a0c      mov   eax, dword [ebx+0x0c]
      ||    0x00c06a0f      lea   ecx, dword [edi+edi*4]
      ||    0x00c06a12      sub   esi, edi
      ||    0x00c06a14      push  esi
      ||    0x00c06a15      lea   eax, dword [eax+ecx*4]
      ||    0x00c06a18      push  eax
      ||    0x00c06a19      call  0x9b21a0
      ||    0x00c06a1e      add   esp, 0x08
      ||    0x00c06a21      mov   dword [ebx+0x10], edi
      |`--> 0x00c06a24      mov   edi, dword [esp+0x10]
      `---> 0x00c06a28      mov   dword [esp+0x1c], 0x00
            0x00c06a30      test  edi, edi
        ,=< 0x00c06a32      jz    0xc06b4d
        |   0x00c06a38      xor   ecx, ecx
        |   0x00c06a3a      mov   dword [esp+0x20], ecx
        |   0x00c06a3e      nop
       .--> 0x00c06a40      mov   edi, dword [ebx+0x0c]
       :|   0x00c06a43      lea   eax, dword [esp+0x14]
       :|   0x00c06a47      add   edi, ecx
       :|   0x00c06a49      mov   dword [esp+0x14], 0x00
       :|   0x00c06a51      mov   ecx, ebp
       :|   0x00c06a53      neg   ecx
       :|   0x00c06a55      push  0x04                                 ; 4
       :|   0x00c06a57      push  eax
       :|   0x00c06a58      lea   eax, dword [ebp-0x14]
       :|   0x00c06a5b      sbb   ecx, ecx
       :|   0x00c06a5d      and   ecx, eax
       :|   0x00c06a5f      call  0xb5abf0
       :|   0x00c06a64      mov   ebx, dword [esp+0x14]
       :|   0x00c06a68      mov   esi, dword [edi+0x10]
       :|   0x00c06a6b      cmp   ebx, esi
      ,===< 0x00c06a6d      jbe   0xc06af8
      |:|   0x00c06a73      cmp   ebx, dword [edi+0x04]
     ,====< 0x00c06a76      jbe   0xc06adb
     ||:|   0x00c06a78      test  ebx, ebx
    ,=====< 0x00c06a7a      jnz   0xc06a82
    |||:|   0x00c06a7c      xor   eax, eax
    |||:|   0x00c06a7e      mov   ecx, esi
   ,======< 0x00c06a80      jmp   0xc06a9f
   |`-----> 0x00c06a82      call  0x52b950
   | ||:|   0x00c06a87      push  dword [0x1d6c084]
   | ||:|   0x00c06a8d      mov   ecx, eax
   | ||:|   0x00c06a8f      lea   eax, dword [ebx*4]
   | ||:|   0x00c06a96      push  eax
   | ||:|   0x00c06a97      call  0x52b5a0
   | ||:|   0x00c06a9c      mov   ecx, dword [edi+0x10]
   `------> 0x00c06a9f      push  ecx
     ||:|   0x00c06aa0      push  dword [edi+0x0c]
     ||:|   0x00c06aa3      mov   dword [esp+0x20], eax
     ||:|   0x00c06aa7      push  eax
     ||:|   0x00c06aa8      call  0x4de440
     ||:|   0x00c06aad      add   esp, 0x0c
     ||:|   0x00c06ab0      cmp   dword [edi+0x04], 0x00
    ,=====< 0x00c06ab4      jz    0xc06ad1
    |||:|   0x00c06ab6      mov   eax, dword [edi+0x0c]
    |||:|   0x00c06ab9      mov   dword [esp+0x24], eax
    |||:|   0x00c06abd      test  eax, eax
   ,======< 0x00c06abf      jz    0xc06ad1
   ||||:|   0x00c06ac1      call  0x52b950
   ||||:|   0x00c06ac6      push  dword [esp+0x24]
   ||||:|   0x00c06aca      mov   ecx, eax
   ||||:|   0x00c06acc      call  0x52b8b0
   ``-----> 0x00c06ad1      mov   eax, dword [esp+0x18]
     ||:|   0x00c06ad5      mov   dword [edi+0x0c], eax
     ||:|   0x00c06ad8      mov   dword [edi+0x04], ebx
     `----> 0x00c06adb      mov   dword [edi+0x10], ebx
      |:|   0x00c06ade      nop
     .----> 0x00c06ae0      mov   eax, dword [edi+0x0c]
     :|:|   0x00c06ae3      mov   dword [eax+esi*4], 0x00
     :|:|   0x00c06aea      lea   eax, dword [eax+esi*4]
     :|:|   0x00c06aed      inc   esi
     :|:|   0x00c06aee      cmp   esi, ebx
     `====< 0x00c06af0      jb    0xc06ae0
      |:|   0x00c06af2      mov   ebx, dword [esp+0x14]
     ,====< 0x00c06af6      jmp   0xc06afd
    ,=`---> 0x00c06af8      jnb   0xc06afd
    || :|   0x00c06afa      mov   dword [edi+0x10], ebx
    ``----> 0x00c06afd      xor   esi, esi
       :|   0x00c06aff      test  ebx, ebx
      ,===< 0x00c06b01      jz    0xc06b2b
      |:|   0x00c06b03      lea   ebx, dword [ebp-0x14]
     .----> 0x00c06b06      mov   eax, dword [edi+0x0c]
     :|:|   0x00c06b09      mov   ecx, ebx
     :|:|   0x00c06b0b      lea   eax, dword [eax+esi*4]
     :|:|   0x00c06b0e      test  ebp, ebp
    ,=====< 0x00c06b10      jnz   0xc06b15
    |:|:|   0x00c06b12      lea   ebx, dword [ebp-0x14]
    `-----> 0x00c06b15      push  0x04                                 ; 4
     :|:|   0x00c06b17      push  eax
     :|:|   0x00c06b18      xor   eax, eax
     :|:|   0x00c06b1a      test  ebp, ebp
     :|:|   0x00c06b1c      cmovz ecx, eax
     :|:|   0x00c06b1f      call  0xb5abf0
     :|:|   0x00c06b24      inc   esi
     :|:|   0x00c06b25      cmp   esi, dword [esp+0x14]
     `====< 0x00c06b29      jb    0xc06b06
      `---> 0x00c06b2b      mov   eax, dword [esp+0x1c]
       :|   0x00c06b2f      mov   ecx, dword [esp+0x20]
       :|   0x00c06b33      inc   eax
       :|   0x00c06b34      mov   ebx, dword [esp+0x2c]
       :|   0x00c06b38      add   ecx, 0x14                            ; 20
       :|   0x00c06b3b      mov   dword [esp+0x1c], eax
       :|   0x00c06b3f      mov   dword [esp+0x20], ecx
       :|   0x00c06b43      cmp   eax, dword [esp+0x10]
       `==< 0x00c06b47      jb    0xc06a40
        `-> 0x00c06b4d      pop   edi
            0x00c06b4e      pop   esi
            0x00c06b4f      pop   ebp
            0x00c06b50      pop   ebx
            0x00c06b51      add   esp, 0x18
            0x00c06b54      ret   0x08
            0x00c06b57      int3
            0x00c06b58      int3
            0x00c06b59      int3
            0x00c06b5a      int3
            0x00c06b5b      int3
            0x00c06b5c      int3
            0x00c06b5d      int3
            0x00c06b5e      int3
            0x00c06b5f      int3
            0x00c06b60      push  edi
            0x00c06b61      mov   edi, dword [esp+0x0c]
            0x00c06b65      test  edi, edi
        ,=< 0x00c06b67      jz    0xc06b90
        |   0x00c06b69      push  esi
        |   0x00c06b6a      mov   esi, dword [esp+0x0c]
        |   0x00c06b6e      lea   ecx, dword [edi+edi*2]
        |   0x00c06b71      shl   ecx, 0x04
        |   0x00c06b74      add   esi, 0xffffffd0                      ; 4294967248
        |   0x00c06b77      add   esi, ecx
        |   0x00c06b79      nop   dword [eax], eax
       .--> 0x00c06b80      mov   ecx, esi
       :|   0x00c06b82      call  0xc36a20
       :|   0x00c06b87      sub   esi, 0x30                            ; 48
       :|   0x00c06b8a      sub   edi, 0x01
       `==< 0x00c06b8d      jnz   0xc06b80
        |   0x00c06b8f      pop   esi
        `-> 0x00c06b90      pop   edi
            0x00c06b91      ret
            0x00c06b92      int3
            0x00c06b93      int3
            0x00c06b94      int3
            0x00c06b95      int3
            0x00c06b96      int3
            0x00c06b97      int3
            0x00c06b98      int3
            0x00c06b99      int3
            0x00c06b9a      int3
            0x00c06b9b      int3
            0x00c06b9c      int3
            0x00c06b9d      int3
            0x00c06b9e      int3
            0x00c06b9f      int3
            0x00c06ba0      push  ebx
            0x00c06ba1      push  esi
            0x00c06ba2      mov   esi, dword [esp+0x0c]
            0x00c06ba6      mov   ebx, ecx
            0x00c06ba8      push  edi
            0x00c06ba9      push  dword [esp+0x14]
            0x00c06bad      push  esi
            0x00c06bae      invalid
            0x00c06baf      invalid
            0x00a75940      sub   esp, 0x08
            0x00a75943      push  esi
            0x00a75944      push  edi
            0x00a75945      mov   edi, dword [esp+0x14]
            0x00a75949      lea   eax, dword [esp+0x08]
            0x00a7594d      push  0x04                                 ; 4
            0x00a7594f      push  eax
            0x00a75950      lea   eax, dword [ecx-0x14]
            0x00a75953      mov   dword [esp+0x10], 0x00
            0x00a7595b      neg   ecx
            0x00a7595d      sbb   ecx, ecx
            0x00a7595f      and   ecx, eax
            0x00a75961      call  0xb5abf0
            0x00a75966      lea   eax, dword [esp+0x14]
            0x00a7596a      push  eax
            0x00a7596b      push  dword [esp+0x0c]
            0x00a7596f      lea   ecx, dword [esp+0x14]
            0x00a75973      call  0x4f7950
            0x00a75978      mov   esi, dword [eax]
            0x00a7597a      call  0x512430
            0x00a7597f      cmp   esi, dword [eax]
        ,=< 0x00a75981      jz    0xa759c2
        |   0x00a75983      mov   eax, dword [0x201e2d8]               ; [0x201e2d8:4]=0
        |   0x00a75988      push  0x00
        |   0x00a7598a      mov   ecx, dword [eax+0x54]
        |   0x00a7598d      push  ecx
        |   0x00a7598e      mov   eax, esp
        |   0x00a75990      mov   dword [eax], esi
        |   0x00a75992      call  0xae5730
        |   0x00a75997      mov   esi, eax
        |   0x00a75999      test  esi, esi
       ,==< 0x00a7599b      jnz   0xa759a9
       ||   0x00a7599d      xor   ecx, ecx
       ||   0x00a7599f      mov   dword [edi], ecx
       ||   0x00a759a1      pop   edi
       ||   0x00a759a2      pop   esi
       ||   0x00a759a3      add   esp, 0x08
       ||   0x00a759a6      ret   0x08
       `--> 0x00a759a9      mov   ecx, esi
        |   0x00a759ab      call  0x5c7b80
        |   0x00a759b0      xor   ecx, ecx
        |   0x00a759b2      cmp   eax, 0x01                            ; 1
        |   0x00a759b5      cmovz ecx, esi
        |   0x00a759b8      mov   dword [edi], ecx
        |   0x00a759ba      pop   edi
        |   0x00a759bb      pop   esi
        |   0x00a759bc      add   esp, 0x08
        |   0x00a759bf      ret   0x08
        `-> 0x00a759c2      mov   dword [edi], 0x00
            0x00a759c8      pop   edi
            0x00a759c9      pop   esi
            0x00a759ca      add   esp, 0x08
            0x00a759cd      ret   0x08
            0x00a759d0      sub   esp, 0x0c
            0x00a759d3      push  esi
            0x00a759d4      push  0x04                                 ; 4
            0x00a759d6      lea   eax, dword [esp+0x0c]
            0x00a759da      mov   dword [esp+0x0c], 0x00
            0x00a759e2      push  eax
            0x00a759e3      lea   eax, dword [ecx-0x14]
            0x00a759e6      neg   ecx
            0x00a759e8      sbb   ecx, ecx
            0x00a759ea      and   ecx, eax
            0x00a759ec      call  0xb5abf0
            0x00a759f1      lea   eax, dword [esp+0x07]
            0x00a759f5      push  eax
            0x00a759f6      push  dword [esp+0x0c]
            0x00a759fa      lea   ecx, dword [esp+0x14]
            0x00a759fe      call  0x4f7950
            0x00a75a03      mov   esi, dword [eax]
            0x00a75a05      call  0x512430
            0x00a75a0a      cmp   esi, dword [eax]
        ,=< 0x00a75a0c      jz    0xa75a44
        |   0x00a75a0e      mov   eax, dword [0x201e2d8]               ; [0x201e2d8:4]=0
        |   0x00a75a13      push  0x00
        |   0x00a75a15      mov   ecx, dword [eax+0x54]
        |   0x00a75a18      push  ecx
        |   0x00a75a19      mov   eax, esp
        |   0x00a75a1b      mov   dword [eax], esi
        |   0x00a75a1d      call  0xae5730
        |   0x00a75a22      mov   esi, eax
        |   0x00a75a24      test  esi, esi
       ,==< 0x00a75a26      jz    0xa75a44
       ||   0x00a75a28      mov   ecx, esi
       ||   0x00a75a2a      call  0x5c7b80
       ||   0x00a75a2f      xor   ecx, ecx
       ||   0x00a75a31      cmp   eax, 0x01                            ; 1
       ||   0x00a75a34      mov   eax, dword [esp+0x14]
       ||   0x00a75a38      cmovz ecx, esi
       ||   0x00a75a3b      mov   dword [eax], ecx
       ||   0x00a75a3d      pop   esi
       ||   0x00a75a3e      add   esp, 0x0c
       ||   0x00a75a41      ret   0x08
       ``-> 0x00a75a44      mov   eax, dword [esp+0x14]
            0x00a75a48      pop   esi
            0x00a75a49      mov   dword [eax], 0x00
            0x00a75a4f      add   esp, 0x0c
            0x00a75a52      ret   0x08
            0x00a75a55      int3
            0x00a75a56      int3
            0x00a75a57      int3
            0x00a75a58      int3
            0x00a75a59      int3
            0x00a75a5a      int3
            0x00a75a5b      int3
            0x00a75a5c      int3
            0x00a75a5d      int3
            0x00a75a5e      int3
            0x00a75a5f      int3
            0x00a75a60      push  esi
            0x00a75a61      call  0xa70490
            0x00a75a66      mov   ecx, dword [0x203a2ac]               ; [0x203a2ac:4]=0
            0x00a75a6c      mov   esi, eax
            0x00a75a6e      invalid
            0x00a75a6f      invalid
            0x00c0fad0      push  ebp
            0x00c0fad1      mov   ebp, esp
            0x00c0fad3      push  0xffffffff                           ; 255
            0x00c0fad5      push  0x184d3f8
            0x00c0fada      mov   eax, dword fs:[0x0]
            0x00c0fae0      push  eax
            0x00c0fae1      sub   esp, 0x2c
            0x00c0fae4      push  esi
            0x00c0fae5      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0faea      xor   eax, ebp
            0x00c0faec      push  eax
            0x00c0faed      lea   eax, dword [ebp-0x0c]
            0x00c0faf0      mov   dword fs:[0x0], eax
            0x00c0faf6      mov   esi, ecx
            0x00c0faf8      push  dword [ebp+0x08]
            0x00c0fafb      lea   ecx, dword [ebp-0x38]
            0x00c0fafe      call  0xb580a0
            0x00c0fb03      push  dword [ebp+0x0c]
            0x00c0fb06      lea   eax, dword [ebp-0x38]
            0x00c0fb09      mov   dword [ebp-0x04], 0x00
            0x00c0fb10      push  eax
            0x00c0fb11      mov   ecx, esi
            0x00c0fb13      call  0xc06c20
            0x00c0fb18      lea   ecx, dword [ebp-0x38]
            0x00c0fb1b      call  0xb589a0
            0x00c0fb20      mov   ecx, dword [ebp-0x0c]
            0x00c0fb23      mov   dword fs:[0x0], ecx
            0x00c0fb2a      pop   ecx
            0x00c0fb2b      pop   esi
            0x00c0fb2c      mov   esp, ebp
            0x00c0fb2e      pop   ebp
            0x00c0fb2f      ret   0x08
            0x00c0fb32      int3
            0x00c0fb33      int3
            0x00c0fb34      int3
            0x00c0fb35      int3
            0x00c0fb36      int3
            0x00c0fb37      int3
            0x00c0fb38      int3
            0x00c0fb39      int3
            0x00c0fb3a      int3
            0x00c0fb3b      int3
            0x00c0fb3c      int3
            0x00c0fb3d      int3
            0x00c0fb3e      int3
            0x00c0fb3f      int3
            0x00c0fb40      push  ebp
            0x00c0fb41      mov   ebp, esp
            0x00c0fb43      push  0xffffffff                           ; 255
            0x00c0fb45      push  0x184d368
            0x00c0fb4a      mov   eax, dword fs:[0x0]
            0x00c0fb50      push  eax
            0x00c0fb51      sub   esp, 0x1c
            0x00c0fb54      push  esi
            0x00c0fb55      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0fb5a      xor   eax, ebp
            0x00c0fb5c      push  eax
            0x00c0fb5d      lea   eax, dword [ebp-0x0c]
            0x00c0fb60      mov   dword fs:[0x0], eax
            0x00c0fb66      mov   esi, ecx
            0x00c0fb68      push  dword [ebp+0x08]
            0x00c0fb6b      lea   ecx, dword [ebp-0x28]
            0x00c0fb6e      call  0xb58330
            0x00c0fb73      push  dword [ebp+0x0c]
            0x00c0fb76      lea   eax, dword [ebp-0x28]
            0x00c0fb79      mov   dword [ebp-0x04], 0x00
            0x00c0fb80      push  eax
            0x00c0fb81      mov   ecx, esi
            0x00c0fb83      call  0xc06e50
            0x00c0fb88      lea   ecx, dword [ebp-0x28]
            0x00c0fb8b      call  0xb589c0
            0x00c0fb90      mov   ecx, dword [ebp-0x0c]
            0x00c0fb93      mov   dword fs:[0x0], ecx
            0x00c0fb9a      pop   ecx
            0x00c0fb9b      pop   esi
            0x00c0fb9c      mov   esp, ebp
            0x00c0fb9e      pop   ebp
            0x00c0fb9f      ret   0x08
            0x00c0fba2      int3
            0x00c0fba3      int3
            0x00c0fba4      int3
            0x00c0fba5      int3
            0x00c0fba6      int3
            0x00c0fba7      int3
            0x00c0fba8      int3
            0x00c0fba9      int3
            0x00c0fbaa      int3
            0x00c0fbab      int3
            0x00c0fbac      int3
            0x00c0fbad      int3
            0x00c0fbae      int3
            0x00c0fbaf      int3
            0x00c0fbb0      push  ebp
            0x00c0fbb1      mov   ebp, esp
            0x00c0fbb3      push  0xffffffff                           ; 255
            0x00c0fbb5      push  0x184d3f8
            0x00c0fbba      mov   eax, dword fs:[0x0]
            0x00c0fbc0      push  eax
            0x00c0fbc1      sub   esp, 0x2c
            0x00c0fbc4      push  esi
            0x00c0fbc5      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0fbca      xor   eax, ebp
            0x00c0fbcc      push  eax
            0x00c0fbcd      lea   eax, dword [ebp-0x0c]
            0x00c0fbd0      mov   dword fs:[0x0], eax
            0x00c0fbd6      mov   esi, ecx
            0x00c0fbd8      push  dword [ebp+0x08]
            0x00c0fbdb      lea   ecx, dword [ebp-0x38]
            0x00c0fbde      call  0xb581e0
            0x00c0fbe3      push  dword [ebp+0x0c]
            0x00c0fbe6      lea   eax, dword [ebp-0x38]
            0x00c0fbe9      mov   dword [ebp-0x04], 0x00
            0x00c0fbf0      push  eax
            0x00c0fbf1      mov   ecx, esi
            0x00c0fbf3      call  0xc06c20
            0x00c0fbf8      lea   ecx, dword [ebp-0x38]
            0x00c0fbfb      call  0xb589a0
            0x00c0fc00      mov   ecx, dword [ebp-0x0c]
            0x00c0fc03      mov   dword fs:[0x0], ecx
            0x00c0fc0a      pop   ecx
            0x00c0fc0b      pop   esi
            0x00c0fc0c      mov   esp, ebp
            0x00c0fc0e      pop   ebp
            0x00c0fc0f      ret   0x08
            0x00c0fc12      int3
            0x00c0fc13      int3
            0x00c0fc14      int3
            0x00c0fc15      int3
            0x00c0fc16      int3
            0x00c0fc17      int3
            0x00c0fc18      int3
            0x00c0fc19      int3
            0x00c0fc1a      int3
            0x00c0fc1b      int3
            0x00c0fc1c      int3
            0x00c0fc1d      int3
            0x00c0fc1e      int3
            0x00c0fc1f      int3
            0x00c0fc20      push  ebp
            0x00c0fc21      mov   ebp, esp
            0x00c0fc23      push  0xffffffff                           ; 255
            0x00c0fc25      push  0x184d3f8
            0x00c0fc2a      mov   eax, dword fs:[0x0]
            0x00c0f530      push  ebp
            0x00c0f531      mov   ebp, esp
            0x00c0f533      push  0xffffffff                           ; 255
            0x00c0f535      push  0x184d3f8
            0x00c0f53a      mov   eax, dword fs:[0x0]
            0x00c0f540      push  eax
            0x00c0f541      sub   esp, 0x2c
            0x00c0f544      push  esi
            0x00c0f545      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0f54a      xor   eax, ebp
            0x00c0f54c      push  eax
            0x00c0f54d      lea   eax, dword [ebp-0x0c]
            0x00c0f550      mov   dword fs:[0x0], eax
            0x00c0f556      mov   esi, ecx
            0x00c0f558      push  dword [ebp+0x08]
            0x00c0f55b      lea   ecx, dword [ebp-0x38]
            0x00c0f55e      call  0xb580a0
            0x00c0f563      push  dword [ebp+0x0c]
            0x00c0f566      lea   eax, dword [ebp-0x38]
            0x00c0f569      mov   dword [ebp-0x04], 0x00
            0x00c0f570      push  eax
            0x00c0f571      mov   ecx, esi
            0x00c0f573      call  0xc06ba0
            0x00c0f578      lea   ecx, dword [ebp-0x38]
            0x00c0f57b      call  0xb589a0
            0x00c0f580      mov   ecx, dword [ebp-0x0c]
            0x00c0f583      mov   dword fs:[0x0], ecx
            0x00c0f58a      pop   ecx
            0x00c0f58b      pop   esi
            0x00c0f58c      mov   esp, ebp
            0x00c0f58e      pop   ebp
            0x00c0f58f      ret   0x08
            0x00c0f592      int3
            0x00c0f593      int3
            0x00c0f594      int3
            0x00c0f595      int3
            0x00c0f596      int3
            0x00c0f597      int3
            0x00c0f598      int3
            0x00c0f599      int3
            0x00c0f59a      int3
            0x00c0f59b      int3
            0x00c0f59c      int3
            0x00c0f59d      int3
            0x00c0f59e      int3
            0x00c0f59f      int3
            0x00c0f5a0      push  ebp
            0x00c0f5a1      mov   ebp, esp
            0x00c0f5a3      push  0xffffffff                           ; 255
            0x00c0f5a5      push  0x184d368
            0x00c0f5aa      mov   eax, dword fs:[0x0]
            0x00c0f5b0      push  eax
            0x00c0f5b1      sub   esp, 0x1c
            0x00c0f5b4      push  esi
            0x00c0f5b5      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0f5ba      xor   eax, ebp
            0x00c0f5bc      push  eax
            0x00c0f5bd      lea   eax, dword [ebp-0x0c]
            0x00c0f5c0      mov   dword fs:[0x0], eax
            0x00c0f5c6      mov   esi, ecx
            0x00c0f5c8      push  dword [ebp+0x08]
            0x00c0f5cb      lea   ecx, dword [ebp-0x28]
            0x00c0f5ce      call  0xb58330
            0x00c0f5d3      push  dword [ebp+0x0c]
            0x00c0f5d6      lea   eax, dword [ebp-0x28]
            0x00c0f5d9      mov   dword [ebp-0x04], 0x00
            0x00c0f5e0      push  eax
            0x00c0f5e1      mov   ecx, esi
            0x00c0f5e3      call  0xc06da0
            0x00c0f5e8      lea   ecx, dword [ebp-0x28]
            0x00c0f5eb      call  0xb589c0
            0x00c0f5f0      mov   ecx, dword [ebp-0x0c]
            0x00c0f5f3      mov   dword fs:[0x0], ecx
            0x00c0f5fa      pop   ecx
            0x00c0f5fb      pop   esi
            0x00c0f5fc      mov   esp, ebp
            0x00c0f5fe      pop   ebp
            0x00c0f5ff      ret   0x08
            0x00c0f602      int3
            0x00c0f603      int3
            0x00c0f604      int3
            0x00c0f605      int3
            0x00c0f606      int3
            0x00c0f607      int3
            0x00c0f608      int3
            0x00c0f609      int3
            0x00c0f60a      int3
            0x00c0f60b      int3
            0x00c0f60c      int3
            0x00c0f60d      int3
            0x00c0f60e      int3
            0x00c0f60f      int3
            0x00c0f610      push  ebp
            0x00c0f611      mov   ebp, esp
            0x00c0f613      push  0xffffffff                           ; 255
            0x00c0f615      push  0x184d3f8
            0x00c0f61a      mov   eax, dword fs:[0x0]
            0x00c0f620      push  eax
            0x00c0f621      sub   esp, 0x2c
            0x00c0f624      push  esi
            0x00c0f625      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0f62a      xor   eax, ebp
            0x00c0f62c      push  eax
            0x00c0f62d      lea   eax, dword [ebp-0x0c]
            0x00c0f630      mov   dword fs:[0x0], eax
            0x00c0f636      mov   esi, ecx
            0x00c0f638      push  dword [ebp+0x08]
            0x00c0f63b      lea   ecx, dword [ebp-0x38]
            0x00c0f63e      invalid
            0x00c0f63f      popfd
            0x00b2cc00      push  ebp
            0x00b2cc01      mov   ebp, esp
            0x00b2cc03      push  0xffffffff                           ; 255
            0x00b2cc05      push  0x1868fe8
            0x00b2cc0a      mov   eax, dword fs:[0x0]
            0x00b2cc10      push  eax
            0x00b2cc11      sub   esp, 0x50
            0x00b2cc14      push  esi
            0x00b2cc15      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2cc1a      xor   eax, ebp
            0x00b2cc1c      push  eax
            0x00b2cc1d      lea   eax, dword [ebp-0x0c]
            0x00b2cc20      mov   dword fs:[0x0], eax
            0x00b2cc26      mov   esi, ecx
            0x00b2cc28      lea   eax, dword [esi+0x04]
            0x00b2cc2b      push  eax
            0x00b2cc2c      lea   ecx, dword [ebp-0x5c]
            0x00b2cc2f      call  0xb2a420
            0x00b2cc34      lea   eax, dword [ebp-0x5c]
            0x00b2cc37      mov   dword [ebp-0x04], 0x00
            0x00b2cc3e      push  eax
            0x00b2cc3f      mov   ecx, esi
            0x00b2cc41      call  0xcfd2a0
            0x00b2cc46      cmp   dword [ebp-0x1c], 0x00
            0x00b2cc4a      mov   dword [ebp-0x04], 0x01
            0x00b2cc51      mov   dword [ebp-0x10], 0x00
        ,=< 0x00b2cc58      jz    0xb2cc6e
        |   0x00b2cc5a      push  dword [ebp-0x14]
        |   0x00b2cc5d      push  0x00
        |   0x00b2cc5f      call  0x5291c0
        |   0x00b2cc64      add   esp, 0x08
        |   0x00b2cc67      mov   dword [ebp-0x1c], 0x00
        `-> 0x00b2cc6e      lea   ecx, dword [ebp-0x58]
            0x00b2cc71      call  0x975700
            0x00b2cc76      lea   ecx, dword [ebp-0x5c]
            0x00b2cc79      call  0x4dc500
            0x00b2cc7e      mov   ecx, dword [ebp-0x0c]
            0x00b2cc81      mov   dword fs:[0x0], ecx
            0x00b2cc88      pop   ecx
            0x00b2cc89      pop   esi
            0x00b2cc8a      mov   esp, ebp
            0x00b2cc8c      pop   ebp
            0x00b2cc8d      ret   0x08
            0x00b2cc90      push  ebp
            0x00b2cc91      lea   ebp, dword [esp-0x58]
            0x00b2cc95      sub   esp, 0x58
            0x00b2cc98      push  0xffffffff                           ; 255
            0x00b2cc9a      push  0x1869028
            0x00b2cc9f      mov   eax, dword fs:[0x0]
            0x00b2cca5      push  eax
            0x00b2cca6      sub   esp, 0x58
            0x00b2cca9      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2ccae      xor   eax, ebp
            0x00b2ccb0      mov   dword [ebp+0x54], eax
            0x00b2ccb3      push  ebx
            0x00b2ccb4      push  esi
            0x00b2ccb5      push  edi
            0x00b2ccb6      push  eax
            0x00b2ccb7      lea   eax, dword [ebp-0x0c]
            0x00b2ccba      mov   dword fs:[0x0], eax
            0x00b2ccc0      mov   esi, ecx
            0x00b2ccc2      mov   dword [ebp+0x3c], esi
            0x00b2ccc5      mov   ebx, dword [ebp+0x60]
            0x00b2ccc8      lea   eax, dword [esi+0xf8]
            0x00b2ccce      mov   edi, dword [ebp+0x64]
            0x00b2ccd1      lea   ecx, dword [ebp+0x38]
            0x00b2ccd4      push  eax
            0x00b2ccd5      call  0x4e6c30
            0x00b2ccda      mov   eax, dword [esi+0xf4]
            0x00b2cce0      lea   ecx, dword [ebp-0x64]
            0x00b2cce3      mov   dword [ebp+0x34], eax
            0x00b2cce6      lea   eax, dword [esi+0xd0]
            0x00b2ccec      push  eax
            0x00b2cced      mov   dword [ebp-0x04], 0x00
            0x00b2ccf4      call  0xabb0d0
            0x00b2ccf9      movss xmm0, dword [esi+0xc8]
            0x00b2cd01      lea   eax, dword [esi+0x60]
            0x00b2cd04      movss dword [ebp+0x4c], xmm0
            0x00b2cd09      movss xmm0, dword [esi+0xcc]
            0x00b2cd11      movss dword [ebp+0x50], xmm0
            0x00b2cd16      movss xmm0, dword [esi+0xbc]
            0x00b2cd1e      push  eax
            0x00b2cd1f      movss dword [ebp+0x40], xmm0
            0x00b2cd24      lea   eax, dword [ebp-0x40]
            0x00b2cd27      movss xmm0, dword [esi+0xc0]
            0x00b2cd2f      push  edi
0x019a1b00  0x004dc500 0x00b37ea0 0x004dc500 0x01b9b134  ..M..~....M.4...
0x019a1b10  0x00b2c0c0 0x0051c100 0x0058f560 0x0058f530  ......Q.`.X.0.X.
0x019a1b20  0x004dc500 0x00b37e80 0x004dc500 0x01b9a674  ..M..~....M.t...
0x019a1b30  0x00b2b5b0 0x00514c80 0x00a2d830 0x004d7b40  .....LQ.0...@{M.
0x019a1b40  0xaaaaaaab 0x40d046aa 0xaaaaaaaa 0x40e046aa  .....F.@.....F.@
0x019a1b50  0x00000000 0x40f5f900 0x00000000 0x00000000  .......@........
0x019a1b60  0xffffffff 0x00000000 0x00000000 0x00000000  ................
0x019a1b70  0x00000000 0xffffffff 0x00000000 0x00000000  ................
0x019a1b80  0x00000000 0x00000000 0xffffffff 0x00000000  ................
0x019a1b90  0x7fffffff 0x7fffffff 0x7fffffff 0x7fffffff  ................
0x019a1ba0  0x3f800000 0x3f317283 0x3e75e85c 0x3d64cbf4  ...?.r1?\.u>..d=
