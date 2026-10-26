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
            0x004f724c      invalid
            0x004f724d      invalid
            0x004f724e      sbb   al, 0xfa
            0x00b5abd0      push  dword [esp+0x08]
            0x00b5abd4      mov   ecx, dword [0x203b890]               ; [0x203b890:4]=0
            0x00b5abda      push  dword [esp+0x08]
            0x00b5abde      call  0xb5a630
            0x00b5abe3      ret
            0x00b5abe4      int3
            0x00b5abe5      int3
            0x00b5abe6      int3
            0x00b5abe7      int3
            0x00b5abe8      int3
            0x00b5abe9      int3
            0x00b5abea      int3
            0x00b5abeb      int3
            0x00b5abec      int3
            0x00b5abed      int3
            0x00b5abee      int3
            0x00b5abef      int3
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
      |||   0x00b5ad1f      mov   dword [ebp-0x04], 0x03
      |||   0x00b5ad26      push  str.Trying_to_read                   ; 0x19a3244 ; "Trying to read "
      |||   0x00b5ad2b      push  eax
      |||   0x00b5ad2c      call  0x4d81d0
      |||   0x00b5ad31      add   esp, 0x08
      |||   0x00b5ad34      mov   ecx, eax
      |||   0x00b5ad36      push  str.in_a_chunk_but_there_is_not_enough_space_available ; 0x19a3210 ; " in a chunk but there is not enough space available"
      |||   0x00b5ad3b      push  edi
      |||   0x00b5ad3c      call  dword [sym.imp.MSVCP140.dll_public:_class_std::basic_ostream_char__struct_std::char_traits_char_______thiscall_std::basic_ostream_char__struct_std::char_traits_char__::operator___unsigned_int] ; 0x1914428 ; "~\x9c\x96\U00000001>\x9c\x96\U00000001\xfe\x9b\x96\U00000001\xa6\x9b\x96\U00000001V\x9b\x96\U00000001\U00000018\x9b\x96\U0000000"
      |||   0x00b5ad42      push  eax
      |||   0x00b5ad43      call  0x4d81d0
      |||   0x00b5ad48      add   esp, 0x08
      |||   0x00b5ad4b      mov   ecx, dword [ebp-0x64]
      |||   0x00b5ad4e      mov   byte [ebp-0x04], 0x04
      |||   0x00b5ad52      mov   dword [ebp+0x1c], 0x00
      |||   0x00b5ad59      mov   dword [ebp+0x20], 0x0f               ; 0xf ; 15
      |||   0x00b5ad60      mov   byte [ebp+0x0c], 0x00
      |||   0x00b5ad64      mov   dword [ebp], 0x09
      |||   0x00b5ad6b      test  cl, 0x02                             ; 2
     ,====< 0x00b5ad6e      jnz   0xb5ad8c
     ||||   0x00b5ad70      mov   eax, dword [ebp-0x80]
     ||||   0x00b5ad73      mov   edx, dword [eax]
     ||||   0x00b5ad75      test  edx, edx
    ,=====< 0x00b5ad77      jz    0xb5ad8c
    |||||   0x00b5ad79      mov   eax, dword [ebp-0x90]
    |||||   0x00b5ad7f      cmp   edx, dword [ebp-0x68]
    |||||   0x00b5ad82      cmovb edx, dword [ebp-0x68]
    |||||   0x00b5ad86      mov   ecx, dword [eax]
    |||||   0x00b5ad88      sub   edx, ecx
   ,======< 0x00b5ad8a      jmp   0xb5adac
   |``----> 0x00b5ad8c      test  cl, 0x04                             ; 4
   | ,====< 0x00b5ad8f      jnz   0xb5adb6
   | ||||   0x00b5ad91      mov   eax, dword [ebp-0x84]
   | ||||   0x00b5ad97      mov   edx, dword [eax]
   | ||||   0x00b5ad99      test  edx, edx
   |,=====< 0x00b5ad9b      jz    0xb5adb6
   ||||||   0x00b5ad9d      mov   eax, dword [ebp-0x94]
   ||||||   0x00b5ada3      mov   ecx, dword [eax]
   ||||||   0x00b5ada5      sub   edx, ecx
   ||||||   0x00b5ada7      mov   eax, dword [ebp-0x74]
   ||||||   0x00b5adaa      add   edx, dword [eax]
   `------> 0x00b5adac      push  edx
    |||||   0x00b5adad      push  ecx
    |||||   0x00b5adae      lea   ecx, dword [ebp+0x08]
    |||||   0x00b5adb1      call  0x5202f0
    ``----> 0x00b5adb6      cmp   dword [ebp+0x20], 0x10
      |||   0x00b5adba      lea   eax, dword [ebp+0x0c]
      |||   0x00b5adbd      mov   dword [ebp-0x04], 0x05
      |||   0x00b5adc4      cmovnb eax, dword [ebp+0x0c]
      |||   0x00b5adc8      push  eax
      |||   0x00b5adc9      push  0x1928c94
      |||   0x00b5adce      push  0x1cf                                ; 463
      |||   0x00b5add3      push  str.C:_Data_GitlabBuild_9qFhLbMy_0_eugen_Slayer_Code_Eugen_CPP_EugIA_Common_SavingSystem.cpp ; 0x19a3258 ; "C:\Data\GitlabBuild\9qFhLbMy\0\eugen\Slayer\Code\Eugen\CPP\EugIA_Common\SavingSystem.cpp"
      |||   0x00b5add8      call  0x5027d0
      |||   0x00b5addd      add   esp, 0x10
      |||   0x00b5ade0      lea   ecx, dword [ebp+0x08]
      |||   0x00b5ade3      call  0x4fa250
      |||   0x00b5ade8      mov   al, byte [0x1]                       ; [0x1:1]=255 ; 1
      |||   0x00b5aded      lea   ecx, dword [ebp-0xa4]
      |||   0x00b5adf3      mov   byte [0x203b8a4], al
      |||   0x00b5adf8      call  0x4fe920
      ```-> 0x00b5adfd      mov   ecx, dword [ebp-0x0c]
            0x00b5ae00      mov   dword fs:[0x0], ecx
            0x00b5ae07      pop   ecx
            0x00b5ae08      pop   edi
            0x00b5ae09      pop   esi
            0x00b5ae0a      mov   ecx, dword [ebp+0x24]
            0x00b5ae0d      xor   ecx, ebp
            0x00b5ae0f      call  0x18075f6
            0x00b5ae14      lea   esp, dword [ebp+0x28]
            0x00b5ae17      pop   ebp
            0x00b5ae18      ret   0x08
            0x00b5ae1b      int3
            0x00b5ae1c      int3
            0x00b5ae1d      int3
            0x00b5ae1e      int3
            0x00b5ae1f      int3
            0x00b5ae20      push  dword [esp+0x08]
            0x00b5ae24      lea   eax, dword [ecx+0x14]
            0x00b5ae27      push  dword [esp+0x08]
            0x00b5ae2b      push  eax
            0x00b5ae2c      call  0x52c670
            0x00b5ae31      add   esp, 0x0c
            0x00b5ae34      ret   0x08
            0x00b5ae37      int3
            0x00b5ae38      int3
            0x00b5ae39      int3
            0x00b5ae3a      int3
            0x00b5ae3b      int3
            0x00b5ae3c      int3
            0x00b5ae3d      int3
            0x00b5ae3e      int3
            0x00b5ae3f      int3
            0x00b5ae40      movss xmm0, dword [ecx+0x14]
            0x00b5ae45      movss xmm1, dword [esp+0x04]
            0x00b5ae4b      comiss xmm0, xmm1
        ,=< 0x00b5ae4e      jnbe  0xb5aea6
        |   0x00b5ae50      movss xmm0, dword [ecx+0x18]
        |   0x00b5ae55      comiss xmm0, xmm1
       ,==< 0x00b5ae58      jnbe  0xb5aea6
       ||   0x00b5ae5a      movss xmm0, dword [ecx+0x20]
       ||   0x00b5ae5f      comiss xmm0, xmm1
      ,===< 0x00b5ae62      jnbe  0xb5aea6
      |||   0x00b5ae64      movss xmm0, dword [ecx+0x24]
      |||   0x00b5ae69      comiss xmm0, xmm1
     ,====< 0x00b5ae6c      jnbe  0xb5aea6
     ||||   0x00b5ae6e      mov   eax, 0x03
     ||||   0x00b5ae73      add   ecx, 0x7c                            ; 124
    .-----> 0x00b5ae76      cmp   eax, 0x02                            ; 2
   ,======< 0x00b5ae79      jz    0xb5ae98
   |:||||   0x00b5ae7b      cmp   eax, 0x09                            ; 9
  ,=======< 0x00b5ae7e      jz    0xb5ae98
  ||:||||   0x00b5ae80      cmp   eax, 0x03                            ; 3
  ========< 0x00b5ae83      jz    0xb5ae98
  ||:||||   0x00b5ae85      cmp   eax, 0x05                            ; 5
  ========< 0x00b5ae88      jz    0xb5ae98
  ||:||||   0x00b5ae8a      cmp   eax, 0x0a                            ; 0xa ; 10
  ========< 0x00b5ae8d      jnb   0xb5ae98
  ||:||||   0x00b5ae8f      movss xmm0, dword [ecx]
  ||:||||   0x00b5ae93      comiss xmm0, xmm1
  ========< 0x00b5ae96      jnbe  0xb5aea6
  ``------> 0x00b5ae98      inc   eax
    :||||   0x00b5ae99      add   ecx, 0x04
    :||||   0x00b5ae9c      cmp   eax, 0x09                            ; 9
    `=====< 0x00b5ae9f      jnz   0xb5ae76
     ||||   0x00b5aea1      xor   al, al
     ||||   0x00b5aea3      ret   0x04
  ---````-> 0x00b5aea6      mov   al, 0x01
            0x00b5aea8      ret   0x04
            0x00b5aeab      int3
            0x00b5aeac      int3
            0x00b5aead      int3
            0x00b5aeae      int3
            0x00b5aeaf      int3
            0x00b5aeb0      push  ebp
            0x00b5aeb1      mov   ebp, esp
            0x00b5aeb3      push  0xffffffff                           ; 255
            0x00b5aeb5      push  0x186c3af
            0x00b5aeba      mov   eax, dword fs:[0x0]
            0x00b5aec0      push  eax
            0x00b5aec1      push  ecx
            0x00b5aec2      push  esi
            0x00b5aec3      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b5aec8      xor   eax, ebp
            0x00b5aeca      push  eax
            0x00b5aecb      lea   eax, dword [ebp-0x0c]
            0x00b5aece      mov   dword fs:[0x0], eax
            0x00b5aed4      mov   ecx, dword [0x203b720]               ; [0x203b720:4]=0
            0x00b5aeda      push  0x10                                 ; 16
            0x00b5aedc      call  0x556f00
            0x00b5aee1      mov   esi, eax
            0x00b5aee3      mov   dword [ebp-0x10], esi
            0x00b5aee6      mov   dword [ebp-0x04], 0x00
            0x00b5aeed      test  esi, esi
        ,=< 0x00b5aeef      jz    0xb5af17
        |   0x00b5aef1      mov   ecx, esi
        |   0x00b5aef3      call  0x54ec00
        |   0x00b5aef8      mov   dword [esi], 0x19a3174               ; [0x19a3174:4]=0xb590c0
        |   0x00b5aefe      mov   eax, esi
        |   0x00b5af00      mov   dword [esi+0x0c], 0x00
        |   0x00b5af07      mov   ecx, dword [ebp-0x0c]
        |   0x00b5af0a      mov   dword fs:[0x0], ecx
        |   0x00b5af11      pop   ecx
        |   0x00b5af12      pop   esi
        |   0x00b5af13      mov   esp, ebp
        |   0x00b5af15      pop   ebp
        |   0x00b5af16      ret
        `-> 0x00b5af17      xor   eax, eax
            0x00b5af19      mov   ecx, dword [ebp-0x0c]
            0x00b5af1c      mov   dword fs:[0x0], ecx
            0x00b5af23      pop   ecx
            0x00b5af24      pop   esi
            0x00b5af25      mov   esp, ebp
            0x00b5af27      pop   ebp
            0x00b5af28      ret
            0x00b5af29      int3
            0x00b5af2a      int3
            0x00b5af2b      int3
            0x00b5af2c      int3
            0x00b5af2d      int3
            0x00b5af2e      int3
            0x00b5af2f      int3
            0x00b5af30      push  ebp
            0x00b5af31      mov   ebp, esp
            0x00b5af33      push  0xffffffff                           ; 255
            0x00b5af35      push  0x186c3e2
            0x00b5af3a      mov   eax, dword fs:[0x0]
            0x00b5af40      push  eax
            0x00b5af41      push  ecx
            0x00b5af42      push  esi
            0x00b5af43      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b5af48      xor   eax, ebp
            0x00b5af4a      push  eax
            0x00b5af4b      lea   eax, dword [ebp-0x0c]
            0x00b5af4e      mov   dword fs:[0x0], eax
            0x00b5af54      mov   ecx, dword [0x203b728]               ; [0x203b728:4]=0
            0x00b5af5a      push  0x8c                                 ; 140
            0x00b5af5f      call  0x556f00
            0x00b5af64      mov   esi, eax
            0x00b5af66      mov   dword [ebp-0x10], esi
            0x00b5af69      mov   dword [ebp-0x04], 0x00
            0x00b5af70      test  esi, esi
        ,=< 0x00b5af72      jz    0xb5b05b
        |   0x00b5af78      mov   ecx, esi
        |   0x00b5af7a      call  0xb02fc0
        |   0x00b5af7f      mov   dword [esi], 0x19a3310               ; [0x19a3310:4]=0xb593b0
        |   0x00b5af85      mov   dword [esi+0x18], 0x00
        |   0x00b5af8c      mov   dword [esi+0x1c], 0x00
        |   0x00b5af93      mov   dword [esi+0x20], 0x00
        |   0x00b5af9a      mov   dword [esi+0x24], 0x00
        |   0x00b5afa1      mov   dword [esi+0x28], 0x00
        |   0x00b5afa8      mov   dword [esi+0x2c], 0x00
        |   0x00b5afaf      mov   dword [esi+0x30], 0x00
        |   0x00b5afb6      mov   dword [esi+0x34], 0x00
        |   0x00b5afbd      mov   dword [esi+0x38], 0x00
        |   0x00b5afc4      mov   dword [esi+0x3c], 0x00
        |   0x00b5afcb      invalid
        |   0x00b5afcc      inc   esi
        |   0x00b5afcd      inc   eax
        |   0x00b5afce      add   byte [eax], al
            0x00c0b40b      lea   ecx, dword [ebp-0x124]
            0x00c0b411      call  0x4f6c50
            0x00c0b416      lea   ecx, dword [ebp-0x48]
            0x00c0b419      mov   dword [ebp-0x04], 0x00
            0x00c0b420      call  0x598730
            0x00c0b425      push  0xffffffff                           ; 255
            0x00c0b427      lea   eax, dword [ebp-0x38]
            0x00c0b42a      mov   byte [ebp-0x04], 0x01
            0x00c0b42e      push  eax
            0x00c0b42f      lea   ecx, dword [ebp-0x48]
            0x00c0b432      call  0xaf5040
            0x00c0b437      push  0xffffffff                           ; 255
            0x00c0b439      lea   eax, dword [ebp-0x28]
            0x00c0b43c      push  eax
            0x00c0b43d      lea   ecx, dword [ebp-0x48]
            0x00c0b440      call  0xaf5150
            0x00c0b445      lea   eax, dword [edi+0x18]
            0x00c0b448      push  0xffffffff                           ; 255
            0x00c0b44a      push  eax
            0x00c0b44b      lea   ecx, dword [ebp-0x48]
            0x00c0b44e      call  0xaf51e0
            0x00c0b453      lea   eax, dword [edi+0x6c]
            0x00c0b456      push  0xffffffff                           ; 255
            0x00c0b458      push  eax
            0x00c0b459      lea   ecx, dword [ebp-0x48]
            0x00c0b45c      call  0xaf5260
            0x00c0b461      cmp   esi, 0x04                            ; 4
        ,=< 0x00c0b464      jnb   0xc0b46e
        |   0x00c0b466      lea   eax, dword [edi+0x74]
        |   0x00c0b469      lea   eax, dword [eax+esi*4]
       ,==< 0x00c0b46c      jmp   0xc0b47a
       |`-> 0x00c0b46e      mov   eax, dword [edi+0x84]
       |    0x00c0b474      lea   eax, dword [eax+esi*4]
       |    0x00c0b477      add   eax, 0xfffffff0                      ; 4294967280
       `--> 0x00c0b47a      push  0xffffffff                           ; 255
            0x00c0b47c      push  eax
            0x00c0b47d      lea   ecx, dword [ebp-0x48]
            0x00c0b480      call  0xc07290
            0x00c0b485      push  0xffffffff                           ; 255
            0x00c0b487      lea   eax, dword [ebp-0x14]
            0x00c0b48a      mov   dword [ebp-0x14], 0x00
            0x00c0b491      push  eax
            0x00c0b492      lea   ecx, dword [ebp-0x48]
            0x00c0b495      call  0xaf53e0
            0x00c0b49a      mov   eax, dword [edi+0x08]
            0x00c0b49d      lea   ecx, dword [ebp-0x48]
            0x00c0b4a0      push  0xffffffff                           ; 255
            0x00c0b4a2      add   eax, 0x20                            ; 32
            0x00c0b4a5      push  eax
            0x00c0b4a6      call  0xaf50d0
            0x00c0b4ab      push  0xffffffff                           ; 255
            0x00c0b4ad      push  dword [edi+0x10]
            0x00c0b4b0      lea   ecx, dword [ebp-0x48]
            0x00c0b4b3      call  0xc07310
            0x00c0b4b8      mov   edx, dword [ebp-0x3c]
            0x00c0b4bb      mov   eax, dword [edi+0x14]
            0x00c0b4be      imul  ecx, edx, 0xb4
            0x00c0b4c4      mov   dword [ebp-0x14], eax
            0x00c0b4c7      mov   eax, dword [ebp-0x40]
            0x00c0b4ca      mov   dword [ebp-0x12c], edx
            0x00c0b4d0      add   ecx, eax
            0x00c0b4d2      cmp   eax, ecx
        ,=< 0x00c0b4d4      jz    0xc0b4ee
       .--> 0x00c0b4d6      cmp   dword [eax], 0x6a                    ; 'j'
      ,===< 0x00c0b4d9      jnz   0xc0b4e1
      |:|   0x00c0b4db      cmp   dword [eax+0x04], 0xffffffff
     ,====< 0x00c0b4df      jz    0xc0b4ea
     |`---> 0x00c0b4e1      add   eax, 0xb4                            ; 180
     | :|   0x00c0b4e6      cmp   eax, ecx
     | `==< 0x00c0b4e8      jnz   0xc0b4d6
     `----> 0x00c0b4ea      cmp   eax, ecx
       ,==< 0x00c0b4ec      jnz   0xc0b525
       |`-> 0x00c0b4ee      cmp   edx, dword [ebp-0x48]
       |,=< 0x00c0b4f1      jnz   0xc0b501
       ||   0x00c0b4f3      lea   ecx, dword [ebp-0x48]
       ||   0x00c0b4f6      call  0x9d6ad0
       ||   0x00c0b4fb      mov   edx, dword [ebp-0x12c]
       |`-> 0x00c0b501      imul  ecx, edx, 0xb4
       |    0x00c0b507      lea   eax, dword [edx+0x01]
       |    0x00c0b50a      mov   edx, dword [ebp-0x14]
       |    0x00c0b50d      mov   dword [ebp-0x3c], eax
       |    0x00c0b510      add   ecx, dword [ebp-0x40]
       |    0x00c0b513      mov   dword [ecx], 0x6a                    ; 'j'
       |                                                               ; [0x6a:4]=-1 ; 106
       |    0x00c0b519      mov   dword [ecx+0x04], 0xffffffff         ; [0xffffffff:4]=-1 ; -1
       |    0x00c0b520      mov   dword [ecx+0x08], edx
       |,=< 0x00c0b523      jmp   0xc0b52b
       `--> 0x00c0b525      mov   edx, dword [ebp-0x14]
        |   0x00c0b528      mov   dword [eax+0x08], edx
        `-> 0x00c0b52b      lea   ecx, dword [ebp-0x100]
            0x00c0b531      call  0xaf6620
            0x00c0b536      movss xmm0, dword [ebp-0x38]
            0x00c0b53b      cmp   dword [edi+0x10], 0x00
            0x00c0b53f      mov   eax, dword [edi+0x08]
            0x00c0b542      movss dword [ebp-0xe8], xmm0
            0x00c0b54a      setz  byte [ebp-0x14]
            0x00c0b54e      movss xmm0, dword [ebp-0x34]
            0x00c0b553      push  0x01                                 ; 1
            0x00c0b555      push  dword [ebp-0x14]
            0x00c0b558      movss dword [ebp-0xe4], xmm0
            0x00c0b560      movss xmm0, dword [ebp-0x30]
            0x00c0b565      mov   dword [ebp-0xec], eax
            0x00c0b56b      mov   al, byte [ebp-0x101]
            0x00c0b571      movss dword [ebp-0xe0], xmm0
            0x00c0b579      movss xmm0, dword [ebp-0x28]
            0x00c0b57e      push  0x01                                 ; 1
            0x00c0b580      push  dword [edi+0x0c]
            0x00c0b583      mov   byte [ebp-0xcc], al
            0x00c0b589      lea   eax, dword [ebp-0x48]
            0x00c0b58c      movss dword [ebp-0xdc], xmm0
            0x00c0b594      movss xmm0, dword [ebp-0x24]
            0x00c0b599      push  eax
            0x00c0b59a      movss dword [ebp-0xd8], xmm0
            0x00c0b5a2      lea   eax, dword [ebp-0x100]
            0x00c0b5a8      movss xmm0, dword [ebp-0x20]
            0x00c0b5ad      push  eax
            0x00c0b5ae      mov   byte [ebp-0x04], 0x02
            0x00c0b5b2      movss dword [ebp-0xd4], xmm0
            0x00c0b5ba      mov   dword [ebp-0xd0], 0x09
            0x00c0b5c4      call  0xaf9a30
            0x00c0b5c9      add   eax, 0x20                            ; 32
            0x00c0b5cc      push  eax
            0x00c0b5cd      call  0xb9d8f0
            0x00c0b5d2      add   esp, 0x1c
            0x00c0b5d5      cmp   dword [edi+0x10], 0x00
            0x00c0b5d9      mov   eax, dword [eax]
            0x00c0b5db      mov   dword [ebp-0x124], eax
        ,=< 0x00c0b5e1      jnz   0xc0b5f9
        |   0x00c0b5e3      lea   ecx, dword [ebp-0x124]
        |   0x00c0b5e9      call  0xb01530
        |   0x00c0b5ee      mov   ecx, dword [ebp-0x130]
        |   0x00c0b5f4      mov   eax, dword [eax+0x20]
        |   0x00c0b5f7      mov   dword [ecx], eax
        `-> 0x00c0b5f9      lea   ecx, dword [ebp-0x60]
            0x00c0b5fc      call  0x4dc500
            0x00c0b601      lea   ecx, dword [ebp-0x9c]
            0x00c0b607      call  0x975700
            0x00c0b60c      cmp   dword [ebp-0xb0], 0x00
            0x00c0b613      mov   byte [ebp-0x04], 0x03
            0x00c0b617      mov   dword [ebp-0xa4], 0x00
        ,=< 0x00c0b621      jz    0xc0b63d
        |   0x00c0b623      push  dword [ebp-0xa8]
        |   0x00c0b629      push  0x00
        |   0x00c0b62b      call  0x5291c0
        |   0x00c0b630      add   esp, 0x08
        |   0x00c0b633      mov   dword [ebp-0xb0], 0x00
        `-> 0x00c0b63d      lea   ecx, dword [ebp-0xb8]
            0x00c0b643      call  0x4dc500
            0x00c0b648      lea   ecx, dword [ebp-0x40]
            0x00c0b64b      mov   byte [ebp-0x04], 0x04
            0x00c0b64f      call  0x9d6700
            0x00c0b654      cmp   dword [ebp-0x48], 0x00
        ,=< 0x00c0b658      jz    0xc0b667
        |   0x00c0b65a      push  dword [ebp-0x40]
        |   0x00c0b65d      push  0x00
        |   0x00c0b65f      call  0x5291c0
        |   0x00c0b664      add   esp, 0x08
        `-> 0x00c0b667      lea   ecx, dword [ebp-0x120]
            0x00c0b66d      mov   byte [ebp-0x04], 0x00
            0x00c0b671      call  0x4f6c50
            0x00c0b676      cmp   dword [edi+0x10], 0x00
            0x00c0b67a      mov   byte [ebp-0x04], 0x05
        ,=< 0x00c0b67e      jz    0xc0b8d1
        |   0x00c0b684      lea   ecx, dword [ebp-0x118]
        |   0x00c0b68a      call  0x598730
        |   0x00c0b68f      push  0xffffffff                           ; 255
        |   0x00c0b691      lea   eax, dword [ebp-0x38]
        |   0x00c0b694      mov   byte [ebp-0x04], 0x06
        |   0x00c0b698      push  eax
        |   0x00c0b699      lea   ecx, dword [ebp-0x118]
        |   0x00c0b69f      call  0xaf5040
        |   0x00c0b6a4      push  0xffffffff                           ; 255
        |   0x00c0b6a6      lea   eax, dword [ebp-0x28]
        |   0x00c0b6a9      push  eax
        |   0x00c0b6aa      lea   ecx, dword [ebp-0x118]
        |   0x00c0b6b0      call  0xaf5150
        |   0x00c0b6b5      push  0xffffffff                           ; 255
        |   0x00c0b6b7      lea   eax, dword [edi+0x18]
        |   0x00c0b6ba      push  eax
        |   0x00c0b6bb      lea   ecx, dword [ebp-0x118]
        |   0x00c0b6c1      call  0xaf51e0
        |   0x00c0b6c6      push  0xffffffff                           ; 255
        |   0x00c0b6c8      lea   eax, dword [edi+0x6c]
        |   0x00c0b6cb      push  eax
        |   0x00c0b6cc      lea   ecx, dword [ebp-0x118]
        |   0x00c0b6d2      call  0xaf5260
        |   0x00c0b6d7      cmp   esi, 0x04                            ; 4
       ,==< 0x00c0b6da      jnb   0xc0b6e4
       ||   0x00c0b6dc      lea   eax, dword [edi+0x74]
       ||   0x00c0b6df      lea   eax, dword [eax+esi*4]
      ,===< 0x00c0b6e2      jmp   0xc0b6f0
      |`--> 0x00c0b6e4      mov   eax, dword [edi+0x84]
      | |   0x00c0b6ea      lea   eax, dword [eax+esi*4]
      | |   0x00c0b6ed      add   eax, 0xfffffff0                      ; 4294967280
      `---> 0x00c0b6f0      push  0xffffffff                           ; 255
        |   0x00c0b6f2      push  eax
        |   0x00c0b6f3      lea   ecx, dword [ebp-0x118]
        |   0x00c0b6f9      call  0xc07290
        |   0x00c0b6fe      push  0xffffffff                           ; 255
        |   0x00c0b700      lea   eax, dword [ebp-0x14]
        |   0x00c0b703      mov   dword [ebp-0x14], 0x00
        |   0x00c0b70a      push  eax
        |   0x00c0b70b      lea   ecx, dword [ebp-0x118]
        |   0x00c0b711      call  0xaf53e0
        |   0x00c0b716      mov   eax, dword [edi+0x08]
        |   0x00c0b719      lea   ecx, dword [ebp-0x118]
        |   0x00c0b71f      push  0xffffffff                           ; 255
        |   0x00c0b721      add   eax, 0x20                            ; 32
        |   0x00c0b724      push  eax
        |   0x00c0b725      call  0xaf50d0
        |   0x00c0b72a      push  0xffffffff                           ; 255
        |   0x00c0b72c      push  dword [edi+0x0c]
        |   0x00c0b72f      lea   ecx, dword [ebp-0x118]
        |   0x00c0b735      call  0xc07390
        |   0x00c0b73a      push  0xffffffff                           ; 255
        |   0x00c0b73c      push  dword [edi+0x14]
        |   0x00c0b73f      lea   ecx, dword [ebp-0x118]
        |   0x00c0b745      call  0xc07310
        |   0x00c0b74a      lea   ecx, dword [ebp-0x100]
        |   0x00c0b750      call  0xaf6620
        |   0x00c0b755      movss xmm0, dword [ebp-0x38]
        |   0x00c0b75a      cmp   dword [edi+0x14], 0x00
        |   0x00c0b75e      mov   eax, dword [edi+0x08]
        |   0x00c0b761      movss dword [ebp-0xe8], xmm0
        |   0x00c0b769      setz  byte [ebp-0x14]
        |   0x00c0b76d      movss xmm0, dword [ebp-0x34]
        |   0x00c0b772      push  0x01                                 ; 1
        |   0x00c0b774      push  dword [ebp-0x14]
        |   0x00c0b777      movss dword [ebp-0xe4], xmm0
        |   0x00c0b77f      movss xmm0, dword [ebp-0x30]
        |   0x00c0b784      mov   dword [ebp-0xec], eax
        |   0x00c0b78a      mov   al, byte [ebp-0x101]
        |   0x00c0b790      movss dword [ebp-0xe0], xmm0
        |   0x00c0b798      movss xmm0, dword [ebp-0x28]
        |   0x00c0b79d      push  0x01                                 ; 1
        |   0x00c0b79f      push  dword [edi+0x10]
        |   0x00c0b7a2      mov   byte [ebp-0xcc], al
        |   0x00c0b7a8      lea   eax, dword [ebp-0x118]
        |   0x00c0b7ae      movss dword [ebp-0xdc], xmm0
        |   0x00c0b7b6      movss xmm0, dword [ebp-0x24]
        |   0x00c0b7bb      push  eax
        |   0x00c0b7bc      movss dword [ebp-0xd8], xmm0
        |   0x00c0b7c4      lea   eax, dword [ebp-0x100]
        |   0x00c0b7ca      movss xmm0, dword [ebp-0x20]
        |   0x00c0b7cf      push  eax
        |   0x00c0b7d0      mov   byte [ebp-0x04], 0x07
        |   0x00c0b7d4      movss dword [ebp-0xd4], xmm0
        |   0x00c0b7dc      mov   dword [ebp-0xd0], 0x09
        |   0x00c0b7e6      call  0xaf9a30
        |   0x00c0b7eb      add   esp, 0x14
        |   0x00c0b7ee      mov   ecx, esp
        |   0x00c0b7f0      lea   esi, dword [eax+0x20]
        |   0x00c0b7f3      mov   dword [ecx], 0xffffffff              ; [0xffffffff:4]=-1 ; -1
        |   0x00c0b7f9      mov   eax, dword [esi]
        |   0x00c0b7fb      mov   dword [ecx], eax
        |   0x00c0b7fd      lea   eax, dword [ebp-0x14]
        |   0x00c0b800      push  eax
        |   0x00c0b801      call  0xdb0c80
        |   0x00c0b806      push  eax
        |   0x00c0b807      lea   eax, dword [ebp-0x124]
        |   0x00c0b80d      mov   byte [ebp-0x04], 0x08
        |   0x00c0b811      push  eax
        |   0x00c0b812      call  0xd8dab0
        |   0x00c0b817      add   esp, 0x10
        |   0x00c0b81a      mov   byte [ebp-0x04], 0x07
        |   0x00c0b81e      lea   ecx, dword [ebp-0x14]
        |   0x00c0b821      call  0x4dc500
        |   0x00c0b826      push  esi
        |   0x00c0b827      call  0xb9d8f0
        |   0x00c0b82c      add   esp, 0x04
        |   0x00c0b82f      cmp   dword [edi+0x14], 0x00
        |   0x00c0b833      mov   eax, dword [eax]
        |   0x00c0b835      mov   dword [ebp-0x120], eax
       ,==< 0x00c0b83b      jnz   0xc0b853
       ||   0x00c0b83d      lea   ecx, dword [ebp-0x120]
       ||   0x00c0b843      call  0xb01530
       ||   0x00c0b848      mov   ecx, dword [ebp-0x130]
       ||   0x00c0b84e      mov   eax, dword [eax+0x20]
       ||   0x00c0b851      mov   dword [ecx], eax
       `--> 0x00c0b853      lea   ecx, dword [ebp-0x60]
        |   0x00c0b856      call  0x4dc500
        |   0x00c0b85b      lea   ecx, dword [ebp-0x9c]
        |   0x00c0b861      call  0x975700
        |   0x00c0b866      cmp   dword [ebp-0xb0], 0x00
        |   0x00c0b86d      mov   byte [ebp-0x04], 0x09
        |   0x00c0b871      mov   dword [ebp-0xa4], 0x00
       ,==< 0x00c0b87b      jz    0xc0b897
       ||   0x00c0b87d      push  dword [ebp-0xa8]
       ||   0x00c0b883      push  0x00
       ||   0x00c0b885      call  0x5291c0
       ||   0x00c0b88a      add   esp, 0x08
       ||   0x00c0b88d      mov   dword [ebp-0xb0], 0x00
       `--> 0x00c0b897      lea   ecx, dword [ebp-0xb8]
        |   0x00c0b89d      call  0x4dc500
        |   0x00c0b8a2      lea   ecx, dword [ebp-0x110]
        |   0x00c0b8a8      mov   byte [ebp-0x04], 0x0a
        |   0x00c0b8ac      call  0x9d6700
        |   0x00c0b8b1      cmp   dword [ebp-0x118], 0x00
       ,==< 0x00c0b8b8      jz    0xc0b8ca
       ||   0x00c0b8ba      push  dword [ebp-0x110]
       ||   0x00c0b8c0      push  0x00
       ||   0x00c0b8c2      call  0x5291c0
       ||   0x00c0b8c7      add   esp, 0x08
       `--> 0x00c0b8ca      mov   esi, dword [ebp+0x0c]
        |   0x00c0b8cd      mov   byte [ebp-0x04], 0x05
        `-> 0x00c0b8d1      lea   ecx, dword [ebp-0x128]
            0x00c0b8d7      call  0x4f6c50
            0x00c0b8dc      cmp   dword [edi+0x14], 0x00
            0x00c0b8e0      mov   byte [ebp-0x04], 0x0b                ; 0xb ; 11
        ,=< 0x00c0b8e4      jz    0xc0bb94
        |   0x00c0b8ea      lea   ecx, dword [ebp-0x118]
        |   0x00c0b8f0      call  0x598730
        |   0x00c0b8f5      push  0xffffffff                           ; 255
        |   0x00c0b8f7      lea   eax, dword [ebp-0x38]
        |   0x00c0b8fa      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
        |   0x00c0b8fe      push  eax
        |   0x00c0b8ff      lea   ecx, dword [ebp-0x118]
        |   0x00c0b905      call  0xaf5040
        |   0x00c0b90a      push  0xffffffff                           ; 255
        |   0x00c0b90c      lea   eax, dword [ebp-0x28]
        |   0x00c0b90f      push  eax
        |   0x00c0b910      lea   ecx, dword [ebp-0x118]
        |   0x00c0b916      call  0xaf5150
        |   0x00c0b91b      push  0xffffffff                           ; 255
        |   0x00c0b91d      lea   eax, dword [edi+0x18]
        |   0x00c0b920      push  eax
        |   0x00c0b921      lea   ecx, dword [ebp-0x118]
        |   0x00c0b927      call  0xaf51e0
        |   0x00c0b92c      push  0xffffffff                           ; 255
        |   0x00c0b92e      lea   eax, dword [edi+0x6c]
        |   0x00c0b931      push  eax
        |   0x00c0b932      lea   ecx, dword [ebp-0x118]
        |   0x00c0b938      call  0xaf5260
        |   0x00c0b93d      cmp   esi, 0x04                            ; 4
       ,==< 0x00c0b940      jnb   0xc0b94a
       ||   0x00c0b942      lea   eax, dword [edi+0x74]
       ||   0x00c0b945      lea   eax, dword [eax+esi*4]
      ,===< 0x00c0b948      jmp   0xc0b956
      |`--> 0x00c0b94a      mov   eax, dword [edi+0x84]
      | |   0x00c0b950      lea   eax, dword [eax+esi*4]
      | |   0x00c0b953      add   eax, 0xfffffff0                      ; 4294967280
      `---> 0x00c0b956      push  0xffffffff                           ; 255
        |   0x00c0b958      push  eax
        |   0x00c0b959      lea   ecx, dword [ebp-0x118]
        |   0x00c0b95f      call  0xc07290
        |   0x00c0b964      push  0xffffffff                           ; 255
        |   0x00c0b966      lea   eax, dword [ebp-0x14]
        |   0x00c0b969      mov   dword [ebp-0x14], 0x00
        |   0x00c0b970      push  eax
        |   0x00c0b971      lea   ecx, dword [ebp-0x118]
        |   0x00c0b977      call  0xaf53e0
        |   0x00c0b97c      mov   eax, dword [edi+0x08]
        |   0x00c0b97f      lea   ecx, dword [ebp-0x118]
        |   0x00c0b985      push  0xffffffff                           ; 255
        |   0x00c0b987      add   eax, 0x20                            ; 32
        |   0x00c0b98a      push  eax
        |   0x00c0b98b      call  0xaf50d0
        |   0x00c0b990      push  0xffffffff                           ; 255
        |   0x00c0b992      push  dword [edi+0x10]
        |   0x00c0b995      lea   ecx, dword [ebp-0x118]
        |   0x00c0b99b      call  0xc07390
        |   0x00c0b9a0      mov   esi, dword [ebp-0x10c]
        |   0x00c0b9a6      mov   eax, dword [edi+0x0c]
        |   0x00c0b9a9      mov   edx, dword [ebp-0x110]
        |   0x00c0b9af      imul  ecx, esi, 0xb4
        |   0x00c0b9b5      mov   dword [ebp-0x14], eax
        |   0x00c0b9b8      mov   eax, edx
        |   0x00c0b9ba      add   ecx, eax
        |   0x00c0b9bc      cmp   eax, ecx
       ,==< 0x00c0b9be      jz    0xc0b9d8
      .---> 0x00c0b9c0      cmp   dword [eax], 0x6c                    ; 'l'
     ,====< 0x00c0b9c3      jnz   0xc0b9cb
     |:||   0x00c0b9c5      cmp   dword [eax+0x04], 0xffffffff
    ,=====< 0x00c0b9c9      jz    0xc0b9d4
    |`----> 0x00c0b9cb      add   eax, 0xb4                            ; 180
    | :||   0x00c0b9d0      cmp   eax, ecx
    | `===< 0x00c0b9d2      jnz   0xc0b9c0
    `-----> 0x00c0b9d4      cmp   eax, ecx
      ,===< 0x00c0b9d6      jnz   0xc0ba17
      |`--> 0x00c0b9d8      cmp   esi, dword [ebp-0x118]
      |,==< 0x00c0b9de      jnz   0xc0b9f1
      |||   0x00c0b9e0      lea   ecx, dword [ebp-0x118]
      |||   0x00c0b9e6      call  0x9d6ad0
      |||   0x00c0b9eb      mov   edx, dword [ebp-0x110]
      |`--> 0x00c0b9f1      imul  ecx, esi, 0xb4
      | |   0x00c0b9f7      lea   eax, dword [esi+0x01]
      | |   0x00c0b9fa      add   ecx, edx
      | |   0x00c0b9fc      mov   dword [ebp-0x10c], eax
      | |   0x00c0ba02      mov   edx, dword [ebp-0x14]
      | |   0x00c0ba05      mov   dword [ecx], 0x6c                    ; 'l'
      | |                                                              ; [0x6c:4]=-1 ; 108
      | |   0x00c0ba0b      mov   dword [ecx+0x04], 0xffffffff         ; [0xffffffff:4]=-1 ; -1
      | |   0x00c0ba12      mov   dword [ecx+0x08], edx
      |,==< 0x00c0ba15      jmp   0xc0ba1d
      `---> 0x00c0ba17      mov   edx, dword [ebp-0x14]
       ||   0x00c0ba1a      mov   dword [eax+0x08], edx
       `--> 0x00c0ba1d      lea   ecx, dword [ebp-0x100]
        |   0x00c0ba23      call  0xaf6620
        |   0x00c0ba28      movss xmm0, dword [ebp-0x38]
        |   0x00c0ba2d      mov   eax, dword [edi+0x08]
        |   0x00c0ba30      movss dword [ebp-0xe8], xmm0
        |   0x00c0ba38      movss xmm0, dword [ebp-0x34]
        |   0x00c0ba3d      push  0x01                                 ; 1
        |   0x00c0ba3f      movss dword [ebp-0xe4], xmm0
        |   0x00c0ba47      movss xmm0, dword [ebp-0x30]
        |   0x00c0ba4c      push  0x01                                 ; 1
        |   0x00c0ba4e      mov   dword [ebp-0xec], eax
        |   0x00c0ba54      mov   al, byte [ebp-0x101]
        |   0x00c0ba5a      movss dword [ebp-0xe0], xmm0
        |   0x00c0ba62      movss xmm0, dword [ebp-0x28]
        |   0x00c0ba67      push  0x01                                 ; 1
        |   0x00c0ba69      push  dword [edi+0x14]
        |   0x00c0ba6c      mov   byte [ebp-0xcc], al
        |   0x00c0ba72      lea   eax, dword [ebp-0x118]
        |   0x00c0ba78      movss dword [ebp-0xdc], xmm0
        |   0x00c0ba80      movss xmm0, dword [ebp-0x24]
        |   0x00c0ba85      push  eax
        |   0x00c0ba86      movss dword [ebp-0xd8], xmm0
        |   0x00c0ba8e      lea   eax, dword [ebp-0x100]
        |   0x00c0ba94      movss xmm0, dword [ebp-0x20]
        |   0x00c0ba99      push  eax
        |   0x00c0ba9a      mov   byte [ebp-0x04], 0x0d                ; 0xd ; 13
        |   0x00c0ba9e      movss dword [ebp-0xd4], xmm0
        |   0x00c0baa6      mov   dword [ebp-0xd0], 0x09
        |   0x00c0bab0      call  0xaf9a30
        |   0x00c0bab5      add   esp, 0x14
        |   0x00c0bab8      mov   ecx, esp
        |   0x00c0baba      lea   esi, dword [eax+0x20]
        |   0x00c0babd      mov   dword [ecx], 0xffffffff              ; [0xffffffff:4]=-1 ; -1
        |   0x00c0bac3      mov   eax, dword [esi]
        |   0x00c0bac5      mov   dword [ecx], eax
        |   0x00c0bac7      lea   eax, dword [ebp-0x108]
        |   0x00c0bacd      push  eax
        |   0x00c0bace      call  0xdb0c80
        |   0x00c0bad3      push  eax
        |   0x00c0bad4      lea   eax, dword [ebp-0x120]
        |   0x00c0bada      mov   byte [ebp-0x04], 0x0e                ; 0xe ; 14
        |   0x00c0bade      push  eax
        |   0x00c0badf      call  0xd8dab0
        |   0x00c0bae4      add   esp, 0x10
        |   0x00c0bae7      mov   byte [ebp-0x04], 0x0d                ; 0xd ; 13
        |   0x00c0baeb      lea   ecx, dword [ebp-0x108]
        |   0x00c0baf1      call  0x4dc500
        |   0x00c0baf6      push  esi
        |   0x00c0baf7      call  0xb9d8f0
        |   0x00c0bafc      add   esp, 0x04
        |   0x00c0baff      lea   ecx, dword [ebp-0x128]
        |   0x00c0bb05      mov   eax, dword [eax]
        |   0x00c0bb07      mov   dword [ebp-0x128], eax
        |   0x00c0bb0d      call  0xb01530
        |   0x00c0bb12      mov   ecx, dword [ebp-0x130]
        |   0x00c0bb18      mov   eax, dword [eax+0x20]
        |   0x00c0bb1b      mov   dword [ecx], eax
        |   0x00c0bb1d      lea   ecx, dword [ebp-0x60]
        |   0x00c0bb20      call  0x4dc500
        |   0x00c0bb25      lea   ecx, dword [ebp-0x9c]
        |   0x00c0bb2b      call  0x975700
        |   0x00c0bb30      cmp   dword [ebp-0xb0], 0x00
        |   0x00c0bb37      mov   byte [ebp-0x04], 0x0f                ; 0xf ; 15
        |   0x00c0bb3b      mov   dword [ebp-0xa4], 0x00
       ,==< 0x00c0bb45      jz    0xc0bb61
       ||   0x00c0bb47      push  dword [ebp-0xa8]
       ||   0x00c0bb4d      push  0x00
       ||   0x00c0bb4f      call  0x5291c0
       ||   0x00c0bb54      add   esp, 0x08
       ||   0x00c0bb57      mov   dword [ebp-0xb0], 0x00
       `--> 0x00c0bb61      lea   ecx, dword [ebp-0xb8]
        |   0x00c0bb67      call  0x4dc500
        |   0x00c0bb6c      lea   ecx, dword [ebp-0x110]
        |   0x00c0bb72      mov   byte [ebp-0x04], 0x10                ; 16
        |   0x00c0bb76      call  0x9d6700
        |   0x00c0bb7b      cmp   dword [ebp-0x118], 0x00
       ,==< 0x00c0bb82      jz    0xc0bb94
       ||   0x00c0bb84      push  dword [ebp-0x110]
       ||   0x00c0bb8a      push  0x00
       ||   0x00c0bb8c      call  0x5291c0
       ||   0x00c0bb91      add   esp, 0x08
       ``-> 0x00c0bb94      mov   dword [ebp-0x148], 0x00
            0x00c0bb9e      mov   dword [ebp-0x140], 0x00
            0x00c0bba8      mov   ecx, dword [ebp+0x0c]
            0x00c0bbab      lea   edx, dword [edi+0x1c]
            0x00c0bbae      cmp   ecx, 0x04                            ; 4
        ,=< 0x00c0bbb1      jnb   0xc0bbbc
        |   0x00c0bbb3      mov   eax, ecx
        |   0x00c0bbb5      shl   eax, 0x04
        |   0x00c0bbb8      add   eax, edx
       ,==< 0x00c0bbba      jmp   0xc0bbc5
       |`-> 0x00c0bbbc      lea   eax, dword [ecx-0x04]
       |    0x00c0bbbf      shl   eax, 0x04
       |    0x00c0bbc2      add   eax, dword [edx+0x40]
       `--> 0x00c0bbc5      movss xmm0, dword [eax]
            0x00c0bbc9      movss dword [ebp-0x188], xmm0
            0x00c0bbd1      movss xmm0, dword [eax+0x04]
            0x00c0bbd6      movss dword [ebp-0x184], xmm0
            0x00c0bbde      movss xmm0, dword [eax+0x08]
            0x00c0bbe3      mov   eax, dword [eax+0x0c]
            0x00c0bbe6      movss dword [ebp-0x180], xmm0
            0x00c0bbee      mov   dword [ebp-0x17c], eax
            0x00c0bbf4      mov   dword [ebp-0x144], 0x01
            0x00c0bbfe      mov   dword [ebp-0x44], 0x00
            0x00c0bc05      mov   dword [ebp-0x3c], 0x00
            0x00c0bc0c      cmp   ecx, 0x04                            ; 4
        ,=< 0x00c0bc0f      jnb   0xc0bc19
        |   0x00c0bc11      lea   eax, dword [ecx+0x1d]
        |   0x00c0bc14      lea   eax, dword [edi+eax*4]
       ,==< 0x00c0bc17      jmp   0xc0bc25
       |`-> 0x00c0bc19      mov   eax, dword [edi+0x84]
       |    0x00c0bc1f      lea   eax, dword [eax+ecx*4]
       |    0x00c0bc22      add   eax, 0xfffffff0                      ; 4294967280
       `--> 0x00c0bc25      mov   eax, dword [eax]
            0x00c0bc27      xor   esi, esi
            0x00c0bc29      mov   dword [ebp-0x54], eax
            0x00c0bc2c      mov   dword [ebp-0x40], 0x01
            0x00c0bc33      mov   dword [ebp-0x118], 0x00
            0x00c0bc3d      mov   dword [ebp-0x110], esi
            0x00c0bc43      mov   dword [ebp-0x10c], esi
            0x00c0bc49      mov   byte [ebp-0x04], 0x13                ; 19
            0x00c0bc4d      cmp   dword [edi+0xa8], esi
        ,=< 0x00c0bc53      jz    0xc0bc84
        |   0x00c0bc55      mov   eax, dword [edi+0xa4]
        |   0x00c0bc5b      lea   ecx, dword [ecx+ecx*4]
        |   0x00c0bc5e      lea   esi, dword [eax+ecx*4]
        |   0x00c0bc61      lea   ecx, dword [ebp-0x11c]
        |   0x00c0bc67      call  0xac31e0
        |   0x00c0bc6c      push  esi
        |   0x00c0bc6d      mov   esi, dword [ebp-0x110]
        |   0x00c0bc73      mov   ecx, esi
        |   0x00c0bc75      call  0x9009a0
        |   0x00c0bc7a      mov   dword [ebp-0x10c], 0x01
        `-> 0x00c0bc84      push  dword [0x1d6c084]
            0x00c0bc8a      push  0x01                                 ; 1
            0x00c0bc8c      push  0xac                                 ; 172
            0x00c0bc91      push  0x01                                 ; 1
            0x00c0bc93      call  0x529280
            0x00c0bc98      add   esp, 0x10
            0x00c0bc9b      mov   dword [ebp-0x108], eax
            0x00c0bca1      mov   byte [ebp-0x04], 0x14                ; 20
            0x00c0bca5      test  eax, eax
        ,=< 0x00c0bca7      jz    0xc0bd00
        |   0x00c0bca9      mov   cl, byte [edi+0x95]
        |   0x00c0bcaf      lea   eax, dword [ebp-0x11c]
        |   0x00c0bcb5      mov   dl, byte [edi+0x94]
        |   0x00c0bcbb      push  0x01                                 ; 1
        |   0x00c0bcbd      push  eax
        |   0x00c0bcbe      mov   esi, dword [edi+0x08]
        |   0x00c0bcc1      lea   eax, dword [ebp-0x54]
        |   0x00c0bcc4      push  ecx
        |   0x00c0bcc5      push  edx
        |   0x00c0bcc6      push  dword [edi+0x90]
        |   0x00c0bccc      push  eax
        |   0x00c0bccd      push  0x01                                 ; 1
        |   0x00c0bccf      push  dword [edi+0x6c]
        |   0x00c0bcd2      lea   eax, dword [ebp-0x188]
        |   0x00c0bcd8      push  dword [edi+0x68]
        |   0x00c0bcdb      sub   esp, 0x4c
        |   0x00c0bcde      mov   ecx, esp
        |   0x00c0bce0      push  eax
        |   0x00c0bce1      call  0xb2a2f0
        |   0x00c0bce6      mov   ecx, dword [ebp-0x108]
        |   0x00c0bcec      lea   eax, dword [edi+0x0c]
        |   0x00c0bcef      push  eax
        |   0x00c0bcf0      push  esi
        |   0x00c0bcf1      call  0xc08180
        |   0x00c0bcf6      mov   esi, dword [ebp-0x110]
        |   0x00c0bcfc      mov   edx, eax
       ,==< 0x00c0bcfe      jmp   0xc0bd02
       |`-> 0x00c0bd00      xor   edx, edx
       `--> 0x00c0bd02      mov   eax, dword [edi+0x90]
            0x00c0bd08      invalid
            0x00c0bd09      inc   ebp
            0x00c0bd0a      cld
            0x00c0de10      sub   esp, 0x08
            0x00c0de13      push  ebx
            0x00c0de14      push  ebp
            0x00c0de15      push  esi
            0x00c0de16      push  edi
            0x00c0de17      mov   edi, ecx
            0x00c0de19      cmp   dword [edi+0x08], 0x00
        ,=< 0x00c0de1d      jz    0xc0ded2
        |   0x00c0de23      cmp   dword [edi+0x0c], 0x00
       ,==< 0x00c0de27      jz    0xc0ded2
       ||   0x00c0de2d      cmp   dword [edi+0x60], 0x00
      ,===< 0x00c0de31      jz    0xc0ded2
      |||   0x00c0de37      mov   eax, dword [edi+0x18]
      |||   0x00c0de3a      test  eax, eax
     ,====< 0x00c0de3c      js    0xc0ded2
     ||||   0x00c0de42      cmp   eax, 0x05                            ; 5
    ,=====< 0x00c0de45      jnle  0xc0ded2
    |||||   0x00c0de4b      cmp   dword [edi+0x6c], 0x00
   ,======< 0x00c0de4f      jl    0xc0ded2
   ||||||   0x00c0de55      mov   eax, dword [edi+0x70]
   ||||||   0x00c0de58      test  eax, eax
  ,=======< 0x00c0de5a      jle   0xc0ded2
  |||||||   0x00c0de5c      mov   ecx, dword [edi+0x88]
  |||||||   0x00c0de62      cmp   eax, ecx
  ========< 0x00c0de64      jnz   0xc0ded2
  |||||||   0x00c0de66      mov   eax, dword [edi+0xa8]
  |||||||   0x00c0de6c      test  eax, eax
  ========< 0x00c0de6e      jz    0xc0de74
  |||||||   0x00c0de70      cmp   eax, ecx
  ========< 0x00c0de72      jnz   0xc0ded2
  --------> 0x00c0de74      mov   eax, dword [edi+0x90]
  |||||||   0x00c0de7a      cmp   eax, 0x02                            ; 2
  ========< 0x00c0de7d      jz    0xc0dec8
  |||||||   0x00c0de7f      cmp   eax, 0x01                            ; 1
  ========< 0x00c0de82      jnz   0xc0ded2
  |||||||   0x00c0de84      mov   eax, dword [0x201e2d8]               ; [0x201e2d8:4]=0
  |||||||   0x00c0de89      mov   ecx, dword [eax+0x38]
  |||||||   0x00c0de8c      mov   eax, dword [edi+0x60]
  |||||||   0x00c0de8f      mov   dword [esp+0x14], ecx
  |||||||   0x00c0de93      mov   dword [esp+0x10], eax
  |||||||   0x00c0de97      test  eax, eax
  ========< 0x00c0de99      jz    0xc0dec8
  |||||||   0x00c0de9b      xor   esi, esi
  |||||||   0x00c0de9d      lea   ebx, dword [esi-0x40]
  --------> 0x00c0dea0      lea   eax, dword [edi+0x5c]
  |||||||   0x00c0dea3      cmp   esi, 0x04                            ; 4
  ========< 0x00c0dea6      jb    0xc0deab
  |||||||   0x00c0dea8      mov   eax, dword [edi+0x5c]
  --------> 0x00c0deab      push  dword [edi+0x08]
  |||||||   0x00c0deae      add   eax, ebx
  |||||||   0x00c0deb0      push  eax
  |||||||   0x00c0deb1      call  0xaa0360
  |||||||   0x00c0deb6      test  al, al
  ========< 0x00c0deb8      jz    0xc0ded2
  |||||||   0x00c0deba      mov   ecx, dword [esp+0x14]
  |||||||   0x00c0debe      inc   esi
  |||||||   0x00c0debf      add   ebx, 0x10                            ; 16
  |||||||   0x00c0dec2      cmp   esi, dword [esp+0x10]
  ========< 0x00c0dec6      jnz   0xc0dea0
  --------> 0x00c0dec8      pop   edi
  |||||||   0x00c0dec9      pop   esi
  |||||||   0x00c0deca      pop   ebp
  |||||||   0x00c0decb      mov   al, 0x01
  |||||||   0x00c0decd      pop   ebx
  |||||||   0x00c0dece      add   esp, 0x08
  |||||||   0x00c0ded1      ret
  ```````-> 0x00c0ded2      pop   edi
            0x00c0ded3      pop   esi
            0x00c0ded4      pop   ebp
            0x00c0ded5      xor   al, al
            0x00c0ded7      pop   ebx
            0x00c0ded8      add   esp, 0x08
            0x00c0dedb      ret
            0x00c0dedc      int3
            0x00c0dedd      int3
            0x00c0dede      int3
            0x00c0dedf      int3
            0x00c0dee0      push  ebp
            0x00c0dee1      mov   ebp, esp
            0x00c0dee3      push  0xffffffff                           ; 255
            0x00c0dee5      push  0x18768bc
            0x00c0deea      mov   eax, dword fs:[0x0]
            0x00c0def0      push  eax
            0x00c0def1      sub   esp, 0xf4
            0x00c0def7      push  esi
            0x00c0def8      push  edi
            0x00c0def9      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0defe      xor   eax, ebp
            0x00c0df00      push  eax
            0x00c0df01      lea   eax, dword [ebp-0x0c]
            0x00c0df04      mov   dword fs:[0x0], eax
            0x00c0df0a      mov   edx, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c0df10      mov   eax, dword [edx+0x1c]
            0x00c0df13      mov   dword [ebp-0x60], 0x00
            0x00c0df1a      mov   dword [ebp-0x5c], 0x00
            0x00c0df21      mov   ecx, dword [eax*4+0x2028adc]
            0x00c0df28      mov   dword [ebp-0x64], ecx
            0x00c0df2b      test  ecx, ecx
        ,=< 0x00c0df2d      jz    0xc0df40
        |   0x00c0df2f      mov   eax, dword [ecx]
        |   0x00c0df31      lea   edx, dword [ebp-0x60]
        |   0x00c0df34      push  0x00
        |   0x00c0df36      push  edx
        |   0x00c0df37      call  dword [eax+0x3c]                     ; 60
        |   0x00c0df3a      mov   edx, dword [0x201f660]               ; [0x201f660:4]=0
        `-> 0x00c0df40      mov   eax, dword [edx+0x210]
            0x00c0df46      mov   dword [ebp-0x04], 0x00
            0x00c0df4d      mov   dword [ebp-0x6c], 0x00
            0x00c0df54      mov   dword [ebp-0x68], 0x00
            0x00c0df5b      mov   ecx, dword [eax*4+0x20286d8]
            0x00c0df62      mov   dword [ebp-0x70], ecx
            0x00c0df65      test  ecx, ecx
        ,=< 0x00c0df67      jz    0xc0df74
        |   0x00c0df69      mov   eax, dword [ecx]
        |   0x00c0df6b      lea   edx, dword [ebp-0x6c]
        |   0x00c0df6e      push  0x00
        |   0x00c0df70      push  edx
        |   0x00c0df71      call  dword [eax+0x40]                     ; 64
        `-> 0x00c0df74      mov   ecx, dword [0x2024798]               ; [0x2024798:4]=0
            0x00c0df7a      mov   byte [ebp-0x04], 0x01
            0x00c0df7e      call  0x5145c0
            0x00c0df83      mov   edi, eax
            0x00c0df85      mov   dword [ebp-0xec], 0x00
            0x00c0df8f      invalid
            0x00c0ddd0      cmp   dword [ecx+0x08], 0x00
        ,=< 0x00c0ddd4      jz    0xc0ddfe
        |   0x00c0ddd6      cmp   dword [ecx+0x0c], 0x00
       ,==< 0x00c0ddda      jz    0xc0ddfe
       ||   0x00c0dddc      mov   eax, dword [ecx+0x18]
       ||   0x00c0dddf      test  eax, eax
      ,===< 0x00c0dde1      js    0xc0ddfe
      |||   0x00c0dde3      cmp   eax, 0x05                            ; 5
     ,====< 0x00c0dde6      jnle  0xc0ddfe
     ||||   0x00c0dde8      cmp   dword [ecx+0x1c], 0x00
    ,=====< 0x00c0ddec      jl    0xc0ddfe
    |||||   0x00c0ddee      mov   eax, dword [ecx+0x20]
    |||||   0x00c0ddf1      cmp   eax, 0x02                            ; 2
   ,======< 0x00c0ddf4      jz    0xc0ddfb
   ||||||   0x00c0ddf6      cmp   eax, 0x01                            ; 1
  ,=======< 0x00c0ddf9      jnz   0xc0ddfe
  |`------> 0x00c0ddfb      mov   al, 0x01
  | |||||   0x00c0ddfd      ret
  `-`````-> 0x00c0ddfe      xor   al, al
            0x00c0de00      ret
            0x00c0de01      int3
            0x00c0de02      int3
            0x00c0de03      int3
            0x00c0de04      int3
            0x00c0de05      int3
            0x00c0de06      int3
            0x00c0de07      int3
            0x00c0de08      int3
            0x00c0de09      int3
            0x00c0de0a      int3
            0x00c0de0b      int3
            0x00c0de0c      int3
            0x00c0de0d      int3
            0x00c0de0e      int3
            0x00c0de0f      int3
            0x00c0de10      sub   esp, 0x08
            0x00c0de13      push  ebx
            0x00c0de14      push  ebp
            0x00c0de15      push  esi
            0x00c0de16      push  edi
            0x00c0de17      mov   edi, ecx
            0x00c0de19      cmp   dword [edi+0x08], 0x00
        ,=< 0x00c0de1d      jz    0xc0ded2
        |   0x00c0de23      cmp   dword [edi+0x0c], 0x00
       ,==< 0x00c0de27      jz    0xc0ded2
       ||   0x00c0de2d      cmp   dword [edi+0x60], 0x00
      ,===< 0x00c0de31      jz    0xc0ded2
      |||   0x00c0de37      mov   eax, dword [edi+0x18]
      |||   0x00c0de3a      test  eax, eax
     ,====< 0x00c0de3c      js    0xc0ded2
     ||||   0x00c0de42      cmp   eax, 0x05                            ; 5
    ,=====< 0x00c0de45      jnle  0xc0ded2
    |||||   0x00c0de4b      cmp   dword [edi+0x6c], 0x00
   ,======< 0x00c0de4f      jl    0xc0ded2
   ||||||   0x00c0de55      mov   eax, dword [edi+0x70]
   ||||||   0x00c0de58      test  eax, eax
  ,=======< 0x00c0de5a      jle   0xc0ded2
  |||||||   0x00c0de5c      mov   ecx, dword [edi+0x88]
  |||||||   0x00c0de62      cmp   eax, ecx
  ========< 0x00c0de64      jnz   0xc0ded2
  |||||||   0x00c0de66      mov   eax, dword [edi+0xa8]
  |||||||   0x00c0de6c      test  eax, eax
  ========< 0x00c0de6e      jz    0xc0de74
  |||||||   0x00c0de70      cmp   eax, ecx
  ========< 0x00c0de72      jnz   0xc0ded2
  --------> 0x00c0de74      mov   eax, dword [edi+0x90]
  |||||||   0x00c0de7a      cmp   eax, 0x02                            ; 2
  ========< 0x00c0de7d      jz    0xc0dec8
  |||||||   0x00c0de7f      cmp   eax, 0x01                            ; 1
  ========< 0x00c0de82      jnz   0xc0ded2
  |||||||   0x00c0de84      mov   eax, dword [0x201e2d8]               ; [0x201e2d8:4]=0
  |||||||   0x00c0de89      mov   ecx, dword [eax+0x38]
  |||||||   0x00c0de8c      mov   eax, dword [edi+0x60]
  |||||||   0x00c0de8f      mov   dword [esp+0x14], ecx
  |||||||   0x00c0de93      mov   dword [esp+0x10], eax
  |||||||   0x00c0de97      test  eax, eax
  ========< 0x00c0de99      jz    0xc0dec8
  |||||||   0x00c0de9b      xor   esi, esi
  |||||||   0x00c0de9d      lea   ebx, dword [esi-0x40]
  --------> 0x00c0dea0      lea   eax, dword [edi+0x5c]
  |||||||   0x00c0dea3      cmp   esi, 0x04                            ; 4
  ========< 0x00c0dea6      jb    0xc0deab
  |||||||   0x00c0dea8      mov   eax, dword [edi+0x5c]
  --------> 0x00c0deab      push  dword [edi+0x08]
  |||||||   0x00c0deae      add   eax, ebx
  |||||||   0x00c0deb0      push  eax
  |||||||   0x00c0deb1      call  0xaa0360
  |||||||   0x00c0deb6      test  al, al
  ========< 0x00c0deb8      jz    0xc0ded2
  |||||||   0x00c0deba      mov   ecx, dword [esp+0x14]
  |||||||   0x00c0debe      inc   esi
  |||||||   0x00c0debf      add   ebx, 0x10                            ; 16
  |||||||   0x00c0dec2      cmp   esi, dword [esp+0x10]
  ========< 0x00c0dec6      jnz   0xc0dea0
  --------> 0x00c0dec8      pop   edi
  |||||||   0x00c0dec9      pop   esi
  |||||||   0x00c0deca      pop   ebp
  |||||||   0x00c0decb      mov   al, 0x01
  |||||||   0x00c0decd      pop   ebx
  |||||||   0x00c0dece      add   esp, 0x08
  |||||||   0x00c0ded1      ret
  ```````-> 0x00c0ded2      pop   edi
            0x00c0ded3      pop   esi
            0x00c0ded4      pop   ebp
            0x00c0ded5      xor   al, al
            0x00c0ded7      pop   ebx
            0x00c0ded8      add   esp, 0x08
            0x00c0dedb      ret
            0x00c0dedc      int3
            0x00c0dedd      int3
            0x00c0dede      int3
            0x00c0dedf      int3
            0x00c0dee0      push  ebp
            0x00c0dee1      mov   ebp, esp
            0x00c0dee3      push  0xffffffff                           ; 255
            0x00c0dee5      push  0x18768bc
            0x00c0deea      mov   eax, dword fs:[0x0]
            0x00c0def0      push  eax
            0x00c0def1      sub   esp, 0xf4
            0x00c0def7      push  esi
            0x00c0def8      push  edi
            0x00c0def9      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c0defe      xor   eax, ebp
            0x00c0df00      push  eax
            0x00c0df01      lea   eax, dword [ebp-0x0c]
            0x00c0df04      mov   dword fs:[0x0], eax
            0x00c0df0a      mov   edx, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c0df10      mov   eax, dword [edx+0x1c]
            0x00c0df13      mov   dword [ebp-0x60], 0x00
            0x00c0df1a      mov   dword [ebp-0x5c], 0x00
            0x00c0df21      mov   ecx, dword [eax*4+0x2028adc]
            0x00c0df28      mov   dword [ebp-0x64], ecx
            0x00c0df2b      test  ecx, ecx
        ,=< 0x00c0df2d      jz    0xc0df40
        |   0x00c0df2f      mov   eax, dword [ecx]
        |   0x00c0df31      lea   edx, dword [ebp-0x60]
        |   0x00c0df34      push  0x00
        |   0x00c0df36      push  edx
        |   0x00c0df37      call  dword [eax+0x3c]                     ; 60
        |   0x00c0df3a      mov   edx, dword [0x201f660]               ; [0x201f660:4]=0
        `-> 0x00c0df40      mov   eax, dword [edx+0x210]
            0x00c0df46      mov   dword [ebp-0x04], 0x00
            0x00c0df4d      invalid
            0x00c0df4e      inc   ebp
            0x00c0df4f      xchg  esp, eax
            0x00b2f2c0      push  0x01                                 ; 1
            0x00b2f2c2      call  dword [eax+0x08]                     ; 8
            0x00b2f2c5      xor   eax, eax
            0x00b2f2c7      mov   ecx, dword [ebp-0x0c]
            0x00b2f2ca      mov   dword fs:[0x0], ecx
            0x00b2f2d1      pop   ecx
            0x00b2f2d2      pop   edi
            0x00b2f2d3      pop   esi
            0x00b2f2d4      mov   esp, ebp
            0x00b2f2d6      pop   ebp
            0x00b2f2d7      ret
            0x00b2f2d8      int3
            0x00b2f2d9      int3
            0x00b2f2da      int3
            0x00b2f2db      int3
            0x00b2f2dc      int3
            0x00b2f2dd      int3
            0x00b2f2de      int3
            0x00b2f2df      int3
            0x00b2f2e0      push  ebp
            0x00b2f2e1      mov   ebp, esp
            0x00b2f2e3      push  0xffffffff                           ; 255
            0x00b2f2e5      push  0x1848d23
            0x00b2f2ea      mov   eax, dword fs:[0x0]
            0x00b2f2f0      push  eax
            0x00b2f2f1      push  ecx
            0x00b2f2f2      push  esi
            0x00b2f2f3      push  edi
            0x00b2f2f4      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2f2f9      xor   eax, ebp
            0x00b2f2fb      push  eax
            0x00b2f2fc      lea   eax, dword [ebp-0x0c]
            0x00b2f2ff      mov   dword fs:[0x0], eax
            0x00b2f305      push  dword [0x1d6c084]
            0x00b2f30b      push  0x01                                 ; 1
            0x00b2f30d      push  0x10                                 ; 16
            0x00b2f30f      push  0x01                                 ; 1
            0x00b2f311      call  0x529280
            0x00b2f316      mov   esi, eax
            0x00b2f318      add   esp, 0x10
            0x00b2f31b      mov   dword [ebp-0x10], esi
            0x00b2f31e      mov   dword [ebp-0x04], 0x00
            0x00b2f325      test  esi, esi
        ,=< 0x00b2f327      jz    0xb2f338
        |   0x00b2f329      mov   ecx, esi
        |   0x00b2f32b      call  0xb21f60
        |   0x00b2f330      mov   dword [esi], 0x19a1a0c               ; [0x19a1a0c:4]=0x561c50
       ,==< 0x00b2f336      jmp   0xb2f33a
       |`-> 0x00b2f338      xor   esi, esi
       `--> 0x00b2f33a      mov   edi, dword [ebp+0x08]
            0x00b2f33d      mov   ecx, edi
            0x00b2f33f      invalid
            0x00b2f580      push  ebp
            0x00b2f581      mov   ebp, esp
            0x00b2f583      push  0xffffffff                           ; 255
            0x00b2f585      push  0x186932b
            0x00b2f58a      mov   eax, dword fs:[0x0]
            0x00b2f590      push  eax
            0x00b2f591      push  ecx
            0x00b2f592      push  ebx
            0x00b2f593      push  esi
            0x00b2f594      push  edi
            0x00b2f595      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2f59a      xor   eax, ebp
            0x00b2f59c      push  eax
            0x00b2f59d      lea   eax, dword [ebp-0x0c]
            0x00b2f5a0      mov   dword fs:[0x0], eax
            0x00b2f5a6      push  dword [0x1d6c084]
            0x00b2f5ac      push  0x01                                 ; 1
            0x00b2f5ae      push  0x18                                 ; 24
            0x00b2f5b0      push  0x01                                 ; 1
            0x00b2f5b2      call  0x529280
            0x00b2f5b7      mov   edi, eax
            0x00b2f5b9      add   esp, 0x10
            0x00b2f5bc      mov   dword [ebp-0x10], edi
            0x00b2f5bf      mov   dword [ebp-0x04], 0x00
            0x00b2f5c6      test  edi, edi
        ,=< 0x00b2f5c8      jz    0xb2f5ec
        |   0x00b2f5ca      mov   ecx, edi
        |   0x00b2f5cc      call  0xb21f60
        |   0x00b2f5d1      mov   dword [edi], 0x19a19e4               ; [0x19a19e4:4]=0x561c50
        |   0x00b2f5d7      lea   ecx, dword [edi+0x08]
        |   0x00b2f5da      mov   byte [ebp-0x04], 0x01
        |   0x00b2f5de      mov   dword [edi+0x04], 0x00
        |   0x00b2f5e5      call  0x4f71f0
       ,==< 0x00b2f5ea      jmp   0xb2f5ee
       |`-> 0x00b2f5ec      xor   edi, edi
       `--> 0x00b2f5ee      mov   ebx, dword [ebp+0x08]
            0x00b2f5f1      lea   ecx, dword [edi+0x04]
            0x00b2f5f4      push  0x04                                 ; 4
            0x00b2f5f6      push  ecx
            0x00b2f5f7      mov   ecx, ebx
            0x00b2f5f9      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b2f600      mov   eax, dword [ebx]
            0x00b2f602      mov   eax, dword [eax+0x04]
            0x00b2f605      call  eax
            0x00b2f607      test  al, al
        ,=< 0x00b2f609      jz    0xb2f632
        |   0x00b2f60b      mov   edx, dword [ebx]
        |   0x00b2f60d      mov   ecx, ebx
        |   0x00b2f60f      push  0x10                                 ; 16
        |   0x00b2f611      mov   esi, dword [edx+0x04]
        |   0x00b2f614      lea   edx, dword [edi+0x08]
        |   0x00b2f617      push  edx
        |   0x00b2f618      call  esi
        |   0x00b2f61a      test  al, al
       ,==< 0x00b2f61c      jz    0xb2f632
       ||   0x00b2f61e      mov   eax, edi
       ||   0x00b2f620      mov   ecx, dword [ebp-0x0c]
       ||   0x00b2f623      mov   dword fs:[0x0], ecx
       ||   0x00b2f62a      pop   ecx
       ||   0x00b2f62b      pop   edi
       ||   0x00b2f62c      pop   esi
       ||   0x00b2f62d      pop   ebx
       ||   0x00b2f62e      mov   esp, ebp
       ||   0x00b2f630      pop   ebp
       ||   0x00b2f631      ret
       ``-> 0x00b2f632      test  edi, edi
        ,=< 0x00b2f634      jz    0xb2f63f
        |   0x00b2f636      mov   eax, dword [edi]
        |   0x00b2f638      mov   ecx, edi
        |   0x00b2f63a      push  0x01                                 ; 1
        |   0x00b2f63c      call  dword [eax+0x08]                     ; 8
        `-> 0x00b2f63f      xor   eax, eax
            0x00b2f641      mov   ecx, dword [ebp-0x0c]
            0x00b2f644      mov   dword fs:[0x0], ecx
            0x00b2f64b      pop   ecx
            0x00b2f64c      pop   edi
            0x00b2f64d      pop   esi
            0x00b2f64e      pop   ebx
            0x00b2f64f      mov   esp, ebp
            0x00b2f651      pop   ebp
            0x00b2f652      ret
            0x00b2f653      int3
            0x00b2f654      int3
            0x00b2f655      int3
            0x00b2f656      int3
            0x00b2f657      int3
            0x00b2f658      int3
            0x00b2f659      int3
            0x00b2f65a      int3
            0x00b2f65b      int3
            0x00b2f65c      int3
            0x00b2f65d      int3
            0x00b2f65e      int3
            0x00b2f65f      int3
            0x00b2f660      push  ebp
            0x00b2f661      mov   ebp, esp
            0x00b2f663      push  0xffffffff                           ; 255
            0x00b2f665      push  0x1848d23
            0x00b2f66a      mov   eax, dword fs:[0x0]
            0x00b2f670      push  eax
            0x00b2f671      push  ecx
            0x00b2f672      push  esi
            0x00b2f673      push  edi
            0x00b2f674      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2f679      xor   eax, ebp
            0x00b2f67b      push  eax
            0x00b2f67c      lea   eax, dword [ebp-0x0c]
            0x00b2f67f      mov   dword fs:[0x0], eax
            0x00b2f685      push  dword [0x1d6c084]
            0x00b2f68b      push  0x01                                 ; 1
            0x00b2f68d      push  0x0c                                 ; 0xc ; 12
            0x00b2f68f      push  0x01                                 ; 1
            0x00b2f691      call  0x529280
            0x00b2f696      mov   esi, eax
            0x00b2f698      add   esp, 0x10
            0x00b2f69b      mov   dword [ebp-0x10], esi
            0x00b2f69e      mov   dword [ebp-0x04], 0x00
            0x00b2f6a5      test  esi, esi
        ,=< 0x00b2f6a7      jz    0xb2f6b8
        |   0x00b2f6a9      mov   ecx, esi
        |   0x00b2f6ab      call  0xb21f60
        |   0x00b2f6b0      mov   dword [esi], 0x19a1aac               ; [0x19a1aac:4]=0x5127a0
       ,==< 0x00b2f6b6      jmp   0xb2f6ba
       |`-> 0x00b2f6b8      xor   esi, esi
       `--> 0x00b2f6ba      mov   edi, dword [ebp+0x08]
            0x00b2f6bd      mov   ecx, edi
            0x00b2f6bf      push  0x04                                 ; 4
            0x00b2f6c1      mov   dword [ebp-0x04], 0xffffffff         ; -1
            0x00b2f6c8      mov   eax, dword [edi]
            0x00b2f6ca      mov   edx, dword [eax+0x04]
            0x00b2f6cd      lea   eax, dword [esi+0x04]
            0x00b2f6d0      push  eax
            0x00b2f6d1      call  edx
            0x00b2f6d3      test  al, al
        ,=< 0x00b2f6d5      jnz   0xb2f6f7
       .--> 0x00b2f6d7      test  esi, esi
      ,===< 0x00b2f6d9      jz    0xb2f6e4
      |:|   0x00b2f6db      mov   eax, dword [esi]
      |:|   0x00b2f6dd      mov   ecx, esi
      |:|   0x00b2f6df      push  0x01                                 ; 1
      |:|   0x00b2f6e1      call  dword [eax+0x08]                     ; 8
      `---> 0x00b2f6e4      xor   eax, eax
       :|   0x00b2f6e6      mov   ecx, dword [ebp-0x0c]
       :|   0x00b2f6e9      mov   dword fs:[0x0], ecx
       :|   0x00b2f6f0      pop   ecx
       :|   0x00b2f6f1      pop   edi
       :|   0x00b2f6f2      pop   esi
       :|   0x00b2f6f3      mov   esp, ebp
       :|   0x00b2f6f5      pop   ebp
       :|   0x00b2f6f6      ret
       :`-> 0x00b2f6f7      mov   eax, dword [edi]
       :    0x00b2f6f9      mov   ecx, edi
       :    0x00b2f6fb      push  0x04                                 ; 4
       :    0x00b2f6fd      mov   edx, dword [eax+0x04]
       :    0x00b2f700      lea   eax, dword [esi+0x08]
       :    0x00b2f703      push  eax
       :    0x00b2f704      call  edx
       :    0x00b2f706      test  al, al
       `==< 0x00b2f708      jz    0xb2f6d7
            0x00b2f70a      mov   eax, esi
            0x00b2f70c      mov   ecx, dword [ebp-0x0c]
            0x00b2f70f      invalid
