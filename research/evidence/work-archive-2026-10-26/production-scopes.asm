            0x00b599a0      sub   esp, 0x08
            0x00b599a3      push  ebx
            0x00b599a4      mov   ebx, dword [esp+0x10]
            0x00b599a8      push  edi
            0x00b599a9      mov   edi, ecx
            0x00b599ab      mov   dword [esp+0x0c], 0x00
            0x00b599b3      cmp   byte [edi+0x10], 0x00
            0x00b599b7      mov   eax, dword [edi+0x04]
            0x00b599ba      mov   dword [esp+0x08], eax
        ,=< 0x00b599be      jz    0xb599c4
        |   0x00b599c0      mov   byte [ebx+0x10], 0x01
        `-> 0x00b599c4      cmp   byte [edi+0x11], 0x00
        ,=< 0x00b599c8      jz    0xb599ce
        |   0x00b599ca      mov   byte [ebx+0x11], 0x01
        `-> 0x00b599ce      push  0x08                                 ; 8
            0x00b599d0      lea   eax, dword [esp+0x0c]
            0x00b599d4      push  eax
            0x00b599d5      call  0xb5abf0
            0x00b599da      mov   eax, dword [esp+0x08]
            0x00b599de      mov   dword [ebx+0x04], eax
            0x00b599e1      mov   eax, dword [esp+0x0c]
            0x00b599e5      test  eax, eax
        ,=< 0x00b599e7      jz    0xb59a0e
        |   0x00b599e9      push  esi
        |   0x00b599ea      mov   esi, dword [edi+0x20]
        |   0x00b599ed      lea   ecx, dword [ebx+0x18]
        |   0x00b599f0      push  0x01                                 ; 1
        |   0x00b599f2      push  eax
        |   0x00b599f3      mov   eax, dword [edi+0x18]
        |   0x00b599f6      add   eax, esi
        |   0x00b599f8      push  eax
        |   0x00b599f9      call  0x519a30
        |   0x00b599fe      mov   eax, dword [esp+0x10]
        |   0x00b59a02      lea   ecx, dword [edi+0x18]
        |   0x00b59a05      add   eax, esi
        |   0x00b59a07      push  eax
        |   0x00b59a08      call  0x519200
        |   0x00b59a0d      pop   esi
        `-> 0x00b59a0e      pop   edi
            0x00b59a0f      pop   ebx
            0x00b59a10      add   esp, 0x08
            0x00b59a13      ret   0x04
            0x00b59a16      int3
            0x00b59a17      int3
            0x00b59a18      int3
            0x00b59a19      int3
            0x00b59a1a      int3
            0x00b59a1b      int3
            0x00b59a1c      int3
            0x00b59a1d      int3
            0x00b59a1e      int3
            0x00b59a1f      int3
            0x00b59a20      push  ecx
            0x00b59a21      push  0x18                                 ; 24
            0x00b59a23      call  0xb58c10
            0x00b59a28      add   esp, 0x04
            0x00b59a2b      mov   dword [esp], eax
            0x00b59a2e      test  eax, eax
        ,=< 0x00b59a30      jz    0xb59a4f
        |   0x00b59a32      mov   dword [eax], 0x19a3134               ; [0x19a3134:4]=0xb59240
        |   0x00b59a38      mov   dword [eax+0x08], 0x00
        |   0x00b59a3f      mov   dword [eax+0x10], 0x00
        |   0x00b59a46      mov   dword [eax+0x14], 0x00
        |   0x00b59a4d      pop   ecx
        |   0x00b59a4e      ret
        `-> 0x00b59a4f      xor   eax, eax
            0x00b59a51      pop   ecx
            0x00b59a52      ret
            0x00b59a53      int3
            0x00b59a54      int3
            0x00b59a55      int3
            0x00b59a56      int3
            0x00b59a57      int3
            0x00b59a58      int3
            0x00b59a59      int3
            0x00b59a5a      int3
            0x00b59a5b      int3
            0x00b59a5c      int3
            0x00b59a5d      int3
            0x00b59a5e      int3
            0x00b59a5f      int3
            0x00b59a60      push  ebp
            0x00b59a61      mov   ebp, esp
            0x00b59a63      push  0xffffffff                           ; 255
            0x00b59a65      push  0x1848d23
            0x00b59a6a      mov   eax, dword fs:[0x0]
            0x00b59a70      push  eax
            0x00b59a71      push  ecx
            0x00b59a72      push  esi
            0x00b59a73      push  edi
            0x00b59a74      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b59a79      xor   eax, ebp
            0x00b59a7b      push  eax
            0x00b59a7c      lea   eax, dword [ebp-0x0c]
            0x00b59a7f      mov   dword fs:[0x0], eax
            0x00b59a85      mov   edi, ecx
            0x00b59a87      push  dword [0x1d6c084]
            0x00b59a8d      push  0x01                                 ; 1
            0x00b59a8f      push  0x98                                 ; 152
            0x00b59a94      push  0x01                                 ; 1
            0x00b59a96      call  0x529280
            0x00b59a9b      mov   esi, eax
            0x00b59a9d      add   esp, 0x10
            0x00b59aa0      mov   dword [ebp-0x10], esi
            0x00b59aa3      mov   dword [ebp-0x04], 0x00
            0x00b59aaa      test  esi, esi
        ,=< 0x00b59aac      jz    0xb59bc5
        |   0x00b59ab2      push  edi
        |   0x00b59ab3      mov   ecx, esi
        |   0x00b59ab5      call  0xb02ff0
        |   0x00b59aba      mov   dword [esi], 0x19a32b8               ; [0x19a32b8:4]=0x4d7b40
        |   0x00b59ac0      mov   dword [esi+0x10], 0x00
        |   0x00b59ac7      mov   dword [esi+0x14], 0x00
        |   0x00b59ace      mov   dword [esi+0x18], 0x00
        |   0x00b59ad5      mov   dword [esi+0x1c], 0x00
        |   0x00b59adc      mov   dword [esi+0x20], 0x00
        |   0x00b59ae3      mov   dword [esi+0x24], 0x00
        |   0x00b59aea      mov   dword [esi+0x28], 0x00
        |   0x00b59af1      mov   dword [esi+0x2c], 0x7f7fffff         ; [0x7f7fffff:4]=-1
        |   0x00b59af8      mov   dword [esi+0x30], 0x00
        |   0x00b59aff      mov   dword [esi+0x34], 0x00
        |   0x00b59b06      mov   dword [esi+0x38], 0x00
        |   0x00b59b0d      mov   dword [esi+0x3c], 0x00
        |   0x00b59b14      mov   dword [esi+0x40], 0x00
        |   0x00b59b1b      mov   dword [esi+0x44], 0x00
        |   0x00b59b22      mov   dword [esi+0x48], 0x00
        |   0x00b59b29      mov   dword [esi+0x4c], 0x00
        |   0x00b59b30      mov   eax, dword [esi+0x48]
        |   0x00b59b33      mov   dword [esi+0x50], eax
        |   0x00b59b36      mov   eax, dword [esi+0x48]
        |   0x00b59b39      mov   dword [esi+0x54], eax
        |   0x00b59b3c      mov   eax, dword [esi+0x48]
        |   0x00b59b3f      mov   dword [esi+0x58], eax
        |   0x00b59b42      mov   eax, dword [esi+0x48]
        |   0x00b59b45      mov   dword [esi+0x5c], eax
        |   0x00b59b48      mov   eax, dword [esi+0x48]
        |   0x00b59b4b      mov   dword [esi+0x60], eax
        |   0x00b59b4e      mov   eax, dword [esi+0x48]
        |   0x00b59b51      mov   dword [esi+0x64], eax
        |   0x00b59b54      mov   eax, dword [esi+0x48]
        |   0x00b59b57      mov   dword [esi+0x68], eax
        |   0x00b59b5a      mov   eax, dword [esi+0x48]
        |   0x00b59b5d      mov   dword [esi+0x6c], eax
        |   0x00b59b60      mov   dword [esi+0x70], 0x00
        |   0x00b59b67      mov   dword [esi+0x74], 0x00
        |   0x00b59b6e      mov   eax, dword [esi+0x70]
        |   0x00b59b71      mov   dword [esi+0x78], eax
        |   0x00b59b74      mov   eax, dword [esi+0x70]
        |   0x00b59b77      mov   dword [esi+0x7c], eax
        |   0x00b59b7a      mov   eax, dword [esi+0x70]
        |   0x00b59b7d      mov   dword [esi+0x80], eax
        |   0x00b59b83      mov   eax, dword [esi+0x70]
        |   0x00b59b86      mov   dword [esi+0x84], eax
        |   0x00b59b8c      mov   eax, esi
        |   0x00b59b8e      mov   ecx, dword [esi+0x70]
        |   0x00b59b91      mov   dword [esi+0x88], ecx
        |   0x00b59b97      mov   ecx, dword [esi+0x70]
        |   0x00b59b9a      mov   dword [esi+0x8c], ecx
        |   0x00b59ba0      mov   ecx, dword [esi+0x70]
        |   0x00b59ba3      mov   dword [esi+0x90], ecx
        |   0x00b59ba9      mov   ecx, dword [esi+0x70]
        |   0x00b59bac      mov   dword [esi+0x94], ecx
        |   0x00b59bb2      mov   ecx, dword [ebp-0x0c]
        |   0x00b59bb5      mov   dword fs:[0x0], ecx
        |   0x00b59bbc      pop   ecx
        |   0x00b59bbd      pop   edi
        |   0x00b59bbe      pop   esi
        |   0x00b59bbf      mov   esp, ebp
        |   0x00b59bc1      pop   ebp
        |   0x00b59bc2      ret   0x0c
        `-> 0x00b59bc5      xor   eax, eax
            0x00b59bc7      mov   ecx, dword [ebp-0x0c]
            0x00b59bca      mov   dword fs:[0x0], ecx
            0x00b59bd1      pop   ecx
            0x00b59bd2      pop   edi
            0x00b59bd3      pop   esi
            0x00b59bd4      mov   esp, ebp
            0x00b59bd6      pop   ebp
            0x00b59bd7      ret   0x0c
            0x00b59bda      int3
            0x00b59bdb      int3
            0x00b59bdc      int3
            0x00b59bdd      int3
            0x00b59bde      int3
            0x00b59bdf      int3
            0x00b59be0      push  ebp
            0x00b59be1      mov   ebp, esp
            0x00b59be3      push  0xffffffff                           ; 255
            0x00b59be5      push  0x1810663
            0x00b59bea      mov   eax, dword fs:[0x0]
            0x00b59bf0      push  eax
            0x00b59bf1      push  ecx
            0x00b59bf2      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b59bf7      xor   eax, ebp
            0x00b59bf9      push  eax
            0x00b59bfa      lea   eax, dword [ebp-0x0c]
            0x00b59bfd      mov   dword fs:[0x0], eax
            0x00b59c03      cmp   dword [0x2003014], 0x00              ; [0x2003014:4]=0
        ,=< 0x00b59c0a      jnz   0xb59c11
        |   0x00b59c0c      call  0x557da0
        `-> 0x00b59c11      mov   eax, dword [0x203b720]               ; [0x203b720:4]=0
            0x00b59c16      test  eax, eax
        ,=< 0x00b59c18      jnz   0xb59c75
        |   0x00b59c1a      push  dword [0x1d6c084]
        |   0x00b59c20      push  0x01                                 ; 1
        |   0x00b59c22      push  0xac                                 ; 172
        |   0x00b59c27      push  0x01                                 ; 1
        |   0x00b59c29      call  0x529280
        |   0x00b59c2e      add   esp, 0x10
        |   0x00b59c31      mov   dword [ebp-0x10], eax
        |   0x00b59c34      mov   dword [ebp-0x04], 0x00
        |   0x00b59c3b      test  eax, eax
       ,==< 0x00b59c3d      jz    0xb59c6e
       ||   0x00b59c3f      push  0x00
       ||   0x00b59c41      push  0x10                                 ; 16
       ||   0x00b59c43      push  str.TCurrentSavingVersion            ; 0x19a31cc ; "TCurrentSavingVersion"
       ||   0x00b59c48      push  0xb5aeb0
       ||   0x00b59c4d      push  dword [0x2003014]
       ||   0x00b59c53      mov   ecx, eax
       ||   0x00b59c55      call  0x54f0b0
       ||   0x00b59c5a      mov   dword [0x203b720], eax
       ||   0x00b59c5f      mov   ecx, dword [ebp-0x0c]
       ||   0x00b59c62      mov   dword fs:[0x0], ecx
       ||   0x00b59c69      pop   ecx
       ||   0x00b59c6a      mov   esp, ebp
       ||   0x00b59c6c      pop   ebp
       ||   0x00b59c6d      ret
       `--> 0x00b59c6e      xor   eax, eax
        |   0x00b59c70      mov   dword [0x203b720], eax
        `-> 0x00b59c75      mov   ecx, dword [ebp-0x0c]
            0x00b59c78      mov   dword fs:[0x0], ecx
            0x00b59c7f      pop   ecx
            0x00b59c80      mov   esp, ebp
            0x00b59c82      pop   ebp
            0x00b59c83      ret
            0x00b59c84      int3
            0x00b59c85      int3
            0x00b59c86      int3
            0x00b59c87      int3
            0x00b59c88      int3
            0x00b59c89      int3
            0x00b59c8a      int3
            0x00b59c8b      int3
            0x00b59c8c      int3
            0x00b59c8d      int3
            0x00b59c8e      int3
            0x00b59c8f      int3
            0x00b59c90      push  ebp
            0x00b59c91      mov   ebp, esp
            0x00b59c93      push  0xffffffff                           ; 255
            0x00b59c95      push  0x1810663
            0x00b59c9a      mov   eax, dword fs:[0x0]
            0x00b59ca0      push  eax
            0x00b59ca1      push  ecx
            0x00b59ca2      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b59ca7      xor   eax, ebp
            0x00b59ca9      push  eax
            0x00b59caa      lea   eax, dword [ebp-0x0c]
            0x00b59cad      mov   dword fs:[0x0], eax
            0x00b59cb3      cmp   dword [0x2003014], 0x00              ; [0x2003014:4]=0
        ,=< 0x00b59cba      jnz   0xb59cc1
        |   0x00b59cbc      call  0x557da0
        `-> 0x00b59cc1      mov   eax, dword [0x203b72c]               ; [0x203b72c:4]=0
            0x00b59cc6      test  eax, eax
        ,=< 0x00b59cc8      jnz   0xb59d25
        |   0x00b59cca      push  dword [0x1d6c084]
        |   0x00b59cd0      push  0x01                                 ; 1
        |   0x00b59cd2      push  0xac                                 ; 172
        |   0x00b59cd7      push  0x01                                 ; 1
        |   0x00b59cd9      call  0x529280
        |   0x00b59cde      add   esp, 0x10
        |   0x00b59ce1      mov   dword [ebp-0x10], eax
        |   0x00b59ce4      mov   dword [ebp-0x04], 0x00
        |   0x00b59ceb      test  eax, eax
       ,==< 0x00b59ced      jz    0xb59d1e
       ||   0x00b59cef      push  0x01                                 ; 1
       ||   0x00b59cf1      push  0x1c                                 ; 28
       ||   0x00b59cf3      push  str.TSaveableDescriptor              ; 0x19a3104 ; "TSaveableDescriptor"
       ||   0x00b59cf8      push  0x4de290
       ||   0x00b59cfd      push  dword [0x2003014]
       ||   0x00b59d03      mov   ecx, eax
       ||   0x00b59d05      call  0x54f0b0
       ||   0x00b59d0a      mov   dword [0x203b72c], eax
       ||   0x00b59d0f      mov   ecx, dword [ebp-0x0c]
       ||   0x00b59d12      mov   dword fs:[0x0], ecx
       ||   0x00b59d19      pop   ecx
       ||   0x00b59d1a      mov   esp, ebp
       ||   0x00b59d1c      pop   ebp
       ||   0x00b59d1d      ret
       `--> 0x00b59d1e      xor   eax, eax
        |   0x00b59d20      mov   dword [0x203b72c], eax
        `-> 0x00b59d25      mov   ecx, dword [ebp-0x0c]
            0x00b59d28      mov   dword fs:[0x0], ecx
            0x00b59d2f      pop   ecx
            0x00b59d30      mov   esp, ebp
            0x00b59d32      pop   ebp
            0x00b59d33      ret
            0x00b59d34      int3
            0x00b59d35      int3
            0x00b59d36      int3
            0x00b59d37      int3
            0x00b59d38      int3
            0x00b59d39      int3
            0x00b59d3a      int3
            0x00b59d3b      int3
            0x00b59d3c      int3
            0x00b59d3d      int3
            0x00b59d3e      int3
            0x00b59d3f      int3
            0x00b59d40      push  ebp
            0x00b59d41      mov   ebp, esp
            0x00b59d43      push  0xffffffff                           ; 255
            0x00b59d45      push  0x1810663
            0x00b59d4a      mov   eax, dword fs:[0x0]
            0x00b59d50      push  eax
            0x00b59d51      push  ecx
            0x00b59d52      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b59d57      xor   eax, ebp
            0x00b59d59      push  eax
            0x00b59d5a      lea   eax, dword [ebp-0x0c]
            0x00b59d5d      mov   dword fs:[0x0], eax
            0x00b59d63      cmp   dword [0x203a2ac], 0x00              ; [0x203a2ac:4]=0
        ,=< 0x00b59d6a      jnz   0xb59d71
        |   0x00b59d6c      call  0xb05260
        `-> 0x00b59d71      mov   eax, dword [0x203b728]               ; [0x203b728:4]=0
            0x00b59d76      test  eax, eax
        ,=< 0x00b59d78      jnz   0xb59dd8
        |   0x00b59d7a      push  dword [0x1d6c084]
        |   0x00b59d80      push  0x01                                 ; 1
        |   0x00b59d82      push  0xac                                 ; 172
        |   0x00b59d87      push  0x01                                 ; 1
        |   0x00b59d89      call  0x529280
        |   0x00b59d8e      add   esp, 0x10
        |   0x00b59d91      mov   dword [ebp-0x10], eax
        |   0x00b59d94      mov   dword [ebp-0x04], 0x00
        |   0x00b59d9b      test  eax, eax
       ,==< 0x00b59d9d      jz    0xb59dd1
       ||   0x00b59d9f      invalid
            0x00a66fc0      sub   esp, 0x34
            0x00a66fc3      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00a66fc8      xor   eax, esp
            0x00a66fca      mov   dword [esp+0x30], eax
            0x00a66fce      push  esi
            0x00a66fcf      mov   esi, ecx
            0x00a66fd1      lea   ecx, dword [esp+0x14]
            0x00a66fd5      push  edi
            0x00a66fd6      mov   edi, dword [esp+0x40]
            0x00a66fda      call  0x4f71f0
            0x00a66fdf      lea   eax, dword [esi-0x14]
            0x00a66fe2      mov   dword [esp+0x14], 0x00
            0x00a66fea      neg   esi
            0x00a66fec      mov   dword [esp+0x10], 0x00
            0x00a66ff4      push  0x04                                 ; 4
            0x00a66ff6      sbb   esi, esi
            0x00a66ff8      mov   dword [esp+0x10], 0x00
            0x00a67000      and   esi, eax
            0x00a67002      mov   dword [esp+0x0c], 0x00
            0x00a6700a      lea   eax, dword [esp+0x18]
            0x00a6700e      mov   ecx, esi
            0x00a67010      push  eax
            0x00a67011      call  0xb5abf0
            0x00a67016      push  0x04                                 ; 4
            0x00a67018      lea   eax, dword [esp+0x14]
            0x00a6701c      mov   ecx, esi
            0x00a6701e      push  eax
            0x00a6701f      call  0xb5abf0
            0x00a67024      push  0x04                                 ; 4
            0x00a67026      lea   eax, dword [esp+0x10]
            0x00a6702a      mov   ecx, esi
            0x00a6702c      push  eax
            0x00a6702d      call  0xb5abf0
            0x00a67032      push  0x04                                 ; 4
            0x00a67034      lea   eax, dword [esp+0x0c]
            0x00a67038      mov   ecx, esi
            0x00a6703a      push  eax
            0x00a6703b      call  0xb5abf0
            0x00a67040      push  dword [esp+0x08]
            0x00a67044      lea   ecx, dword [esp+0x2c]
            0x00a67048      push  dword [esp+0x10]
            0x00a6704c      push  dword [esp+0x18]
            0x00a67050      push  dword [esp+0x20]
            0x00a67054      call  0x4f71d0
            0x00a67059      push  eax
            0x00a6705a      lea   ecx, dword [esp+0x1c]
            0x00a6705e      call  0x4f70d0
            0x00a67063      lea   eax, dword [esp+0x18]
            0x00a67067      push  0x00
            0x00a67069      push  eax
            0x00a6706a      call  0xb5abd0
            0x00a6706f      mov   ecx, dword [esp+0x40]
            0x00a67073      add   esp, 0x08
            0x00a67076      mov   dword [edi], eax
            0x00a67078      pop   edi
            0x00a67079      pop   esi
            0x00a6707a      xor   ecx, esp
            0x00a6707c      call  0x18075f6
            0x00a67081      add   esp, 0x34
            0x00a67084      ret   0x08
            0x00a67087      int3
            0x00a67088      int3
            0x00a67089      int3
            0x00a6708a      int3
            0x00a6708b      int3
            0x00a6708c      int3
            0x00a6708d      int3
            0x00a6708e      int3
            0x00a6708f      int3
            0x00a67090      push  ebp
            0x00a67091      mov   ebp, esp
            0x00a67093      push  0xffffffff                           ; 255
            0x00a67095      push  0x185ee70
            0x00a6709a      mov   eax, dword fs:[0x0]
            0x00a670a0      push  eax
            0x00a670a1      sub   esp, 0x24
            0x00a670a4      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00a670a9      xor   eax, ebp
            0x00a670ab      mov   dword [ebp-0x10], eax
            0x00a670ae      push  esi
            0x00a670af      push  edi
            0x00a670b0      push  eax
            0x00a670b1      lea   eax, dword [ebp-0x0c]
            0x00a670b4      mov   dword fs:[0x0], eax
            0x00a670ba      mov   edi, ecx
            0x00a670bc      lea   eax, dword [edi-0x14]
            0x00a670bf      mov   dword [ebp-0x18], 0x00
            0x00a670c6      neg   edi
            0x00a670c8      push  0x04                                 ; 4
            0x00a670ca      sbb   edi, edi
            0x00a670cc      and   edi, eax
            0x00a670ce      lea   eax, dword [ebp-0x18]
            0x00a670d1      push  eax
            0x00a670d2      mov   ecx, edi
            0x00a670d4      call  0xb5abf0
            0x00a670d9      mov   esi, dword [ebp-0x18]
            0x00a670dc      lea   eax, dword [esi+0x0f]
            0x00a670df      cmp   eax, 0x4020                          ; ' @'
        ,=< 0x00a670e4      jnbe  0xa670ef
        |   0x00a670e6      call  0x18076c0
        |   0x00a670eb      mov   eax, esp
       ,==< 0x00a670ed      jmp   0xa670f1
       |`-> 0x00a670ef      xor   eax, eax
       `--> 0x00a670f1      add   eax, 0x0f                            ; 0xf ; 15
            0x00a670f4      lea   ecx, dword [ebp-0x30]
            0x00a670f7      and   eax, 0xfffffff0                      ; 4294967280
            0x00a670fa      push  esi
            0x00a670fb      push  eax
            0x00a670fc      mov   dword [ebp-0x28], eax
            0x00a670ff      call  0x4ea610
            0x00a67104      mov   ecx, dword [ebp-0x28]
            0x00a67107      mov   dword [ebp-0x24], ecx
            0x00a6710a      mov   dword [ebp-0x20], esi
            0x00a6710d      mov   eax, dword [ebp-0x18]
            0x00a67110      xor   esi, esi
            0x00a67112      mov   dword [ebp-0x04], 0x00
            0x00a67119      test  eax, eax
        ,=< 0x00a6711b      jz    0xa67141
        |   0x00a6711d      nop   dword [eax], eax
       .--> 0x00a67120      push  0x01                                 ; 1
       :|   0x00a67122      lea   eax, dword [ebp-0x11]
       :|   0x00a67125      mov   ecx, edi
       :|   0x00a67127      push  eax
       :|   0x00a67128      call  0xb5abf0
       :|   0x00a6712d      mov   ecx, dword [ebp-0x24]
       :|   0x00a67130      mov   al, byte [ebp-0x11]
       :|   0x00a67133      mov   byte [ecx+esi*1], al
       :|   0x00a67136      inc   esi
       :|   0x00a67137      mov   eax, dword [ebp-0x18]
       :|   0x00a6713a      cmp   esi, eax
       `==< 0x00a6713c      jb    0xa67120
        |   0x00a6713e      invalid
        |   0x00a6713f      dec   ebp
            0x0051d1e0      push  esi
            0x0051d1e1      mov   esi, dword [esp+0x0c]
            0x0051d1e5      push  edi
            0x0051d1e6      mov   edi, ecx
            0x0051d1e8      mov   ecx, dword [esp+0x14]
            0x0051d1ec      mov   dword [ecx], 0x00
            0x0051d1f2      mov   edx, dword [edi+0x08]
            0x0051d1f5      lea   eax, dword [edx+esi*1]
            0x0051d1f8      cmp   eax, dword [edi+0x04]
        ,=< 0x0051d1fb      jbe   0x51d20b
        |   0x0051d1fd      mov   dword [ecx], 0x02
        |   0x0051d203      mov   esi, dword [edi+0x04]
        |   0x0051d206      mov   edx, dword [edi+0x08]
        |   0x0051d209      sub   esi, edx
        `-> 0x0051d20b      test  esi, esi
        ,=< 0x0051d20d      jnz   0x51d216
        |   0x0051d20f      pop   edi
        |   0x0051d210      xor   eax, eax
        |   0x0051d212      pop   esi
        |   0x0051d213      ret   0x0c
        `-> 0x0051d216      mov   ecx, dword [edi]
            0x0051d218      push  esi
            0x0051d219      add   ecx, edx
            0x0051d21b      push  ecx
            0x0051d21c      push  dword [esp+0x14]
            0x0051d220      call  0x1809b38
            0x0051d225      add   dword [edi+0x08], esi
            0x0051d228      add   esp, 0x0c
            0x0051d22b      mov   eax, esi
            0x0051d22d      pop   edi
            0x0051d22e      pop   esi
            0x0051d22f      ret   0x0c
            0x0051d232      int3
            0x0051d233      int3
            0x0051d234      int3
            0x0051d235      int3
            0x0051d236      int3
            0x0051d237      int3
            0x0051d238      int3
            0x0051d239      int3
            0x0051d23a      int3
            0x0051d23b      int3
            0x0051d23c      int3
            0x0051d23d      int3
            0x0051d23e      int3
            0x0051d23f      int3
            0x0051d240      push  esi
            0x0051d241      mov   esi, dword [esp+0x0c]
            0x0051d245      push  edi
            0x0051d246      mov   edi, ecx
            0x0051d248      mov   ecx, dword [esp+0x14]
            0x0051d24c      mov   dword [ecx], 0x00
            0x0051d252      mov   edx, dword [edi+0x40]
            0x0051d255      lea   eax, dword [edx+esi*1]
            0x0051d258      cmp   eax, dword [edi+0x4c]
        ,=< 0x0051d25b      jbe   0x51d26b
        |   0x0051d25d      mov   dword [ecx], 0x02
        |   0x0051d263      mov   esi, dword [edi+0x4c]
        |   0x0051d266      mov   edx, dword [edi+0x40]
        |   0x0051d269      sub   esi, edx
        `-> 0x0051d26b      test  esi, esi
        ,=< 0x0051d26d      jnz   0x51d276
        |   0x0051d26f      pop   edi
        |   0x0051d270      xor   eax, eax
        |   0x0051d272      pop   esi
        |   0x0051d273      ret   0x0c
        `-> 0x0051d276      mov   ecx, dword [edi+0x48]
            0x0051d279      push  esi
            0x0051d27a      add   ecx, edx
            0x0051d27c      push  ecx
            0x0051d27d      push  dword [esp+0x14]
            0x0051d281      call  0x1809b38
            0x0051d286      add   dword [edi+0x40], esi
            0x0051d289      add   esp, 0x0c
            0x0051d28c      mov   eax, esi
            0x0051d28e      pop   edi
            0x0051d28f      pop   esi
            0x0051d290      ret   0x0c
            0x0051d293      int3
            0x0051d294      int3
            0x0051d295      int3
            0x0051d296      int3
            0x0051d297      int3
            0x0051d298      int3
            0x0051d299      int3
            0x0051d29a      int3
            0x0051d29b      int3
            0x0051d29c      int3
            0x0051d29d      int3
            0x0051d29e      int3
            0x0051d29f      int3
            0x0051d2a0      push  esi
            0x0051d2a1      mov   esi, dword [esp+0x10]
            0x0051d2a5      push  edi
            0x0051d2a6      mov   edi, dword [esp+0x10]
            0x0051d2aa      push  edi
            0x0051d2ab      push  dword [esp+0x10]
            0x0051d2af      mov   dword [esi], 0x00
            0x0051d2b5      push  dword [ecx+0x0c]
            0x0051d2b8      call  dword [sym.imp.api_ms_win_crt_stdio_l1_1_0.dll__read] ; 0x1914a84 ; ssize_t read(int fildes, void *buf, size_t nbyte)
            0x0051d2be      add   esp, 0x0c
            0x0051d2c1      cmp   eax, edi
        ,=< 0x0051d2c3      jbe   0x51d2cf
        |   0x0051d2c5      xor   eax, eax
        |   0x0051d2c7      mov   dword [esi], 0x104                   ; [0x104:4]=-1 ; 260
        |   0x0051d2cd      cmp   eax, edi
       ,`-> 0x0051d2cf      jnb   0x51d2d7
       |    0x0051d2d1      mov   dword [esi], 0x02
       `--> 0x0051d2d7      pop   edi
            0x0051d2d8      pop   esi
            0x0051d2d9      ret   0x0c
            0x0051d2dc      int3
            0x0051d2dd      int3
            0x0051d2de      int3
            0x0051d2df      int3
            0x0051d2e0      push  esi
            0x0051d2e1      mov   esi, dword [esp+0x0c]
            0x0051d2e5      push  edi
            0x0051d2e6      mov   edi, ecx
            0x0051d2e8      mov   ecx, dword [esp+0x14]
            0x0051d2ec      mov   dword [ecx], 0x00
            0x0051d2f2      mov   edx, dword [edi+0x48]
            0x0051d2f5      lea   eax, dword [edx+esi*1]
            0x0051d2f8      cmp   eax, dword [edi+0x44]
        ,=< 0x0051d2fb      jbe   0x51d30b
        |   0x0051d2fd      mov   dword [ecx], 0x02
        |   0x0051d303      mov   esi, dword [edi+0x44]
        |   0x0051d306      mov   edx, dword [edi+0x48]
        |   0x0051d309      sub   esi, edx
        `-> 0x0051d30b      test  esi, esi
        ,=< 0x0051d30d      jnz   0x51d316
        |   0x0051d30f      pop   edi
        |   0x0051d310      xor   eax, eax
        |   0x0051d312      pop   esi
        |   0x0051d313      ret   0x0c
        `-> 0x0051d316      mov   ecx, dword [edi+0x40]
            0x0051d319      push  esi
            0x0051d31a      add   ecx, edx
            0x0051d31c      push  ecx
            0x0051d31d      push  dword [esp+0x14]
            0x0051d321      call  0x1809b38
            0x0051d326      add   dword [edi+0x48], esi
            0x0051d329      add   esp, 0x0c
            0x0051d32c      mov   eax, esi
            0x0051d32e      pop   edi
            0x0051d32f      pop   esi
            0x00b2fea0      push  ebp
            0x00b2fea1      mov   ebp, esp
            0x00b2fea3      push  0xffffffff                           ; 255
            0x00b2fea5      push  0x1810693
            0x00b2feaa      mov   eax, dword fs:[0x0]
            0x00b2feb0      push  eax
            0x00b2feb1      push  ecx
            0x00b2feb2      push  esi
            0x00b2feb3      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2feb8      xor   eax, ebp
            0x00b2feba      push  eax
            0x00b2febb      lea   eax, dword [ebp-0x0c]
            0x00b2febe      mov   dword fs:[0x0], eax
            0x00b2fec4      push  dword [0x1d6c084]
            0x00b2feca      push  0x01                                 ; 1
            0x00b2fecc      push  0x08                                 ; 8
            0x00b2fece      push  0x01                                 ; 1
            0x00b2fed0      call  0x529280
            0x00b2fed5      mov   esi, eax
            0x00b2fed7      add   esp, 0x10
            0x00b2feda      mov   dword [ebp-0x10], esi
            0x00b2fedd      mov   dword [ebp-0x04], 0x00
            0x00b2fee4      test  esi, esi
        ,=< 0x00b2fee6      jz    0xb2fef7
        |   0x00b2fee8      mov   ecx, esi
        |   0x00b2feea      call  0xb21f60
        |   0x00b2feef      mov   dword [esi], 0x19a1930               ; [0x19a1930:4]=0x561c50
       ,==< 0x00b2fef5      jmp   0xb2fef9
       |`-> 0x00b2fef7      xor   esi, esi
       `--> 0x00b2fef9      mov   ecx, dword [ebp+0x08]
            0x00b2fefc      lea   eax, dword [esi+0x04]
            0x00b2feff      push  eax
            0x00b2ff00      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b2ff07      call  0xb28ef0
            0x00b2ff0c      test  al, al
        ,=< 0x00b2ff0e      jnz   0xb2ff2f
        |   0x00b2ff10      test  esi, esi
       ,==< 0x00b2ff12      jz    0xb2ff1d
       ||   0x00b2ff14      mov   eax, dword [esi]
       ||   0x00b2ff16      mov   ecx, esi
       ||   0x00b2ff18      push  0x01                                 ; 1
       ||   0x00b2ff1a      call  dword [eax+0x08]                     ; 8
       `--> 0x00b2ff1d      xor   eax, eax
        |   0x00b2ff1f      mov   ecx, dword [ebp-0x0c]
        |   0x00b2ff22      mov   dword fs:[0x0], ecx
        |   0x00b2ff29      pop   ecx
        |   0x00b2ff2a      pop   esi
        |   0x00b2ff2b      mov   esp, ebp
        |   0x00b2ff2d      pop   ebp
        |   0x00b2ff2e      ret
        `-> 0x00b2ff2f      invalid
0x019a18d0  0x00b2ced0 0x00b2bdb0 0x00b314f0 0x01b9a924  ............$...
0x019a18e0  0x00561c50 0x00b2c680 0x00b2b890 0x00b30e60  P.V.........`...
0x019a18f0  0x01b9a970 0x00561c50 0x00b2c410 0x00b2b6d0  p...P.V.........
0x019a1900  0x00b30c20 0x01b9a9bc 0x00561c50 0x00b2c390   .......P.V.....
0x019a1910  0x00b2b6a0 0x00b30bb0 0x01b9aa08 0x00561c50  ............P.V.
0x019a1920  0x00b2c6c0 0x00b2b8c0 0x00b30ec0 0x01b9aa54  ............T...
0x019a1930  0x00561c50 0x00b2d0a0 0x00b2be40 0x00b316a0  P.V.....@.......
0x019a1940  0x01b9aaa0 0x005127a0 0x00b2cdf0 0x00b2bd00  .....'Q.........
0x019a1950  0x00b31410 0x01b9aaec 0x005127a0 0x00b2ce30  .........'Q.0...
0x019a1960  0x00b2bd30 0x00b31470 0x01b9ab38 0x005127a0  0...p...8....'Q.
0x019a1970  0x00b2c350 0x00b2b670 0x00b30b50 0x01b9ab84  P...p...P.......
0x019a1980  0x005127a0 0x00b2d200 0x00b2bf80 0x00b31840  .'Q.........@...
0x019a1990  0x01b9abd0 0x005127a0 0x00b2d390 0x00b2bfb0  .....'Q.........
0x019a19a0  0x00b318a0 0x01b9ac1c 0x005127a0 0x00b2d080  .........'Q.....
0x019a19b0  0x00b2be10 0x00b31630 0x01b9ac68 0x005127a0  ....0...h....'Q.
0x019a19c0  0x00b2d1a0 0x00b2bf50 0x00b317e0 0x01b9acb4  ....P...........
0x019a19d0  0x005127a0 0x00b2d6f0 0x00b2c060 0x00b31930  .'Q.....`...0...
0x019a19e0  0x01b9ad00 0x00561c50 0x00b2cb40 0x00b2bb50  ....P.V.@...P...
0x019a19f0  0x00b31240 0x01b9ad4c 0x00561c50 0x00b2ca90  @...L...P.V.....
0x019a1a00  0x00b2bad0 0x00b31190 0x01b9ad98 0x00561c50  ............P.V.
0x019a1a10  0x00b2ca40 0x00b2baa0 0x00b31120 0x01b9ade4  @....... .......
0x019a1a20  0x005127a0 0x00b2cc00 0x00b2bbb0 0x00b312e0  .'Q.............
            0x00c0cd90      push  ebp
            0x00c0cd91      mov   ebp, esp
            0x00c0cd93      push  0xffffffff                           ; 255
            0x00c0cd95      push  0x185ea78
            0x00c0cd9a      mov   eax, dword fs:[0x0]
            0x00c0cda0      push  eax
            0x00c0cda1      sub   esp, 0x0c
            0x00c0cda4      push  ebx
            0x00c0cda5      push  esi
            0x00c0cda6      push  edi
            0x00c0cda7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0cdac      xor   eax, ebp
            0x00c0cdae      push  eax
            0x00c0cdaf      lea   eax, dword [ebp-0x0c]
            0x00c0cdb2      mov   dword fs:[0x0], eax
            0x00c0cdb8      mov   ebx, ecx
            0x00c0cdba      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c0cdbf      xor   edx, edx
            0x00c0cdc1      xor   edi, edi
            0x00c0cdc3      mov   eax, dword [eax+0xe0]
            0x00c0cdc9      mov   dword [ebp-0x14], edx
            0x00c0cdcc      mov   dword [ebp-0x10], edi
            0x00c0cdcf      mov   ecx, dword [eax*4+0x20286d8]
            0x00c0cdd6      mov   dword [ebp-0x18], ecx
            0x00c0cdd9      test  ecx, ecx
        ,=< 0x00c0cddb      jz    0xc0cdf0
        |   0x00c0cddd      mov   eax, dword [ecx]
        |   0x00c0cddf      lea   edx, dword [ebp-0x14]
        |   0x00c0cde2      push  edi
        |   0x00c0cde3      push  edx
        |   0x00c0cde4      call  dword [eax+0x3c]                     ; 60
        |   0x00c0cde7      mov   edi, dword [ebp-0x10]
        |   0x00c0cdea      mov   edx, dword [ebp-0x14]
        |   0x00c0cded      mov   ecx, dword [ebp-0x18]
        `-> 0x00c0cdf0      mov   dword [ebp-0x04], 0x00
            0x00c0cdf7      test  ecx, ecx
        ,=< 0x00c0cdf9      jz    0xc0ce0b
        |   0x00c0cdfb      mov   eax, dword [ebx+0x08]
        |   0x00c0cdfe      movzx esi, word [eax+0x20]
        |   0x00c0ce02      cmp   esi, edi
       ,==< 0x00c0ce04      jnb   0xc0ce0b
       ||   0x00c0ce06      mov   esi, dword [edx+esi*4]
      ,===< 0x00c0ce09      jmp   0xc0ce0d
      |``-> 0x00c0ce0b      xor   esi, esi
      `---> 0x00c0ce0d      lea   ecx, dword [ebx+0x0c]
            0x00c0ce10      call  0xbcdbc0
            0x00c0ce15      push  eax
            0x00c0ce16      mov   ecx, esi
            0x00c0ce18      call  0xc182a0
            0x00c0ce1d      mov   ecx, dword [ebp-0x0c]
            0x00c0ce20      mov   dword fs:[0x0], ecx
            0x00c0ce27      pop   ecx
            0x00c0ce28      pop   edi
            0x00c0ce29      pop   esi
            0x00c0ce2a      pop   ebx
            0x00c0ce2b      mov   esp, ebp
            0x00c0ce2d      pop   ebp
            0x00c0ce2e      ret
            0x00c0ce2f      int3
            0x00c0ce30      mov   eax, dword [esp+0x08]
            0x00c0ce34      cmp   eax, 0x14                            ; 20
        ,=< 0x00c0ce37      jnbe  0xc0ce50
        |   0x00c0ce39      mov   ecx, dword [esp+0x04]
        |   0x00c0ce3d      test  ecx, ecx
       ,==< 0x00c0ce3f      js    0xc0ce50
       ||   0x00c0ce41      cmp   ecx, 0x01                            ; 1
      ,===< 0x00c0ce44      jle   0xc0ce53
      |||   0x00c0ce46      cmp   ecx, 0x02                            ; 2
     ,====< 0x00c0ce49      jnz   0xc0ce50
     ||||   0x00c0ce4b      cmp   eax, 0x01                            ; 1
    ,=====< 0x00c0ce4e      jz    0xc0ce57
   .-`-``-> 0x00c0ce50      xor   eax, eax
   :| |     0x00c0ce52      ret
   :| `---> 0x00c0ce53      test  eax, eax
   `======< 0x00c0ce55      jz    0xc0ce50
    `-----> 0x00c0ce57      mov   eax, 0x01
            0x00c0ce5c      ret
            0x00c0ce5d      int3
            0x00c0ce5e      int3
            0x00c0ce5f      int3
            0x00c0ce60      push  dword [esp+0x04]
            0x00c0ce64      call  0xc09420
            0x00c0ce69      add   esp, 0x04
            0x00c0ce6c      cmp   eax, 0xffffffff                      ; -1
            0x00c0ce6f      setnz al
            0x00c0ce72      ret
            0x00c0ce73      int3
            0x00c0ce74      int3
            0x00c0ce75      int3
            0x00c0ce76      int3
            0x00c0ce77      int3
            0x00c0ce78      int3
            0x00c0ce79      int3
            0x00c0ce7a      int3
            0x00c0ce7b      int3
            0x00c0ce7c      int3
            0x00c0ce7d      int3
            0x00c0ce7e      int3
            0x00c0ce7f      int3
            0x00c0ce80      push  dword [0x202731c]
            0x00c0ce86      add   ecx, 0x0c                            ; 0xc ; 12
            0x00c0ce89      call  0xbcdcd0
            0x00c0ce8e      ret
            0x00c0ce8f      int3
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
            0x00c0ceaf      invalid
            0x00c0ccf0      push  ebp
            0x00c0ccf1      mov   ebp, esp
            0x00c0ccf3      push  0xffffffff                           ; 255
            0x00c0ccf5      push  0x186f298
            0x00c0ccfa      mov   eax, dword fs:[0x0]
            0x00c0cd00      push  eax
            0x00c0cd01      sub   esp, 0x0c
            0x00c0cd04      push  esi
            0x00c0cd05      push  edi
            0x00c0cd06      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0cd0b      xor   eax, ebp
            0x00c0cd0d      push  eax
            0x00c0cd0e      lea   eax, dword [ebp-0x0c]
            0x00c0cd11      mov   dword fs:[0x0], eax
            0x00c0cd17      mov   edi, ecx
            0x00c0cd19      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c0cd1e      xor   edx, edx
            0x00c0cd20      xor   esi, esi
            0x00c0cd22      mov   eax, dword [eax+0xe0]
            0x00c0cd28      mov   dword [ebp-0x14], edx
            0x00c0cd2b      mov   dword [ebp-0x10], esi
            0x00c0cd2e      mov   ecx, dword [eax*4+0x20286d8]
            0x00c0cd35      mov   dword [ebp-0x18], ecx
            0x00c0cd38      test  ecx, ecx
        ,=< 0x00c0cd3a      jz    0xc0cd4f
        |   0x00c0cd3c      mov   eax, dword [ecx]
        |   0x00c0cd3e      lea   edx, dword [ebp-0x14]
        |   0x00c0cd41      push  esi
        |   0x00c0cd42      push  edx
        |   0x00c0cd43      call  dword [eax+0x3c]                     ; 60
        |   0x00c0cd46      mov   esi, dword [ebp-0x10]
        |   0x00c0cd49      mov   edx, dword [ebp-0x14]
        |   0x00c0cd4c      mov   ecx, dword [ebp-0x18]
        `-> 0x00c0cd4f      mov   dword [ebp-0x04], 0x00
            0x00c0cd56      test  ecx, ecx
        ,=< 0x00c0cd58      jz    0xc0cd6a
        |   0x00c0cd5a      mov   eax, dword [edi+0x08]
        |   0x00c0cd5d      movzx ecx, word [eax+0x20]
        |   0x00c0cd61      cmp   ecx, esi
       ,==< 0x00c0cd63      jnb   0xc0cd6a
       ||   0x00c0cd65      mov   ecx, dword [edx+ecx*4]
      ,===< 0x00c0cd68      jmp   0xc0cd6c
      |``-> 0x00c0cd6a      xor   ecx, ecx
      `---> 0x00c0cd6c      push  0x07                                 ; 7
            0x00c0cd6e      call  0xc182a0
            0x00c0cd73      mov   ecx, dword [ebp-0x0c]
            0x00c0cd76      mov   dword fs:[0x0], ecx
            0x00c0cd7d      pop   ecx
            0x00c0cd7e      pop   edi
            0x00c0cd7f      pop   esi
            0x00c0cd80      mov   esp, ebp
            0x00c0cd82      pop   ebp
            0x00c0cd83      ret
            0x00c0cd84      int3
            0x00c0cd85      int3
            0x00c0cd86      int3
            0x00c0cd87      int3
            0x00c0cd88      int3
            0x00c0cd89      int3
            0x00c0cd8a      int3
            0x00c0cd8b      int3
            0x00c0cd8c      int3
            0x00c0cd8d      int3
            0x00c0cd8e      int3
            0x00c0cd8f      int3
            0x00c0cd90      push  ebp
            0x00c0cd91      mov   ebp, esp
            0x00c0cd93      push  0xffffffff                           ; 255
            0x00c0cd95      push  0x185ea78
            0x00c0cd9a      mov   eax, dword fs:[0x0]
            0x00c0cda0      push  eax
            0x00c0cda1      sub   esp, 0x0c
            0x00c0cda4      push  ebx
            0x00c0cda5      push  esi
            0x00c0cda6      push  edi
            0x00c0cda7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0cdac      xor   eax, ebp
            0x00c0cdae      push  eax
            0x00c0cdaf      lea   eax, dword [ebp-0x0c]
            0x00c0cdb2      mov   dword fs:[0x0], eax
            0x00c0cdb8      mov   ebx, ecx
            0x00c0cdba      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c0cdbf      xor   edx, edx
            0x00c0cdc1      xor   edi, edi
            0x00c0cdc3      mov   eax, dword [eax+0xe0]
            0x00c0cdc9      mov   dword [ebp-0x14], edx
            0x00c0cdcc      mov   dword [ebp-0x10], edi
            0x00c0cdcf      mov   ecx, dword [eax*4+0x20286d8]
            0x00c0cdd6      mov   dword [ebp-0x18], ecx
            0x00c0cdd9      test  ecx, ecx
        ,=< 0x00c0cddb      jz    0xc0cdf0
        |   0x00c0cddd      mov   eax, dword [ecx]
        |   0x00c0cddf      lea   edx, dword [ebp-0x14]
        |   0x00c0cde2      push  edi
        |   0x00c0cde3      push  edx
        |   0x00c0cde4      call  dword [eax+0x3c]                     ; 60
        |   0x00c0cde7      mov   edi, dword [ebp-0x10]
        |   0x00c0cdea      mov   edx, dword [ebp-0x14]
        |   0x00c0cded      mov   ecx, dword [ebp-0x18]
