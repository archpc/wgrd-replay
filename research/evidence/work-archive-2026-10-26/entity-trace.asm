            0x00ae5690      push  ebx
            0x00ae5691      push  ebp
            0x00ae5692      mov   ebp, dword [esp+0x0c]
            0x00ae5696      mov   ebx, ecx
            0x00ae5698      push  esi
            0x00ae5699      push  edi
            0x00ae569a      mov   esi, dword [ebx+0x14]
            0x00ae569d      and   esi, 0x7ffffff
        ,=< 0x00ae56a3      jz    0xae56e7
        |   0x00ae56a5      mov   eax, dword [ebp]
        |   0x00ae56a8      mov   edx, eax
        |   0x00ae56aa      shl   eax, 0x04
        |   0x00ae56ad      xor   edx, 0xdeadbeef
        |   0x00ae56b3      add   edx, eax
        |   0x00ae56b5      mov   eax, edx
        |   0x00ae56b7      shr   eax, 0x0a
        |   0x00ae56ba      xor   edx, eax
        |   0x00ae56bc      mov   eax, edx
        |   0x00ae56be      shr   eax, 0x18
        |   0x00ae56c1      add   eax, edx
        |   0x00ae56c3      imul  ecx, eax, 0x81
        |   0x00ae56c9      lea   eax, dword [esp+0x14]
        |   0x00ae56cd      push  eax
        |   0x00ae56ce      mov   eax, ecx
        |   0x00ae56d0      shr   eax, 0x0d
        |   0x00ae56d3      xor   eax, ecx
        |   0x00ae56d5      lea   ecx, dword [ebx+0x14]
        |   0x00ae56d8      push  eax
        |   0x00ae56d9      push  ebp
        |   0x00ae56da      call  0x5cffc0
        |   0x00ae56df      mov   eax, dword [esp+0x14]
        |   0x00ae56e3      test  eax, eax
       ,==< 0x00ae56e5      jnz   0xae56f0
       |`-> 0x00ae56e7      mov   eax, dword [ebx+0x18]
       |    0x00ae56ea      lea   ecx, dword [esi+esi*2]
       |    0x00ae56ed      lea   eax, dword [eax+ecx*4]
       `--> 0x00ae56f0      mov   ecx, dword [ebx+0x18]
            0x00ae56f3      lea   edx, dword [esi+esi*2]
            0x00ae56f6      lea   ecx, dword [ecx+edx*4]
            0x00ae56f9      cmp   eax, ecx
        ,=< 0x00ae56fb      jz    0xae5707
        |   0x00ae56fd      add   eax, 0x04
        |   0x00ae5700      pop   edi
        |   0x00ae5701      pop   esi
        |   0x00ae5702      pop   ebp
        |   0x00ae5703      pop   ebx
        |   0x00ae5704      ret   0x04
        `-> 0x00ae5707      pop   edi
            0x00ae5708      pop   esi
            0x00ae5709      mov   eax, ebp
            0x00ae570b      pop   ebp
            0x00ae570c      pop   ebx
            0x00ae570d      ret   0x04
            0x00ae5710      mov   eax, dword [esp+0x04]
            0x00ae5714      mov   dword [eax], 0xffffffff              ; [0xffffffff:4]=-1 ; -1
            0x00ae571a      mov   ecx, dword [ecx+0x18]
            0x00ae571d      mov   dword [eax], ecx
            0x00ae571f      ret   0x04
            0x00ae5722      int3
            0x00ae5723      int3
            0x00ae5724      int3
            0x00ae5725      int3
            0x00ae5726      int3
            0x00ae5727      int3
            0x00ae5728      int3
            0x00ae5729      int3
            0x00ae572a      int3
            0x00ae572b      int3
            0x00ae572c      int3
            0x00ae572d      int3
            0x00ae572e      int3
            0x00ae572f      int3
            0x00ae5730      push  ecx
            0x00ae5731      push  ebx
            0x00ae5732      push  esi
            0x00ae5733      push  edi
            0x00ae5734      mov   ebx, ecx
            0x00ae5736      call  0x512430
            0x00ae573b      mov   edx, dword [esp+0x14]
            0x00ae573f      cmp   edx, dword [eax]
        ,=< 0x00ae5741      jnz   0xae574c
       .--> 0x00ae5743      xor   eax, eax
       :|   0x00ae5745      pop   edi
       :|   0x00ae5746      pop   esi
       :|   0x00ae5747      pop   ebx
       :|   0x00ae5748      pop   ecx
       :|   0x00ae5749      ret   0x08
       :`-> 0x00ae574c      mov   esi, dword [ebx+0x04]
       :    0x00ae574f      and   esi, 0x7ffffff
       :,=< 0x00ae5755      jz    0xae579a
       :|   0x00ae5757      mov   ecx, edx
       :|   0x00ae5759      shl   edx, 0x04
       :|   0x00ae575c      xor   ecx, 0xdeadbeef
       :|   0x00ae5762      add   ecx, edx
       :|   0x00ae5764      mov   eax, ecx
       :|   0x00ae5766      shr   eax, 0x0a
       :|   0x00ae5769      xor   ecx, eax
       :|   0x00ae576b      mov   eax, ecx
       :|   0x00ae576d      shr   eax, 0x18
       :|   0x00ae5770      add   eax, ecx
       :|   0x00ae5772      imul  ecx, eax, 0x81
       :|   0x00ae5778      lea   eax, dword [esp+0x0c]
       :|   0x00ae577c      push  eax
       :|   0x00ae577d      mov   eax, ecx
       :|   0x00ae577f      shr   eax, 0x0d
       :|   0x00ae5782      xor   eax, ecx
       :|   0x00ae5784      lea   ecx, dword [ebx+0x04]
       :|   0x00ae5787      push  eax
       :|   0x00ae5788      lea   eax, dword [esp+0x1c]
       :|   0x00ae578c      push  eax
       :|   0x00ae578d      call  0x4dc510
       :|   0x00ae5792      mov   eax, dword [esp+0x0c]
       :|   0x00ae5796      test  eax, eax
      ,===< 0x00ae5798      jnz   0xae57a0
      |:`-> 0x00ae579a      mov   eax, dword [ebx+0x08]
      |:    0x00ae579d      lea   eax, dword [eax+esi*8]
      `---> 0x00ae57a0      mov   ecx, dword [ebx+0x08]
       :    0x00ae57a3      lea   ecx, dword [ecx+esi*8]
       :    0x00ae57a6      cmp   eax, ecx
       `==< 0x00ae57a8      jz    0xae5743
            0x00ae57aa      mov   eax, dword [eax+0x04]
            0x00ae57ad      pop   edi
            0x00ae57ae      pop   esi
            0x00ae57af      pop   ebx
            0x00ae57b0      pop   ecx
            0x00ae57b1      ret   0x08
            0x00ae57b4      int3
            0x00ae57b5      int3
            0x00ae57b6      int3
            0x00ae57b7      int3
            0x00ae57b8      int3
            0x00ae57b9      int3
            0x00ae57ba      int3
            0x00ae57bb      int3
            0x00ae57bc      int3
            0x00ae57bd      int3
            0x00ae57be      int3
            0x00ae57bf      int3
            0x00ae57c0      add   ecx, 0x14                            ; 20
            0x00ae57c3      push  esi
            0x00ae57c4      mov   esi, dword [esp+0x08]
            0x00ae57c8      cmp   dword [ecx], 0xffffffff
        ,=< 0x00ae57cb      jz    0xae57ef
        |   0x00ae57cd      call  0xb014f0
        |   0x00ae57d2      mov   ecx, eax
        |   0x00ae57d4      call  0xa735d0
        |   0x00ae57d9      mov   ecx, dword [eax]
        |   0x00ae57db      mov   dword [esi], ecx
        |   0x00ae57dd      mov   ecx, dword [eax+0x04]
        |   0x00ae57e0      mov   dword [esi+0x04], ecx
        |   0x00ae57e3      mov   ecx, dword [eax+0x08]
        |   0x00ae57e6      mov   eax, esi
        |   0x00ae57e8      mov   dword [esi+0x08], ecx
        |   0x00ae57eb      pop   esi
        |   0x00ae57ec      ret   0x04
        `-> 0x00ae57ef      mov   dword [esi], 0x3f800000              ; [0x3f800000:4]=-1
            0x00ae57f5      mov   eax, esi
            0x00ae57f7      mov   dword [esi+0x04], 0x00
            0x00ae57fe      mov   dword [esi+0x08], 0x00
            0x00ae5805      pop   esi
            0x00ae5806      ret   0x04
            0x00ae5809      int3
            0x00ae580a      int3
            0x00ae580b      int3
            0x00ae580c      int3
            0x00ae580d      int3
            0x00ae580e      int3
            0x00ae580f      int3
            0x00ae5810      sub   esp, 0x08
            0x00ae5813      push  esi
            0x00ae5814      mov   esi, dword [esp+0x10]
            0x00ae5818      push  edi
            0x00ae5819      sub   esp, 0x08
            0x00ae581c      movups xmm0, xmmword [esi]
            0x00ae581f      shufps xmm0, xmmword [esi], 0x55
            0x00ae5823      mulss xmm0, dword [esp+0x24]
            0x00ae5829      cvtss2sd xmm0, xmm0
            0x00ae582d      movsd qword [esp+0x10], xmm0
            0x00ae5833      fld   qword [esp+0x10]
            0x00ae5837      fstp  qword [esp]
            0x00ae583a      call  0x1809c2e
            0x00ae583f      fstp  qword [esp+0x10]
            0x00ae5843      movsd xmm0, qword [esp+0x10]
            0x00ae5849      add   esp, 0x08
            0x00ae584c      cvtpd2ps xmm0, xmm0
            0x00ae5850      call  0x18077c0
            0x00ae5855      mov   ecx, dword [esp+0x18]
            0x00ae5859      sub   esp, 0x08
            0x00ae585c      mov   edi, eax
            0x00ae585e      movss xmm0, dword [ecx]
            0x00ae5862      mulss xmm0, dword [esp+0x24]
            0x00ae5868      cvtps2pd xmm0, xmm0
            0x00ae586b      movsd qword [esp+0x10], xmm0
            0x00ae5871      fld   qword [esp+0x10]
            0x00ae5875      fstp  qword [esp]
            0x00ae5878      call  0x1809c2e
            0x00ae587d      fstp  qword [esp+0x10]
            0x00ae5881      movsd xmm0, qword [esp+0x10]
            0x00ae5887      add   esp, 0x08
            0x00ae588a      cvtpd2ps xmm0, xmm0
            0x00ae588e      call  0x18077c0
            0x00ae5893      movups xmm0, xmmword [esi]
            0x00ae5896      sub   esp, 0x08
            0x00ae5899      mulss xmm0, dword [esp+0x24]
            0x00ae589f      imul  edi, eax
            0x00ae58a2      cvtss2sd xmm0, xmm0
            0x00ae58a6      movsd qword [esp+0x10], xmm0
            0x00ae58ac      fld   qword [esp+0x10]
            0x00ae58b0      fstp  qword [esp]
            0x00ae58b3      call  0x1809c2e
            0x00ae58b8      fstp  qword [esp+0x10]
            0x00ae58bc      movsd xmm0, qword [esp+0x10]
            0x00ae58c2      add   esp, 0x08
            0x00ae58c5      cvtpd2ps xmm0, xmm0
            0x00ae58c9      call  0x18077c0
            0x00ae58ce      add   eax, edi
            0x00ae58d0      pop   edi
            0x00ae58d1      pop   esi
            0x00ae58d2      add   esp, 0x08
            0x00ae58d5      ret
            0x00ae58d6      int3
            0x00ae58d7      int3
            0x00ae58d8      int3
            0x00ae58d9      int3
            0x00ae58da      int3
            0x00ae58db      int3
            0x00ae58dc      int3
            0x00ae58dd      int3
            0x00ae58de      int3
            0x00ae58df      int3
            0x00ae58e0      mov   eax, dword [esp+0x04]
            0x00ae58e4      mov   edx, ecx
            0x00ae58e6      push  0x4de290
            0x00ae58eb      lea   eax, dword [eax*2-0x01]
            0x00ae58f2      bsr   ecx, eax
            0x00ae58f5      mov   eax, 0x01
            0x00ae58fa      shl   eax, cl
            0x00ae58fc      mov   ecx, edx
            0x00ae58fe      push  eax
            0x00ae58ff      call  0xadd960
            0x00ae5904      ret   0x04
            0x00ae5907      int3
            0x00ae5908      int3
            0x00ae5909      int3
            0x00ae590a      int3
            0x00ae590b      int3
            0x00ae590c      int3
            0x00ae590d      int3
            0x00ae590e      int3
            0x00ae590f      int3
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
            0x00b5af5f      invalid
            0x00b2ddd0      sub   esp, 0x1c
            0x00b2ddd3      push  esi
            0x00b2ddd4      mov   esi, dword [esp+0x28]
            0x00b2ddd8      lea   eax, dword [esp+0x30]
            0x00b2dddc      push  edi
            0x00b2dddd      push  eax
            0x00b2ddde      lea   ecx, dword [esp+0x18]
            0x00b2dde2      call  0x4f70d0
            0x00b2dde7      lea   eax, dword [esp+0x14]
            0x00b2ddeb      push  0x01                                 ; 1
            0x00b2dded      push  eax
            0x00b2ddee      call  0xb5abd0
            0x00b2ddf3      add   esp, 0x08
            0x00b2ddf6      lea   ecx, dword [esp+0x10]
            0x00b2ddfa      mov   edi, eax
            0x00b2ddfc      lea   eax, dword [esp+0x0b]
            0x00b2de00      push  eax
            0x00b2de01      push  dword [esp+0x34]
            0x00b2de05      call  0x4f7950
            0x00b2de0a      mov   edx, dword [esp+0x10]
            0x00b2de0e      lea   eax, dword [esp+0x0c]
            0x00b2de12      push  eax
            0x00b2de13      mov   ecx, esi
            0x00b2de15      mov   dword [esp+0x10], edx
            0x00b2de19      call  0xae5690
            0x00b2de1e      mov   ecx, dword [esp+0x0c]
            0x00b2de22      cmp   ecx, dword [eax]
        ,=< 0x00b2de24      jnz   0xb2de34
        |   0x00b2de26      cmp   edi, dword [esp+0x44]
       ,==< 0x00b2de2a      jz    0xb2de34
       ||   0x00b2de2c      pop   edi
       ||   0x00b2de2d      xor   al, al
       ||   0x00b2de2f      pop   esi
       ||   0x00b2de30      add   esp, 0x1c
       ||   0x00b2de33      ret
       ``-> 0x00b2de34      pop   edi
            0x00b2de35      mov   al, 0x01
            0x00b2de37      pop   esi
            0x00b2de38      add   esp, 0x1c
            0x00b2de3b      ret
            0x00b2de3c      int3
            0x00b2de3d      int3
            0x00b2de3e      int3
            0x00b2de3f      int3
            0x00b2de40      push  ebp
            0x00b2de41      mov   ebp, esp
            0x00b2de43      push  0xffffffff                           ; 255
            0x00b2de45      push  0x1818230
            0x00b2de4a      mov   eax, dword fs:[0x0]
            0x00b2de50      push  eax
            0x00b2de51      sub   esp, 0x10
            0x00b2de54      push  ebx
            0x00b2de55      push  esi
            0x00b2de56      push  edi
            0x00b2de57      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2de5c      xor   eax, ebp
            0x00b2de5e      push  eax
            0x00b2de5f      lea   eax, dword [ebp-0x0c]
            0x00b2de62      mov   dword fs:[0x0], eax
            0x00b2de68      mov   ebx, ecx
            0x00b2de6a      mov   dword [ebp-0x14], ebx
            0x00b2de6d      mov   dword [ebx+0x74], 0x00
            0x00b2de74      mov   eax, 0x01
            0x00b2de79      mov   dword [ebx+0x68], 0x00
            0x00b2de80      mov   ecx, 0x1fceff8
            0x00b2de85      mov   dword [ebx+0x6c], 0x00
            0x00b2de8c      mov   dword [ebx+0x98], 0x00
            0x00b2de96      mov   dword [ebx+0x9c], 0x05
            0x00b2dea0      mov   word [ebx+0xa0], 0x00
            0x00b2dea9      mov   word [ebx+0xa3], 0x00
            0x00b2deb2      mov   byte [ebx+0xa6], 0x00
            0x00b2deb9      xchg  dword [ecx], eax
            0x00b2debb      mov   eax, dword [ebx+0x08]
            0x00b2debe      lea   ecx, dword [ebx+0x08]
            0x00b2dec1      push  0x00
            0x00b2dec3      call  dword [eax+0x10]                     ; 16
            0x00b2dec6      mov   eax, dword [ebx+0x08]
            0x00b2dec9      lea   ecx, dword [ebx+0x08]
            0x00b2decc      push  0x00
            0x00b2dece      call  dword [eax+0x20]                     ; 32
            0x00b2ded1      mov   dword [ebx+0x60], 0x00
            0x00b2ded8      mov   ecx, dword [ebx+0x84]
            0x00b2dede      mov   eax, dword [ebx+0x88]
            0x00b2dee4      and   ecx, 0x7ffffff
            0x00b2deea      mov   esi, eax
            0x00b2deec      lea   edi, dword [eax+ecx*8]
            0x00b2deef      cmp   esi, edi
        ,=< 0x00b2def1      jz    0xb2df16
       .--> 0x00b2def3      mov   ebx, dword [esi+0x04]
       :|   0x00b2def6      test  ebx, ebx
      ,===< 0x00b2def8      jz    0xb2df0c
      |:|   0x00b2defa      mov   ecx, ebx
      |:|   0x00b2defc      call  0xb2b160
      |:|   0x00b2df01      push  0x14                                 ; 20
      |:|   0x00b2df03      push  ebx
      |:|   0x00b2df04      call  0x1807170
      |:|   0x00b2df09      add   esp, 0x08
      `---> 0x00b2df0c      add   esi, 0x08
       :|   0x00b2df0f      cmp   esi, edi
       `==< 0x00b2df11      jnz   0xb2def3
        |   0x00b2df13      mov   ebx, dword [ebp-0x14]
        `-> 0x00b2df16      lea   ecx, dword [ebx+0x84]
            0x00b2df1c      call  0x609120
            0x00b2df21      mov   eax, dword [ebx+0x80]
            0x00b2df27      mov   edx, dword [ebx+0x7c]
            0x00b2df2a      and   edx, 0x7ffffff
            0x00b2df30      mov   dword [ebp-0x10], eax
            0x00b2df33      lea   ecx, dword [eax+edx*8]
            0x00b2df36      mov   dword [ebp-0x1c], ecx
            0x00b2df39      cmp   eax, ecx
        ,=< 0x00b2df3b      jz    0xb2e028
       .--> 0x00b2df41      mov   ebx, dword [eax+0x04]
       :|   0x00b2df44      mov   dword [ebp-0x18], ebx
       :|   0x00b2df47      test  ebx, ebx
      ,===< 0x00b2df49      jz    0xb2e017
      |:|   0x00b2df4f      mov   ecx, dword [ebx+0x58]
      |:|   0x00b2df52      mov   eax, dword [ebx+0x5c]
      |:|   0x00b2df55      and   ecx, 0x7ffffff
      |:|   0x00b2df5b      mov   esi, eax
      |:|   0x00b2df5d      lea   edi, dword [eax+ecx*8]
      |:|   0x00b2df60      cmp   esi, edi
     ,====< 0x00b2df62      jz    0xb2df8f
    .-----> 0x00b2df64      mov   ebx, dword [esi+0x04]
    :||:|   0x00b2df67      cmp   ebx, dword [0x203acc0]               ; [0x203acc0:4]=0
   ,======< 0x00b2df6d      jz    0xb2df85
   |:||:|   0x00b2df6f      test  ebx, ebx
  ,=======< 0x00b2df71      jz    0xb2df85
  ||:||:|   0x00b2df73      mov   ecx, ebx
  ||:||:|   0x00b2df75      call  0x4fb700
  ||:||:|   0x00b2df7a      push  0x60                                 ; '`' ; 96
  ||:||:|   0x00b2df7c      push  ebx
  ||:||:|   0x00b2df7d      call  0x1807170
  ||:||:|   0x00b2df82      add   esp, 0x08
  ``------> 0x00b2df85      add   esi, 0x08
    :||:|   0x00b2df88      cmp   esi, edi
    `=====< 0x00b2df8a      jnz   0xb2df64
     ||:|   0x00b2df8c      mov   ebx, dword [ebp-0x18]
     `----> 0x00b2df8f      lea   ecx, dword [ebx+0x58]
      |:|   0x00b2df92      call  0x609120
      |:|   0x00b2df97      lea   ecx, dword [ebx+0x68]
      |:|   0x00b2df9a      call  0x4f9660
      |:|   0x00b2df9f      lea   ecx, dword [ebx+0x60]
      |:|   0x00b2dfa2      call  0x771be0
      |:|   0x00b2dfa7      lea   ecx, dword [ebx+0x58]
      |:|   0x00b2dfaa      call  0x4f9660
      |:|   0x00b2dfaf      mov   dword [ebx+0x44], 0x00
      |:|   0x00b2dfb6      cmp   dword [ebx+0x38], 0x00
      |:|   0x00b2dfba      mov   dword [ebp-0x04], 0x00
     ,====< 0x00b2dfc1      jz    0xb2dfd7
     ||:|   0x00b2dfc3      push  dword [ebx+0x40]
     ||:|   0x00b2dfc6      push  0x00
     ||:|   0x00b2dfc8      call  0x5291c0
     ||:|   0x00b2dfcd      add   esp, 0x08
     ||:|   0x00b2dfd0      mov   dword [ebx+0x38], 0x00
     `----> 0x00b2dfd7      mov   dword [ebx+0x14], 0x00
      |:|   0x00b2dfde      cmp   dword [ebx+0x08], 0x00
      |:|   0x00b2dfe2      mov   dword [ebp-0x04], 0x01
     ,====< 0x00b2dfe9      jz    0xb2dfff
     ||:|   0x00b2dfeb      push  dword [ebx+0x10]
     ||:|   0x00b2dfee      push  0x00
     ||:|   0x00b2dff0      call  0x5291c0
     ||:|   0x00b2dff5      add   esp, 0x08
     ||:|   0x00b2dff8      mov   dword [ebx+0x08], 0x00
     `----> 0x00b2dfff      push  0x70                                 ; 'p' ; 112
      |:|   0x00b2e001      push  ebx
      |:|   0x00b2e002      mov   dword [ebp-0x04], 0xffffffff         ; -1
      |:|   0x00b2e009      call  0x1807170
      |:|   0x00b2e00e      mov   eax, dword [ebp-0x10]
      |:|   0x00b2e011      add   esp, 0x08
      |:|   0x00b2e014      mov   ecx, dword [ebp-0x1c]
      `---> 0x00b2e017      add   eax, 0x08
       :|   0x00b2e01a      mov   dword [ebp-0x10], eax
       :|   0x00b2e01d      cmp   eax, ecx
       `==< 0x00b2e01f      jnz   0xb2df41
        |   0x00b2e025      mov   ebx, dword [ebp-0x14]
        `-> 0x00b2e028      lea   ecx, dword [ebx+0x7c]
            0x00b2e02b      call  0x609120
            0x00b2e030      mov   ecx, dword [ebx+0xac]
            0x00b2e036      mov   byte [ebx+0xa7], 0x00
            0x00b2e03d      test  ecx, ecx
        ,=< 0x00b2e03f      jz    0xb2e052
        |   0x00b2e041      push  0x03                                 ; 3
        |   0x00b2e043      call  0x58b460
        |   0x00b2e048      mov   dword [ebx+0xac], 0x00
        `-> 0x00b2e052      mov   ecx, dword [ebp-0x0c]
            0x00b2e055      mov   dword fs:[0x0], ecx
            0x00b2e05c      pop   ecx
            0x00b2e05d      pop   edi
            0x00b2e05e      pop   esi
            0x00b2e05f      pop   ebx
            0x00b2e060      mov   esp, ebp
            0x00b2e062      pop   ebp
            0x00b2e063      ret
            0x00b2e064      int3
            0x00b2e065      int3
            0x00b2e066      int3
            0x00b2e067      int3
            0x00b2e068      int3
            0x00b2e069      int3
            0x00b2e06a      int3
            0x00b2e06b      int3
            0x00b2e06c      int3
            0x00b2e06d      int3
            0x00b2e06e      int3
            0x00b2e06f      int3
            0x00b2e070      push  ebp
            0x00b2e071      mov   ebp, esp
            0x00b2e073      push  0xffffffff                           ; 255
            0x00b2e075      push  0x1869209
            0x00b2e07a      mov   eax, dword fs:[0x0]
            0x00b2e080      push  eax
            0x00b2e081      sub   esp, 0x74
            0x00b2e084      push  ebx
            0x00b2e085      push  esi
            0x00b2e086      push  edi
            0x00b2e087      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2e08c      xor   eax, ebp
            0x00b2e08e      push  eax
            0x00b2e08f      lea   eax, dword [ebp-0x0c]
            0x00b2e092      mov   dword fs:[0x0], eax
            0x00b2e098      mov   dword [ebp-0x1c], 0x00
            0x00b2e09f      mov   esi, dword [ebp+0x08]
            0x00b2e0a2      mov   ecx, esi
            0x00b2e0a4      mov   dword [ebp-0x04], 0x00
            0x00b2e0ab      call  0x4ea3a0
            0x00b2e0b0      mov   dword [esi+0x04], 0x00
            0x00b2e0b7      lea   edi, dword [esi+0x20]
            0x00b2e0ba      mov   dword [esi+0x08], 0x00
            0x00b2e0c1      mov   dword [esi+0x10], 0x00
            0x00b2e0c8      mov   dword [esi+0x18], 0x00
            0x00b2e0cf      mov   dword [esi+0x1c], 0x00
            0x00b2e0d6      mov   dword [edi+0x04], 0x00
            0x00b2e0dd      mov   dword [edi+0x0c], 0x00
            0x00b2e0e4      mov   dword [edi+0x10], 0x00
            0x00b2e0eb      mov   dword [esi], 0x19a1b30               ; [0x19a1b30:4]=0xb2b5b0
            0x00b2e0f1      mov   eax, dword [ebp+0x14]
            0x00b2e0f4      xor   ebx, ebx
            0x00b2e0f6      mov   dword [ebp-0x04], 0x00
            0x00b2e0fd      mov   dword [ebp-0x1c], 0x01
            0x00b2e104      mov   ecx, dword [eax+0x54]
            0x00b2e107      mov   dword [ebp-0x30], ecx
            0x00b2e10a      test  ecx, ecx
        ,=< 0x00b2e10c      jz    0xb2e24d
        |   0x00b2e112      mov   edx, 0xffffffb0                      ; 4294967216
        |   0x00b2e117      add   eax, 0x50                            ; 80
        |   0x00b2e11a      mov   dword [ebp-0x18], edx
        |   0x00b2e11d      mov   dword [ebp-0x34], eax
            0x00cc0210      push  ebp
            0x00cc0211      mov   ebp, esp
            0x00cc0213      push  0xffffffff                           ; 255
            0x00cc0215      push  0x1867030
            0x00cc021a      mov   eax, dword fs:[0x0]
            0x00cc0220      push  eax
            0x00cc0221      sub   esp, 0x14
            0x00cc0224      push  ebx
            0x00cc0225      push  esi
            0x00cc0226      push  edi
            0x00cc0227      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00cc022c      xor   eax, ebp
            0x00cc022e      push  eax
            0x00cc022f      lea   eax, dword [ebp-0x0c]
            0x00cc0232      mov   dword fs:[0x0], eax
            0x00cc0238      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00cc023d      xor   edi, edi
            0x00cc023f      xor   ebx, ebx
            0x00cc0241      xor   edx, edx
            0x00cc0243      xor   esi, esi
            0x00cc0245      mov   eax, dword [eax+0x108]
            0x00cc024b      mov   dword [ebp-0x1c], edi
            0x00cc024e      mov   dword [ebp-0x18], ebx
            0x00cc0251      mov   dword [ebp-0x14], edx
            0x00cc0254      mov   ecx, dword [eax*4+0x2027ed0]
            0x00cc025b      mov   dword [ebp-0x10], esi
            0x00cc025e      mov   dword [ebp-0x20], ecx
            0x00cc0261      test  ecx, ecx
        ,=< 0x00cc0263      jz    0xcc0285
        |   0x00cc0265      mov   eax, dword [ecx]
        |   0x00cc0267      lea   edx, dword [ebp-0x14]
        |   0x00cc026a      push  edx
        |   0x00cc026b      lea   edx, dword [ebp-0x1c]
        |   0x00cc026e      push  edx
        |   0x00cc026f      call  dword [eax+0x3c]                     ; 60
        |   0x00cc0272      mov   ecx, dword [ebp-0x20]
        |   0x00cc0275      mov   esi, dword [ebp-0x10]
        |   0x00cc0278      mov   edx, dword [ebp-0x14]
        |   0x00cc027b      mov   ebx, dword [ebp-0x18]
        |   0x00cc027e      mov   edi, dword [ebp-0x1c]
        |   0x00cc0281      test  ecx, ecx
       ,==< 0x00cc0283      jnz   0xcc0289
       |`-> 0x00cc0285      xor   ecx, ecx
       |,=< 0x00cc0287      jmp   0xcc02a3
       `--> 0x00cc0289      mov   eax, dword [ebp+0x08]
        |   0x00cc028c      xor   ecx, ecx
        |   0x00cc028e      movzx eax, word [eax]
        |   0x00cc0291      cmp   eax, ebx
       ,==< 0x00cc0293      jnb   0xcc02a3
       ||   0x00cc0295      mov   ecx, dword [edi+eax*4]
       ||   0x00cc0298      test  ecx, ecx
      ,===< 0x00cc029a      jnz   0xcc02a3
      |||   0x00cc029c      cmp   eax, esi
     ,====< 0x00cc029e      jnb   0xcc02a3
     ||||   0x00cc02a0      mov   ecx, dword [edx+eax*4]
     ````-> 0x00cc02a3      test  ecx, ecx
            0x00cc02a5      setnz al
            0x00cc02a8      mov   ecx, dword [ebp-0x0c]
            0x00cc02ab      mov   dword fs:[0x0], ecx
            0x00cc02b2      pop   ecx
            0x00cc02b3      pop   edi
            0x00cc02b4      pop   esi
            0x00cc02b5      pop   ebx
            0x00cc02b6      mov   esp, ebp
            0x00cc02b8      pop   ebp
            0x00cc02b9      ret
            0x00cc02ba      int3
            0x00cc02bb      int3
            0x00cc02bc      int3
            0x00cc02bd      int3
            0x00cc02be      int3
            0x00cc02bf      int3
            0x00cc02c0      push  ebp
            0x00cc02c1      mov   ebp, esp
            0x00cc02c3      push  0xffffffff                           ; 255
            0x00cc02c5      push  0x180d4c0
            0x00cc02ca      mov   eax, dword fs:[0x0]
            0x00cc02d0      push  eax
            0x00cc02d1      sub   esp, 0x14
            0x00cc02d4      push  ebx
            0x00cc02d5      push  esi
            0x00cc02d6      push  edi
            0x00cc02d7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00cc02dc      xor   eax, ebp
            0x00cc02de      push  eax
            0x00cc02df      lea   eax, dword [ebp-0x0c]
            0x00cc02e2      mov   dword fs:[0x0], eax
            0x00cc02e8      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00cc02ed      xor   ebx, ebx
            0x00cc02ef      xor   edi, edi
            0x00cc02f1      xor   edx, edx
            0x00cc02f3      xor   esi, esi
            0x00cc02f5      mov   eax, dword [eax+0x108]
            0x00cc02fb      mov   dword [ebp-0x1c], ebx
            0x00cc02fe      mov   dword [ebp-0x18], edi
            0x00cc0301      mov   dword [ebp-0x14], edx
            0x00cc0304      mov   ecx, dword [eax*4+0x2027ed0]
            0x00cc030b      mov   dword [ebp-0x10], esi
            0x00cc030e      mov   dword [ebp-0x20], ecx
            0x00cc0311      test  ecx, ecx
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
    |||||   0x00cc034f      invalid
            0x00ca0620      push  ebp
            0x00ca0621      mov   ebp, esp
            0x00ca0623      push  0xffffffff                           ; 255
            0x00ca0625      push  0x187e788
            0x00ca062a      mov   eax, dword fs:[0x0]
            0x00ca0630      push  eax
            0x00ca0631      sub   esp, 0x20
            0x00ca0634      push  esi
            0x00ca0635      push  edi
            0x00ca0636      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00ca063b      xor   eax, ebp
            0x00ca063d      push  eax
            0x00ca063e      lea   eax, dword [ebp-0x0c]
            0x00ca0641      mov   dword fs:[0x0], eax
            0x00ca0647      mov   eax, dword [ebp+0x08]
            0x00ca064a      xor   edi, edi
            0x00ca064c      mov   dword [ebp-0x10], eax
            0x00ca064f      xor   edx, edx
            0x00ca0651      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
            0x00ca0656      xor   esi, esi
            0x00ca0658      mov   eax, dword [eax+0x1f8]
            0x00ca065e      mov   dword [ebp-0x20], edi
            0x00ca0661      mov   dword [ebp-0x1c], edi
            0x00ca0664      mov   dword [ebp-0x18], edx
            0x00ca0667      mov   ecx, dword [eax*4+0x2027ed0]
            0x00ca066e      mov   dword [ebp-0x14], esi
            0x00ca0671      mov   dword [ebp-0x24], ecx
            0x00ca0674      test  ecx, ecx
        ,=< 0x00ca0676      jz    0xca0691
        |   0x00ca0678      mov   eax, dword [ecx]
        |   0x00ca067a      lea   edx, dword [ebp-0x18]
        |   0x00ca067d      push  edx
        |   0x00ca067e      lea   edx, dword [ebp-0x20]
        |   0x00ca0681      push  edx
        |   0x00ca0682      call  dword [eax+0x3c]                     ; 60
        |   0x00ca0685      mov   esi, dword [ebp-0x14]
        |   0x00ca0688      mov   edx, dword [ebp-0x18]
        |   0x00ca068b      mov   edi, dword [ebp-0x20]
        |   0x00ca068e      mov   ecx, dword [ebp-0x24]
        `-> 0x00ca0691      mov   dword [ebp-0x04], 0x00
            0x00ca0698      test  ecx, ecx
        ,=< 0x00ca069a      jz    0xca06b7
        |   0x00ca069c      mov   eax, dword [ebp-0x10]
        |   0x00ca069f      xor   ecx, ecx
        |   0x00ca06a1      movzx eax, word [eax]
        |   0x00ca06a4      cmp   eax, dword [ebp-0x1c]
       ,==< 0x00ca06a7      jnb   0xca06b7
       ||   0x00ca06a9      mov   ecx, dword [edi+eax*4]
       ||   0x00ca06ac      test  ecx, ecx
      ,===< 0x00ca06ae      jnz   0xca06b7
      |||   0x00ca06b0      cmp   eax, esi
     ,====< 0x00ca06b2      jnb   0xca06b7
     ||||   0x00ca06b4      mov   ecx, dword [edx+eax*4]
     ````-> 0x00ca06b7      lea   eax, dword [ebp-0x2c]
            0x00ca06ba      push  eax
            0x00ca06bb      call  0x6e2140
            0x00ca06c0      mov   esi, dword [ebp-0x2c]
            0x00ca06c3      mov   eax, dword [ebp-0x28]
            0x00ca06c6      lea   edi, dword [esi+eax*4]
            0x00ca06c9      cmp   esi, edi
        ,=< 0x00ca06cb      jz    0xca073c
        |   0x00ca06cd      nop   dword [eax], eax
       .--> 0x00ca06d0      push  esi
       :|   0x00ca06d1      call  0xa95090
       :|   0x00ca06d6      mov   edx, eax
       :|   0x00ca06d8      xorps xmm0, xmm0
       :|   0x00ca06db      psrldq xmm0, 0x0c
       :|   0x00ca06e0      xorps xmm1, xmm1
       :|   0x00ca06e3      movd  ecx, xmm0
       :|   0x00ca06e7      add   esp, 0x04
       :|   0x00ca06ea      xorps xmm0, xmm0
       :|   0x00ca06ed      psrldq xmm1, 0x04
       :|   0x00ca06f2      mov   eax, dword [edx+0x0c]
       :|   0x00ca06f5      and   eax, ecx
       :|   0x00ca06f7      psrldq xmm0, 0x08
       :|   0x00ca06fc      not   ecx
       :|   0x00ca06fe      xor   eax, ecx
       :|   0x00ca0700      mov   ecx, dword [edx+0x08]
       :|   0x00ca0703      mov   dword [ebp-0x10], eax
       :|   0x00ca0706      movd  eax, xmm0
       :|   0x00ca070a      and   ecx, eax
       :|   0x00ca070c      not   eax
       :|   0x00ca070e      xor   ecx, eax
       :|   0x00ca0710      movd  eax, xmm1
       :|   0x00ca0714      and   dword [ebp-0x10], ecx
       :|   0x00ca0717      mov   ecx, dword [edx+0x04]
       :|   0x00ca071a      and   ecx, eax
       :|   0x00ca071c      not   eax
       :|   0x00ca071e      xor   ecx, eax
       :|   0x00ca0720      mov   eax, dword [edx]
       :|   0x00ca0722      and   dword [ebp-0x10], ecx
       :|   0x00ca0725      and   eax, 0x10                            ; 16
       :|   0x00ca0728      mov   ecx, dword [ebp-0x10]
       :|   0x00ca072b      xor   eax, 0xffffffef                      ; 4294967279
       :|   0x00ca072e      and   ecx, eax
       :|   0x00ca0730      cmp   ecx, 0xffffffff                      ; -1
      ,===< 0x00ca0733      jz    0xca074f
      |:|   0x00ca0735      add   esi, 0x04
      |:|   0x00ca0738      cmp   esi, edi
      |`==< 0x00ca073a      jnz   0xca06d0
      | `-> 0x00ca073c      mov   al, 0x01
      |     0x00ca073e      mov   ecx, dword [ebp-0x0c]
      |     0x00ca0741      mov   dword fs:[0x0], ecx
      |     0x00ca0748      pop   ecx
      |     0x00ca0749      pop   edi
      |     0x00ca074a      pop   esi
      |     0x00ca074b      mov   esp, ebp
      |     0x00ca074d      pop   ebp
      |     0x00ca074e      ret
      `---> 0x00ca074f      xor   al, al
            0x00ca0751      mov   ecx, dword [ebp-0x0c]
            0x00ca0754      mov   dword fs:[0x0], ecx
            0x00ca075b      pop   ecx
            0x00ca075c      pop   edi
            0x00ca075d      pop   esi
            0x00ca075e      mov   esp, ebp
            0x00ca0760      pop   ebp
            0x00ca0761      ret
            0x00ca0762      int3
            0x00ca0763      int3
            0x00ca0764      int3
            0x00ca0765      int3
            0x00ca0766      int3
            0x00ca0767      int3
            0x00ca0768      int3
            0x00ca0769      int3
            0x00ca076a      int3
            0x00ca076b      int3
            0x00ca076c      int3
            0x00ca076d      int3
            0x00ca076e      int3
            0x00ca076f      int3
            0x00ca0770      push  ebx
            0x00ca0771      mov   ebx, esp
            0x00ca0773      sub   esp, 0x08
            0x00ca0776      and   esp, 0xfffffff0
            0x00ca0779      add   esp, 0x04
            0x00ca077c      push  ebp
            0x00ca077d      mov   ebp, dword [ebx+0x04]
            0x00ca0780      mov   dword [esp+0x04], ebp
            0x00ca0784      mov   ebp, esp
            0x00ca0786      push  0xffffffff                           ; 255
            0x00ca0788      push  0x187e7b8
            0x00ca078d      mov   eax, dword fs:[0x0]
            0x00ca0793      push  eax
            0x00ca0794      push  ebx
            0x00ca0795      sub   esp, 0x88
            0x00ca079b      push  esi
            0x00ca079c      push  edi
            0x00ca079d      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00ca07a2      xor   eax, ebp
            0x00ca07a4      push  eax
            0x00ca07a5      lea   eax, dword [ebp-0x0c]
            0x00ca07a8      mov   dword fs:[0x0], eax
            0x00ca07ae      mov   edi, ecx
            0x00ca07b0      mov   eax, dword [ebx+0x0c]
            0x00ca07b3      mov   dword [ebp-0x18], eax
            0x00ca07b6      mov   eax, dword [ebx+0x10]
            0x00ca07b9      mov   dword [ebp-0x1c], eax
            0x00ca07bc      call  0xbb1330
            0x00ca07c1      mov   esi, dword [ebx+0x14]
            0x00ca07c4      fstp  dword [ebp-0x14]
            0x00ca07c7      test  byte [esi+0x50], 0x01
        ,=< 0x00ca07cb      jz    0xca0822
        |   0x00ca07cd      lea   eax, dword [ebp-0x20]
        |   0x00ca07d0      push  eax
        |   0x00ca07d1      call  0xb167c0
        |   0x00ca07d6      mov   ecx, dword [ebp-0x1c]
        |   0x00ca07d9      add   esp, 0x04
        |   0x00ca07dc      push  eax
        |   0x00ca07dd      call  0xafd2b0
        |   0x00ca07e2      mov   ecx, dword [esi+0x5c]
        |   0x00ca07e5      movss xmm1, dword [ebp-0x14]
        |   0x00ca07ea      cmp   ecx, dword [edi+0x1fc]
       ,==< 0x00ca07f0      jz    0xca0806
       ||   0x00ca07f2      movss xmm0, dword [edi+0x200]
       ||   0x00ca07fa      comiss xmm0, xmm1
      ,===< 0x00ca07fd      jbe   0xca0806
      |||   0x00ca07ff      fldz
     ,====< 0x00ca0801      jmp   0xca0c21
     |``--> 0x00ca0806      movss xmm0, dword [eax+0x34]
     |  |   0x00ca080b      addss xmm0, xmm1
     |  |   0x00ca080f      movss dword [edi+0x200], xmm0
     |  |   0x00ca0817      mov   eax, dword [esi+0x5c]
     |  |   0x00ca081a      mov   dword [edi+0x1fc], eax
            0x004f7950      mov   eax, dword [esp+0x04]
            0x004f7954      mov   dword [ecx], eax
            0x004f7956      mov   eax, ecx
            0x004f7958      ret   0x08
            0x004f795b      int3
            0x004f795c      int3
            0x004f795d      int3
            0x004f795e      int3
            0x004f795f      int3
            0x004f7960      cmp   byte [esp+0x08], 0x00
            0x004f7965      mov   eax, dword [esp+0x04]
            0x004f7969      mov   dword [ecx], eax
        ,=< 0x004f796b      jz    0x4f7974
        |   0x004f796d      or    eax, 0x80000000
        |   0x004f7972      mov   dword [ecx], eax
        `-> 0x004f7974      cmp   byte [esp+0x0c], 0x00
        ,=< 0x004f7979      jz    0x4f7982
        |   0x004f797b      or    eax, 0x40000000
        |   0x004f7980      mov   dword [ecx], eax
        `-> 0x004f7982      mov   eax, ecx
            0x004f7984      ret   0x10
            0x004f7987      int3
            0x004f7988      int3
            0x004f7989      int3
            0x004f798a      int3
            0x004f798b      int3
            0x004f798c      int3
            0x004f798d      int3
            0x004f798e      int3
            0x004f798f      int3
            0x004f7990      mov   dword [ecx], 0x1931fc0               ; [0x1931fc0:4]=0x5013d0
            0x004f7996      mov   eax, ecx
            0x004f7998      mov   dword [ecx+0x04], 0x00
            0x004f799f      ret
            0x004f79a0      push  ebp
            0x004f79a1      mov   ebp, esp
            0x004f79a3      push  0xffffffff                           ; 255
            0x004f79a5      push  0x180c717
            0x004f79aa      mov   eax, dword fs:[0x0]
            0x004f79b0      push  eax
            0x004f79b1      sub   esp, 0x08
            0x004f79b4      push  ebx
            0x004f79b5      push  esi
            0x004f79b6      push  edi
            0x004f79b7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x004f79bc      xor   eax, ebp
            0x004f79be      push  eax
            0x004f79bf      lea   eax, dword [ebp-0x0c]
            0x004f79c2      mov   dword fs:[0x0], eax
            0x004f79c8      mov   ebx, ecx
            0x004f79ca      cmp   dword [0x1fd0220], 0x02              ; [0x1fd0220:4]=0
        ,=< 0x004f79d1      jz    0x4f7a30
        |   0x004f79d3      mov   edx, 0x01
        |   0x004f79d8      mov   esi, 0x1fd0220
        |   0x004f79dd      xor   eax, eax
        |   0x004f79df      lock  cmpxchg dword [esi], edx
        |   0x004f79e3      test  eax, eax
       ,==< 0x004f79e5      jnz   0x4f7a1c
       ||   0x004f79e7      mov   eax, dword fs:[0x2c]
       ||   0x004f79ed      mov   ecx, dword [0x218e080]               ; [0x218e080:4]=0
       ||   0x004f79f3      mov   ecx, dword [eax+ecx*4]
       ||   0x004f79f6      mov   eax, dword [0x1fd0228]               ; [0x1fd0228:4]=0
       ||   0x004f79fb      cmp   eax, dword [ecx+0x04]
      ,===< 0x004f7a01      jnle  0x4f7afb
      |||   0x004f7a07      mov   eax, 0x1fd0224
      |||   0x004f7a0c      mov   ecx, 0x1fd021c
      |||   0x004f7a11      xchg  dword [ecx], eax
      |||   0x004f7a13      mov   eax, 0x02
      |||   0x004f7a18      xchg  dword [esi], eax
     ,====< 0x004f7a1a      jmp   0x4f7a30
     ||`--> 0x004f7a1c      cmp   dword [0x1fd0220], 0x02              ; [0x1fd0220:4]=0
     ||,==< 0x004f7a23      jz    0x4f7a30
    .-----> 0x004f7a25      pause
    :||||   0x004f7a27      cmp   dword [0x1fd0220], 0x02              ; [0x1fd0220:4]=0
    `=====< 0x004f7a2e      jnz   0x4f7a25
     `-``-> 0x004f7a30      mov   eax, dword [0x1fd021c]               ; [0x1fd021c:4]=0
      |     0x004f7a35      push  dword [0x1fcf4dc]
      |     0x004f7a3b      mov   dword [ebp-0x10], eax
      |     0x004f7a3e      mov   edi, dword [eax]
      |     0x004f7a40      call  dword [sym.imp.KERNEL32.dll_TlsGetValue] ; 0x1914284 ; LPVOID TlsGetValue(DWORD dwTlsIndex)
      |     0x004f7a46      mov   esi, eax
      |     0x004f7a48      cmp   edi, dword [esi+0x100]
      | ,=< 0x004f7a4e      jb    0x4f7a5c
      | |   0x004f7a50      push  edi
      | |   0x004f7a51      push  esi
      | |   0x004f7a52      mov   ecx, 0x1fcf4c8
      | |   0x004f7a57      call  0x50fb00
      | `-> 0x004f7a5c      mov   edi, dword [esi+edi*4]
      |     0x004f7a5f      invalid
