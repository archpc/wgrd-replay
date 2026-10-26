            0x00c06ba0      push  ebx
            0x00c06ba1      push  esi
            0x00c06ba2      mov   esi, dword [esp+0x0c]
            0x00c06ba6      mov   ebx, ecx
            0x00c06ba8      push  edi
            0x00c06ba9      push  dword [esp+0x14]
            0x00c06bad      push  esi
            0x00c06bae      call  0xb53df0
            0x00c06bb3      push  0x00
            0x00c06bb5      lea   eax, dword [ebx+0x08]
            0x00c06bb8      lea   edi, dword [esi+0x14]
            0x00c06bbb      push  eax
            0x00c06bbc      mov   ecx, edi
            0x00c06bbe      call  0xb074c0
            0x00c06bc3      xor   eax, eax
            0x00c06bc5      lea   ecx, dword [ebx+0x0c]
            0x00c06bc8      test  edi, edi
            0x00c06bca      cmovz esi, eax
            0x00c06bcd      push  dword [esi+0x0c]
            0x00c06bd0      push  esi
            0x00c06bd1      call  0xbd01e0
            0x00c06bd6      lea   eax, dword [edi-0x14]
            0x00c06bd9      neg   edi
            0x00c06bdb      push  0x04                                 ; 4
            0x00c06bdd      sbb   edi, edi
            0x00c06bdf      and   edi, eax
            0x00c06be1      lea   eax, dword [ebx+0x1c]
            0x00c06be4      push  eax
            0x00c06be5      mov   ecx, edi
            0x00c06be7      call  0xb5abf0
            0x00c06bec      push  0x04                                 ; 4
            0x00c06bee      lea   eax, dword [esp+0x18]
            0x00c06bf2      mov   dword [esp+0x18], 0x00
            0x00c06bfa      push  eax
            0x00c06bfb      mov   ecx, edi
            0x00c06bfd      call  0xb5abf0
            0x00c06c02      mov   eax, dword [esp+0x14]
            0x00c06c06      mov   ecx, edi
            0x00c06c08      mov   dword [ebx+0x20], eax
            0x00c06c0b      lea   eax, dword [ebx+0x24]
            0x00c06c0e      push  0x04                                 ; 4
            0x00c06c10      push  eax
            0x00c06c11      call  0xb5abf0
            0x00c06c16      pop   edi
            0x00c06c17      pop   esi
            0x00c06c18      pop   ebx
            0x00c06c19      ret   0x08
            0x00c06c1c      int3
            0x00c06c1d      int3
            0x00c06c1e      int3
            0x00c06c1f      int3
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
            0x00c06d40      xor   eax, eax
            0x00c06d42      test  esi, esi
            0x00c06d44      cmovz edi, eax
            0x00c06d47      mov   ecx, edi
            0x00c06d49      call  0xb5abf0
            0x00c06d4e      mov   eax, dword [esp+0x14]
            0x00c06d52      mov   ecx, esi
            0x00c06d54      mov   dword [ebx+0x30], eax
            0x00c06d57      lea   eax, dword [ebx+0x34]
            0x00c06d5a      push  eax
            0x00c06d5b      call  0xacc0d0
            0x00c06d60      lea   eax, dword [esi-0x14]
            0x00c06d63      neg   esi
            0x00c06d65      push  0x01                                 ; 1
            0x00c06d67      sbb   esi, esi
            0x00c06d69      and   esi, eax
            0x00c06d6b      lea   eax, dword [ebx+0x48]
            0x00c06d6e      push  eax
            0x00c06d6f      mov   ecx, esi
            0x00c06d71      call  0xb5abf0
            0x00c06d76      push  0x04                                 ; 4
            0x00c06d78      lea   eax, dword [esp+0x18]
            0x00c06d7c      mov   dword [esp+0x18], 0x00
            0x00c06d84      push  eax
            0x00c06d85      mov   ecx, esi
            0x00c06d87      call  0xb5abf0
            0x00c06d8c      mov   eax, dword [esp+0x14]
            0x00c06d90      pop   edi
            0x00c06d91      pop   esi
            0x00c06d92      mov   dword [ebx+0x4c], eax
            0x00c06d95      pop   ebx
            0x00c06d96      ret   0x08
            0x00c06d99      int3
            0x00c06d9a      int3
            0x00c06d9b      int3
            0x00c06d9c      int3
            0x00c06d9d      int3
            0x00c06d9e      int3
            0x00c06d9f      int3
            0x00c06da0      push  ebp
            0x00c06da1      mov   ebp, esp
            0x00c06da3      push  0xffffffff                           ; 255
            0x00c06da5      push  0x180a7d0
            0x00c06daa      mov   eax, dword fs:[0x0]
            0x00c06db0      push  eax
            0x00c06db1      push  ebx
            0x00c06db2      push  esi
            0x00c06db3      push  edi
            0x00c06db4      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c06db9      xor   eax, ebp
            0x00c06dbb      push  eax
            0x00c06dbc      lea   eax, dword [ebp-0x0c]
            0x00c06dbf      mov   dword fs:[0x0], eax
            0x00c06dc5      mov   ebx, ecx
            0x00c06dc7      push  dword [ebp+0x0c]
            0x00c06dca      mov   esi, dword [ebp+0x08]
            0x00c06dcd      push  esi
            0x00c06dce      call  0xb53e60
            0x00c06dd3      push  0x00
            0x00c06dd5      push  dword [ebx+0x08]
            0x00c06dd8      lea   edi, dword [esi+0x10]
            0x00c06ddb      mov   ecx, edi
            0x00c06ddd      call  0xa7ab60
            0x00c06de2      xor   eax, eax
            0x00c06de4      lea   ecx, dword [ebx+0x0c]
            0x00c06de7      test  edi, edi
            0x00c06de9      cmovz esi, eax
            0x00c06dec      push  dword [esi+0x0c]
            0x00c06def      push  esi
            0x00c06df0      call  0xbd0270
            0x00c06df5      mov   eax, dword [ebx+0x1c]
            0x00c06df8      lea   esi, dword [edi+0x08]
            0x00c06dfb      mov   dword [ebp+0x0c], eax
            0x00c06dfe      lea   edx, dword [ebp+0x0c]
            0x00c06e01      mov   eax, 0x18                            ; 24
            0x00c06e06      test  edi, edi
            0x00c06e08      push  0x04                                 ; 4
            0x00c06e0a      cmovz esi, eax
            0x00c06e0d      push  edx
            0x00c06e0e      mov   ecx, dword [esi]
            0x00c06e10      mov   eax, dword [ecx]
            0x00c06e12      call  dword [eax+0x1c]                     ; 28
            0x00c06e15      mov   ecx, dword [esi]
            0x00c06e17      lea   edx, dword [ebp+0x0c]
            0x00c06e1a      mov   eax, dword [ebx+0x20]
            0x00c06e1d      mov   dword [ebp+0x0c], eax
            0x00c06e20      push  0x04                                 ; 4
            0x00c06e22      mov   eax, dword [ecx]
            0x00c06e24      push  edx
            0x00c06e25      call  dword [eax+0x1c]                     ; 28
            0x00c06e28      mov   ecx, dword [esi]
            0x00c06e2a      lea   edx, dword [ebp+0x08]
            0x00c06e2d      mov   eax, dword [ebx+0x24]
            0x00c06e30      mov   dword [ebp+0x08], eax
            0x00c06e33      push  0x04                                 ; 4
            0x00c06e35      mov   eax, dword [ecx]
            0x00c06e37      push  edx
            0x00c06e38      call  dword [eax+0x1c]                     ; 28
            0x00c06e3b      mov   ecx, dword [ebp-0x0c]
            0x00c06e3e      mov   dword fs:[0x0], ecx
            0x00c06e45      pop   ecx
            0x00c06e46      pop   edi
            0x00c06e47      pop   esi
            0x00c06e48      pop   ebx
            0x00c06e49      mov   esp, ebp
            0x00c06e4b      pop   ebp
            0x00c06e4c      ret   0x08
            0x00c06e4f      int3
            0x00c06e50      push  ebp
            0x00c06e51      mov   ebp, esp
            0x00c06e53      push  0xffffffff                           ; 255
            0x00c06e55      push  0x180a7d0
            0x00c06e5a      mov   eax, dword fs:[0x0]
            0x00c06e60      push  eax
            0x00c06e61      push  ebx
            0x00c06e62      push  esi
            0x00c06e63      push  edi
            0x00c06e64      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c06e69      xor   eax, ebp
            0x00c06e6b      push  eax
            0x00c06e6c      lea   eax, dword [ebp-0x0c]
            0x00c06e6f      mov   dword fs:[0x0], eax
            0x00c06e75      mov   ebx, ecx
            0x00c06e77      push  dword [ebp+0x0c]
            0x00c06e7a      mov   esi, dword [ebp+0x08]
            0x00c06e7d      push  esi
            0x00c06e7e      call  0xb53e60
            0x00c06e83      push  0x00
            0x00c06e85      push  dword [ebx+0x08]
            0x00c06e88      lea   edi, dword [esi+0x10]
            0x00c06e8b      mov   ecx, edi
            0x00c06e8d      call  0xa7ab60
            0x00c06e92      xor   eax, eax
            0x00c06e94      lea   ecx, dword [ebx+0x0c]
            0x00c06e97      test  edi, edi
            0x00c06e99      cmovz esi, eax
            0x00c06e9c      push  dword [esi+0x0c]
            0x00c06e9f      push  esi
            0x00c06ea0      call  0xbd0270
            0x00c06ea5      lea   eax, dword [ebx+0x1c]
            0x00c06ea8      mov   ecx, edi
            0x00c06eaa      push  eax
            0x00c06eab      call  0xc06340
            0x00c06eb0      push  0x00
            0x00c06eb2      push  dword [ebx+0x68]
            0x00c06eb5      mov   ecx, edi
            0x00c06eb7      call  0xa7ab60
            0x00c06ebc      mov   eax, dword [ebx+0x6c]
            0x00c06ebf      lea   esi, dword [edi+0x08]
            0x00c06ec2      mov   dword [ebp+0x0c], eax
            0x00c06ec5      lea   edx, dword [ebp+0x0c]
            0x00c06ec8      mov   eax, 0x18                            ; 24
            0x00c06ecd      test  edi, edi
            0x00c06ecf      push  0x04                                 ; 4
            0x00c06ed1      cmovz esi, eax
            0x00c06ed4      push  edx
            0x00c06ed5      mov   ecx, dword [esi]
            0x00c06ed7      mov   eax, dword [ecx]
            0x00c06ed9      call  dword [eax+0x1c]                     ; 28
            0x00c06edc      mov   ecx, dword [esi]
            0x00c06ede      lea   edx, dword [ebp+0x0c]
            0x00c06ee1      mov   eax, dword [ebx+0x70]
            0x00c06ee4      mov   dword [ebp+0x0c], eax
            0x00c06ee7      push  0x04                                 ; 4
            0x00c06ee9      mov   eax, dword [ecx]
            0x00c06eeb      push  edx
            0x00c06eec      call  dword [eax+0x1c]                     ; 28
            0x00c06eef      lea   eax, dword [ebx+0x74]
            0x00c06ef2      mov   ecx, edi
            0x00c06ef4      push  eax
            0x00c06ef5      call  0xc06150
            0x00c06efa      mov   ecx, dword [esi]
            0x00c06efc      lea   edx, dword [ebp+0x0c]
            0x00c06eff      mov   eax, dword [ebx+0x90]
            0x00c06f05      mov   dword [ebp+0x0c], eax
            0x00c06f08      push  0x04                                 ; 4
            0x00c06f0a      mov   eax, dword [ecx]
            0x00c06f0c      push  edx
            0x00c06f0d      call  dword [eax+0x1c]                     ; 28
            0x00c06f10      mov   ecx, dword [esi]
            0x00c06f12      lea   edx, dword [ebp+0x0c]
            0x00c06f15      movzx eax, byte [ebx+0x94]
            0x00c06f1c      mov   byte [ebp+0x0c], al
            0x00c06f1f      push  0x01                                 ; 1
            0x00c06f21      mov   eax, dword [ecx]
            0x00c06f23      push  edx
            0x00c06f24      call  dword [eax+0x1c]                     ; 28
            0x00c06f27      mov   ecx, dword [esi]
            0x00c06f29      lea   edx, dword [ebp+0x0c]
            0x00c06f2c      movzx eax, byte [ebx+0x95]
            0x00c06f33      mov   byte [ebp+0x0c], al
            0x00c06f36      push  0x01                                 ; 1
            0x00c06f38      mov   eax, dword [ecx]
            0x00c06f3a      push  edx
            0x00c06f3b      call  dword [eax+0x1c]                     ; 28
            0x00c06f3e      lea   eax, dword [ebx+0x98]
            0x00c06f44      mov   ecx, edi
            0x00c06f46      push  eax
            0x00c06f47      call  0xa602b0
            0x00c06f4c      mov   ecx, dword [esi]
            0x00c06f4e      movzx eax, byte [ebx+0x96]
            0x00c06f55      mov   byte [ebp+0x08], al
            0x00c06f58      push  0x01                                 ; 1
            0x00c06f5a      mov   eax, dword [ecx]
            0x00c06f5c      lea   edx, dword [ebp+0x08]
            0x00c06f5f      push  edx
            0x00c06f60      call  dword [eax+0x1c]                     ; 28
            0x00c06f63      mov   ecx, dword [ebp-0x0c]
            0x00c06f66      mov   dword fs:[0x0], ecx
            0x00c06f6d      pop   ecx
            0x00c06f6e      pop   edi
            0x00c06f6f      pop   esi
