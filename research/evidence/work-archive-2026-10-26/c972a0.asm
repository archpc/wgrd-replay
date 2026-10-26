0x00c972a0      push  ebp
            0x00c972a1      mov   ebp, esp
            0x00c972a3      push  0xffffffff                           ; 255
            0x00c972a5      push  0x187e0fc
            0x00c972aa      mov   eax, dword fs:[0x0]
            0x00c972b0      push  eax
            0x00c972b1      sub   esp, 0x244
            0x00c972b7      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c972bc      xor   eax, ebp
            0x00c972be      mov   dword [ebp-0x10], eax
            0x00c972c1      push  esi
            0x00c972c2      push  edi
            0x00c972c3      push  eax
            0x00c972c4      lea   eax, dword [ebp-0x0c]
            0x00c972c7      mov   dword fs:[0x0], eax
            0x00c972cd      mov   eax, dword [ebp+0x08]
            0x00c972d0      mov   edx, dword [0x201f660]               ; [0x201f660:4]=0
            0x00c972d6      mov   edi, dword [ebp+0x14]
            0x00c972d9      mov   esi, dword [ebp+0x1c]
            0x00c972dc      mov   dword [ebp-0xa0], eax
            0x00c972e2      mov   eax, dword [ebp+0x0c]
            0x00c972e5      mov   dword [ebp-0xf0], eax
            0x00c972eb      mov   eax, dword [ebp+0x18]
            0x00c972ee      mov   dword [ebp-0xb4], eax
            0x00c972f4      mov   eax, dword [0x201e2dc]               ; [0x201e2dc:4]=0
            0x00c972f9      mov   dword [ebp-0xe0], eax
            0x00c972ff      mov   eax, dword [edx+0x1f8]
            0x00c97305      mov   dword [ebp-0xc0], edi
            0x00c9730b      mov   dword [ebp-0xcc], esi
            0x00c97311      mov   dword [ebp-0x110], 0x00
            0x00c9731b      mov   ecx, dword [eax*4+0x2027ed0]
            0x00c97322      mov   dword [ebp-0x10c], 0x00
            0x00c9732c      mov   dword [ebp-0x108], 0x00
            0x00c97336      mov   dword [ebp-0x104], 0x00
            0x00c97340      mov   dword [ebp-0x114], ecx
            0x00c97346      test  ecx, ecx
        ,=< 0x00c97348      jz    0xc97363
        |   0x00c9734a      mov   eax, dword [ecx]
        |   0x00c9734c      lea   edx, dword [ebp-0x108]
        |   0x00c97352      push  edx
        |   0x00c97353      lea   edx, dword [ebp-0x110]
        |   0x00c97359      push  edx
        |   0x00c9735a      call  dword [eax+0x3c]                     ; 60
        |   0x00c9735d      mov   edx, dword [0x201f660]               ; [0x201f660:4]=0
        `-> 0x00c97363      mov   eax, dword [edx+0x1f8]
            0x00c97369      mov   dword [ebp-0x04], 0x00
            0x00c97370      mov   dword [ebp-0x1d4], 0x00
            0x00c9737a      mov   dword [ebp-0x1d0], 0x00
            0x00c97384      mov   ecx, dword [eax*4+0x2027ed0]
            0x00c9738b      mov   dword [ebp-0x1d8], ecx
            0x00c97391      test  ecx, ecx
        ,=< 0x00c97393      jz    0xc973a9
        |   0x00c97395      mov   eax, dword [ecx]
        |   0x00c97397      lea   edx, dword [ebp-0x1d4]
        |   0x00c9739d      push  0x00
        |   0x00c9739f      push  edx
        |   0x00c973a0      call  dword [eax+0x3c]                     ; 60
        |   0x00c973a3      mov   edx, dword [0x201f660]               ; [0x201f660:4]=0
        `-> 0x00c973a9      mov   eax, dword [edx+0x1f8]
            0x00c973af      mov   byte [ebp-0x04], 0x01
            0x00c973b3      mov   dword [ebp-0x144], 0x00
            0x00c973bd      mov   dword [ebp-0x140], 0x00
            0x00c973c7      mov   ecx, dword [eax*4+0x2027ed0]
            0x00c973ce      mov   dword [ebp-0x148], ecx
            0x00c973d4      test  ecx, ecx
        ,=< 0x00c973d6      jz    0xc973e6
        |   0x00c973d8      mov   eax, dword [ecx]
        |   0x00c973da      lea   edx, dword [ebp-0x144]
        |   0x00c973e0      push  edx
        |   0x00c973e1      push  0x00
        |   0x00c973e3      call  dword [eax+0x3c]                     ; 60
        `-> 0x00c973e6      cmp   dword [ebp+0x24], 0x02
            0x00c973ea      mov   al, byte [esi+0x21]
            0x00c973ed      mov   cl, byte [esi+0x20]
            0x00c973f0      mov   byte [ebp-0x04], 0x02
            0x00c973f4      mov   byte [ebp-0xd5], al
            0x00c973fa      mov   byte [ebp-0xd6], cl
        ,=< 0x00c97400      jz    0xc9740d
        |   0x00c97402      mov   byte [ebp-0xda], 0x01
        |   0x00c97409      test  al, al
       ,==< 0x00c9740b      jz    0xc97414
       |`-> 0x00c9740d      mov   byte [ebp-0xda], 0x00
       `--> 0x00c97414      cmp   dword [esi+0x10], 0x0e
        ,=< 0x00c97418      jz    0xc97437
        |   0x00c9741a      mov   esi, dword [esi+0x14]
        |   0x00c9741d      lea   eax, dword [ebp-0x120]
        |   0x00c97423      push  eax
        |   0x00c97424      call  0xb73ce0
        |   0x00c97429      add   esp, 0x04
        |   0x00c9742c      mov   byte [ebp-0x99], 0x00
        |   0x00c97433      cmp   esi, dword [eax]
       ,==< 0x00c97435      jnz   0xc9743e
       |`-> 0x00c97437      mov   byte [ebp-0x99], 0x01
       `--> 0x00c9743e      lea   ecx, dword [ebp-0xac]
            0x00c97444      call  0x4f6c50
            0x00c97449      xor   eax, eax
            0x00c9744b      mov   byte [ebp-0x04], 0x03
            0x00c9744f      mov   dword [ebp-0xc8], eax
            0x00c97455      mov   dword [ebp-0xf4], eax
            0x00c9745b      mov   dword [ebp-0xe4], eax
            0x00c97461      mov   byte [ebp-0xae], al
            0x00c97467      mov   byte [ebp-0xb9], al
            0x00c9746d      mov   byte [ebp-0xa1], al
            0x00c97473      mov   byte [ebp-0xad], al
            0x00c97479      cmp   dword [edi+0x04], eax
        ,=< 0x00c9747c      jz    0xc975e1
        |   0x00c97482      mov   eax, dword [edi]
        |   0x00c97484      mov   eax, dword [eax]
        |   0x00c97486      mov   dword [ebp-0xac], eax
        |   0x00c9748c      cmp   eax, 0xffffffff                      ; -1
       ,==< 0x00c9748f      jz    0xc975e1
       ||   0x00c97495      lea   eax, dword [ebp-0xac]
       ||   0x00c9749b      push  eax
       ||   0x00c9749c      call  0xb9d4b0
       ||   0x00c974a1      mov   ecx, dword [ebp-0xac]
       ||   0x00c974a7      add   esp, 0x04
       ||   0x00c974aa      cmp   dword [ebp-0x114], 0x00
       ||   0x00c974b1      mov   dword [ebp-0xc8], eax
      ,===< 0x00c974b7      jnz   0xc974bd
      |||   0x00c974b9      xor   edi, edi
     ,====< 0x00c974bb      jmp   0xc974f4
     |`---> 0x00c974bd      xor   edi, edi
     | ||   0x00c974bf      movzx edx, cx
     | ||   0x00c974c2      mov   dword [ebp-0xe4], edi
     | ||   0x00c974c8      cmp   edx, dword [ebp-0x10c]
     |,===< 0x00c974ce      jnb   0xc974fa
     ||||   0x00c974d0      mov   eax, dword [ebp-0x110]
     ||||   0x00c974d6      mov   edi, dword [eax+edx*4]
     ||||   0x00c974d9      mov   dword [ebp-0xe4], edi
     ||||   0x00c974df      test  edi, edi
    ,=====< 0x00c974e1      jnz   0xc974fa
    |||||   0x00c974e3      cmp   edx, dword [ebp-0x104]
   ,======< 0x00c974e9      jnb   0xc974fa
   ||||||   0x00c974eb      mov   eax, dword [ebp-0x108]
   ||||||   0x00c974f1      mov   edi, dword [eax+edx*4]
   ||`----> 0x00c974f4      mov   dword [ebp-0xe4], edi
   ``-`---> 0x00c974fa      cmp   dword [ebp-0x148], 0x00
      ,===< 0x00c97501      jz    0xc97519
      |||   0x00c97503      movzx esi, cx
      |||   0x00c97506      cmp   esi, dword [ebp-0x140]
     ,====< 0x00c9750c      jnb   0xc97519
     ||||   0x00c9750e      mov   eax, dword [ebp-0x144]
     ||||   0x00c97514      mov   esi, dword [eax+esi*4]
    ,=====< 0x00c97517      jmp   0xc9751b
    |``---> 0x00c97519      xor   esi, esi
    `-----> 0x00c9751b      test  edi, edi
       ||   0x00c9751d      setnz byte [ebp-0xa1]
       ||   0x00c97524      test  edi, edi
      ,===< 0x00c97526      jz    0xc975bb
      |||   0x00c9752c      lea   eax, dword [ebp-0x1bc]
      |||   0x00c97532      mov   ecx, edi
      |||   0x00c97534      push  eax
      |||   0x00c97535      call  0xdb1640
      |||   0x00c9753a      mov   ecx, eax
      |||   0x00c9753c      mov   byte [ebp-0x04], 0x04
      |||   0x00c97540      call  0xb014f0
      |||   0x00c97545      lea   ecx, dword [ebp-0x1bc]
      |||   0x00c9754b      mov   dword [ebp-0xf4], eax
      |||   0x00c97551      mov   byte [ebp-0x04], 0x03
      |||   0x00c97555      call  0x4dc500
      |||   0x00c9755a      lea   eax, dword [ebp-0xd4]
      |||   0x00c97560      mov   ecx, edi
      |||   0x00c97562      push  eax
      |||   0x00c97563      call  0xdb1640
      |||   0x00c97568      push  eax
      |||   0x00c97569      mov   byte [ebp-0x04], 0x05
      |||   0x00c9756d      call  0xdb1580
      |||   0x00c97572      add   esp, 0x04
      |||   0x00c97575      mov   byte [ebp-0xad], al
      |||   0x00c9757b      lea   ecx, dword [ebp-0xd4]
      |||   0x00c97581      mov   byte [ebp-0x04], 0x03
      |||   0x00c97585      call  0x4dc500
      |||   0x00c9758a      test  esi, esi
     ,====< 0x00c9758c      jz    0xc975e1
     ||||   0x00c9758e      cmp   byte [ebp-0x99], 0x00
     ||||   0x00c97595      mov   cl, byte [ebp-0xad]
     ||||   0x00c9759b      mov   edx, dword [ebp-0xf4]
     ||||   0x00c975a1      mov   dword [ebp-0xf4], edx
     ||||   0x00c975a7      mov   byte [ebp-0xad], cl
    ,=====< 0x00c975ad      jnz   0xc975e1
    |||||   0x00c975af      mov   byte [ebp-0x99], 0x01
   ,======< 0x00c975b6      jmp   0xc9a109
   |||`---> 0x00c975bb      lea   ecx, dword [ebp-0xac]
   ||| ||   0x00c975c1      call  0xb014f0
   ||| ||   0x00c975c6      mov   dword [ebp-0xf4], eax
   ||| ||   0x00c975cc      lea   eax, dword [ebp-0xac]
   ||| ||   0x00c975d2      push  eax
   ||| ||   0x00c975d3      call  0xdb1580
   ||| ||   0x00c975d8      add   esp, 0x04
   ||| ||   0x00c975db      mov   byte [ebp-0xad], al
   |``-``-> 0x00c975e1      mov   edi, dword [ebp+0x10]
   |        0x00c975e4      mov   eax, dword [edi+0x04]
   |        0x00c975e7      mov   dword [ebp-0xd4], eax
   |        0x00c975ed      lea   esi, dword [eax*4]
   |        0x00c975f4      lea   eax, dword [esi+0x0f]
   |        0x00c975f7      cmp   eax, 0x4020                          ; ' @'
   |    ,=< 0x00c975fc      jnbe  0xc97607
   |    |   0x00c975fe      call  0x18076c0
   |    |   0x00c97603      mov   eax, esp
   |   ,==< 0x00c97605      jmp   0xc97609
   |   |`-> 0x00c97607      xor   eax, eax
   |   `--> 0x00c97609      add   eax, 0x0f                            ; 0xf ; 15
   |        0x00c9760c      lea   ecx, dword [ebp-0x13c]
   |        0x00c97612      and   eax, 0xfffffff0                      ; 4294967280
   |        0x00c97615      push  esi
   |        0x00c97616      push  eax
   |        0x00c97617      mov   dword [ebp-0x134], eax
   |        0x00c9761d      call  0x4ea610
   |        0x00c97622      mov   eax, dword [ebp-0xd4]
   |        0x00c97628      mov   dword [ebp-0x130], 0x00
   |        0x00c97632      mov   dword [ebp-0x12c], eax
   |        0x00c97638      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
   |        0x00c9763d      mov   byte [ebp-0x04], 0x09
   |        0x00c97641      mov   eax, dword [eax+0x108]
   |        0x00c97647      mov   dword [ebp-0x174], 0x00
   |        0x00c97651      mov   dword [ebp-0x170], 0x00
   |        0x00c9765b      mov   dword [ebp-0x16c], 0x00
   |        0x00c97665      mov   ecx, dword [eax*4+0x2027ed0]
   |        0x00c9766c      mov   dword [ebp-0x168], 0x00
   |        0x00c97676      mov   dword [ebp-0x178], ecx
   |        0x00c9767c      test  ecx, ecx
   |    ,=< 0x00c9767e      jz    0xc97693
   |    |   0x00c97680      mov   eax, dword [ecx]
   |    |   0x00c97682      lea   edx, dword [ebp-0x16c]
   |    |   0x00c97688      push  edx
   |    |   0x00c97689      lea   edx, dword [ebp-0x174]
   |    |   0x00c9768f      push  edx
   |    |   0x00c97690      call  dword [eax+0x3c]                     ; 60
   |    `-> 0x00c97693      mov   esi, dword [edi]
   |        0x00c97695      mov   eax, dword [edi+0x04]
   |        0x00c97698      mov   byte [ebp-0x04], 0x0a
   |        0x00c9769c      lea   edi, dword [esi+eax*4]
   |        0x00c9769f      cmp   esi, edi
   |    ,=< 0x00c976a1      jz    0xc977af
   |    |   0x00c976a7      nop   word [eax+eax*1], ax
   |   .--> 0x00c976b0      cmp   dword [ebp-0x114], 0x00
   |  ,===< 0x00c976b7      jz    0xc97762
   |  |:|   0x00c976bd      mov   edx, dword [esi]
   |  |:|   0x00c976bf      and   edx, 0xffff
   |  |:|   0x00c976c5      cmp   edx, dword [ebp-0x10c]
   | ,====< 0x00c976cb      jnb   0xc97762
   | ||:|   0x00c976d1      mov   eax, dword [ebp-0x110]
   | ||:|   0x00c976d7      mov   ecx, dword [eax+edx*4]
   | ||:|   0x00c976da      test  ecx, ecx
   |,=====< 0x00c976dc      jnz   0xc976f3
   ||||:|   0x00c976de      cmp   edx, dword [ebp-0x104]
  ,=======< 0x00c976e4      jnb   0xc97762
  |||||:|   0x00c976e6      mov   eax, dword [ebp-0x108]
  |||||:|   0x00c976ec      mov   ecx, dword [eax+edx*4]
  |||||:|   0x00c976ef      test  ecx, ecx
  ========< 0x00c976f1      jz    0xc97762
  ||`-----> 0x00c976f3      cmp   dword [ebp-0x178], 0x00
  ||,=====< 0x00c976fa      jz    0xc9772c
  |||||:|   0x00c976fc      cmp   edx, dword [ebp-0x170]
  ========< 0x00c97702      jnb   0xc9772c
  |||||:|   0x00c97704      mov   eax, dword [ebp-0x174]
  |||||:|   0x00c9770a      mov   eax, dword [eax+edx*4]
  |||||:|   0x00c9770d      test  eax, eax
  ========< 0x00c9770f      jnz   0xc97726
  |||||:|   0x00c97711      cmp   edx, dword [ebp-0x168]
  ========< 0x00c97717      jnb   0xc9772c
  |||||:|   0x00c97719      mov   eax, dword [ebp-0x16c]
  |||||:|   0x00c9771f      mov   eax, dword [eax+edx*4]
  |||||:|   0x00c97722      test  eax, eax
  ========< 0x00c97724      jz    0xc9772c
  --------> 0x00c97726      cmp   dword [eax+0x24], 0x05
  ========< 0x00c9772a      jnz   0xc977a4
  --`-----> 0x00c9772c      call  0xda9b90
  || ||:|   0x00c97731      test  al, al
  ||,=====< 0x00c97733      jz    0xc97742
  |||||:|   0x00c97735      mov   eax, dword [ebp-0xcc]
  |||||:|   0x00c9773b      mov   al, byte [eax+0x20]
  |||||:|   0x00c9773e      test  al, al
  ========< 0x00c97740      jz    0xc977a4
  ||`-----> 0x00c97742      mov   edx, dword [ebp-0x130]
  || ||:|   0x00c97748      mov   ecx, dword [ebp-0x134]
  || ||:|   0x00c9774e      mov   dword [ecx+edx*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  || ||:|   0x00c97755      mov   eax, dword [esi]
  || ||:|   0x00c97757      mov   dword [ecx+edx*4], eax
  || ||:|   0x00c9775a      inc   dword [ebp-0x130]
  ||,=====< 0x00c97760      jmp   0xc977a4
  `--``---> 0x00c97762      mov   eax, dword [ebp-0xf0]
   ||  :|   0x00c97768      mov   edx, dword [eax+0x10]
   ||  :|   0x00c9776b      mov   dword [ebp-0xd4], edx
   ||  :|   0x00c97771      cmp   edx, dword [eax+0x04]
   || ,===< 0x00c97774      jnz   0xc97789
   || |:|   0x00c97776      mov   ecx, eax
   || |:|   0x00c97778      call  0x7aab00
   || |:|   0x00c9777d      mov   edx, dword [ebp-0xd4]
   || |:|   0x00c97783      mov   eax, dword [ebp-0xf0]
   || `---> 0x00c97789      mov   ecx, dword [eax+0x0c]
   ||  :|   0x00c9778c      mov   dword [ecx+edx*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
   ||  :|   0x00c97793      mov   eax, dword [esi]
   ||  :|   0x00c97795      mov   dword [ecx+edx*4], eax
   ||  :|   0x00c97798      lea   eax, dword [edx+0x01]
   ||  :|   0x00c9779b      mov   ecx, dword [ebp-0xf0]
   ||  :|   0x00c977a1      mov   dword [ecx+0x10], eax
  --`-----> 0x00c977a4      add   esi, 0x04
   |   :|   0x00c977a7      cmp   esi, edi
   |   `==< 0x00c977a9      jnz   0xc976b0
   |    `-> 0x00c977af      cmp   dword [ebp-0x130], 0x00
   |        0x00c977b6      mov   byte [ebp-0x04], 0x09
   |    ,=< 0x00c977ba      jz    0xc9a0ed
   |    |   0x00c977c0      lea   ecx, dword [ebp-0xec]
   |    |   0x00c977c6      call  0x4f6c50
   |    |   0x00c977cb      mov   eax, dword [ebp-0x134]
   |    |   0x00c977d1      lea   ecx, dword [ebp-0xec]
   |    |   0x00c977d7      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
   |    |   0x00c977db      mov   eax, dword [eax]
   |    |   0x00c977dd      mov   dword [ebp-0xec], eax
   |    |   0x00c977e3      call  0xb01530
   |    |   0x00c977e8      mov   ecx, dword [ebp-0xe0]
   |    |   0x00c977ee      push  dword [eax+0x3c]
   |    |   0x00c977f1      call  0xbb2190
   |    |   0x00c977f6      mov   ecx, eax
   |    |   0x00c977f8      mov   eax, dword [ebp-0xc8]
   |    |   0x00c977fe      mov   dword [ebp-0xe8], ecx
   |    |   0x00c97804      test  eax, eax
   |   ,==< 0x00c97806      jz    0xc97823
   |   ||   0x00c97808      cmp   ecx, eax
   |   ||   0x00c9780a      push  eax
   |   ||   0x00c9780b      push  ecx
   |   ||   0x00c9780c      setz  byte [ebp-0xae]
   |   ||   0x00c97813      call  0xb3aec0
   |   ||   0x00c97818      add   esp, 0x08
   |   ||   0x00c9781b      mov   byte [ebp-0xb9], al
   |  ,===< 0x00c97821      jmp   0xc97829
   |  |`--> 0x00c97823      mov   al, byte [ebp-0xb9]
   |  `---> 0x00c97829      cmp   byte [ebp-0xad], 0x00
   |   ,==< 0x00c97830      jz    0xc97856
   |   ||   0x00c97832      cmp   byte [ebp-0xae], 0x00
   |  ,===< 0x00c97839      jnz   0xc9783f
   |  |||   0x00c9783b      test  al, al
   | ,====< 0x00c9783d      jz    0xc97856
   | |`---> 0x00c9783f      lea   ecx, dword [ebp-0xec]
   | | ||   0x00c97845      call  0x4dc500
   | | ||   0x00c9784a      mov   byte [ebp-0x99], 0x01
   | |,===< 0x00c97851      jmp   0xc9a0fe
   | `-`--> 0x00c97856      mov   eax, dword [ebp-0x130]
   |  | |   0x00c9785c      xor   ecx, ecx
   |  | |   0x00c9785e      mov   byte [ebp-0x100], 0x01
   |  | |   0x00c97865      mov   dword [ebp-0xc8], ecx
   |  | |   0x00c9786b      test  eax, eax
   |  |,==< 0x00c9786d      jz    0xc97a8f
   |  |||   0x00c97873      nop   dword [eax], eax
   |  |||   0x00c97877      nop   word [eax+eax*1], ax
   | .----> 0x00c97880      mov   eax, dword [ebp-0x134]
   | :|||   0x00c97886      mov   dword [ebp-0xc4], 0xffffffff         ; -1
   | :|||   0x00c97890      mov   eax, dword [eax+ecx*4]
   | :|||   0x00c97893      mov   dword [ebp-0xc4], eax
   | :|||   0x00c97899      xor   ecx, ecx
   | :|||   0x00c9789b      mov   byte [ebp-0x04], 0x10                ; 16
   | :|||   0x00c9789f      cmp   dword [ebp-0x114], ecx
   |,=====< 0x00c978a5      jz    0xc978d0
   ||:|||   0x00c978a7      movzx edx, ax
   ||:|||   0x00c978aa      cmp   edx, dword [ebp-0x10c]
  ,=======< 0x00c978b0      jnb   0xc978d0
  |||:|||   0x00c978b2      mov   eax, dword [ebp-0x110]
  |||:|||   0x00c978b8      mov   ecx, dword [eax+edx*4]
  |||:|||   0x00c978bb      test  ecx, ecx
  ========< 0x00c978bd      jnz   0xc978d0
  |||:|||   0x00c978bf      cmp   edx, dword [ebp-0x104]
  ========< 0x00c978c5      jnb   0xc978d0
  |||:|||   0x00c978c7      mov   eax, dword [ebp-0x108]
  |||:|||   0x00c978cd      mov   ecx, dword [eax+edx*4]
  `-`-----> 0x00c978d0      lea   eax, dword [ebp-0x1a4]
   | :|||   0x00c978d6      push  eax
   | :|||   0x00c978d7      call  0x6e2140
   | :|||   0x00c978dc      mov   edx, dword [0x201f660]               ; [0x201f660:4]=0
   | :|||   0x00c978e2      mov   eax, dword [edx+0x1f4]
   | :|||   0x00c978e8      mov   dword [ebp-0x154], 0x00
   | :|||   0x00c978f2      mov   dword [ebp-0x150], 0x00
   | :|||   0x00c978fc      mov   ecx, dword [eax*4+0x2027ed0]
   | :|||   0x00c97903      mov   dword [ebp-0x158], ecx
   | :|||   0x00c97909      test  ecx, ecx
   |,=====< 0x00c9790b      jz    0xc97921
   ||:|||   0x00c9790d      mov   eax, dword [ecx]
   ||:|||   0x00c9790f      lea   edx, dword [ebp-0x154]
   ||:|||   0x00c97915      push  0x00
   ||:|||   0x00c97917      push  edx
   ||:|||   0x00c97918      call  dword [eax+0x3c]                     ; 60
   ||:|||   0x00c9791b      mov   edx, dword [0x201f660]               ; [0x201f660:4]=0
   |`-----> 0x00c97921      mov   eax, dword [edx+0x1ec]
   | :|||   0x00c97927      mov   byte [ebp-0x04], 0x11                ; 17
   | :|||   0x00c9792b      mov   dword [ebp-0x160], 0x00
   | :|||   0x00c97935      mov   dword [ebp-0x15c], 0x00
   | :|||   0x00c9793f      mov   ecx, dword [eax*4+0x2027ed0]
   | :|||   0x00c97946      mov   dword [ebp-0x164], ecx
   | :|||   0x00c9794c      test  ecx, ecx
   |,=====< 0x00c9794e      jz    0xc9795e
   ||:|||   0x00c97950      mov   eax, dword [ecx]
   ||:|||   0x00c97952      lea   edx, dword [ebp-0x160]
   ||:|||   0x00c97958      push  0x00
   ||:|||   0x00c9795a      push  edx
   ||:|||   0x00c9795b      call  dword [eax+0x3c]                     ; 60
   |`-----> 0x00c9795e      lea   eax, dword [ebp-0xc4]
   | :|||   0x00c97964      mov   byte [ebp-0x04], 0x12                ; 18
   | :|||   0x00c97968      push  eax
   | :|||   0x00c97969      mov   byte [ebp-0xd0], 0x01
   | :|||   0x00c97970      mov   byte [ebp-0x100], 0x01
   | :|||   0x00c97977      call  0xd9dbb0
   | :|||   0x00c9797c      add   esp, 0x04
   | :|||   0x00c9797f      test  al, al
   |,=====< 0x00c97981      jnz   0xc97992
   ||:|||   0x00c97983      mov   byte [ebp-0x99], 0x01
   ||:|||   0x00c9798a      cmp   byte [ebp-0xad], al
  ,=======< 0x00c97990      jz    0xc97999
  ||`-----> 0x00c97992      mov   byte [ebp-0x99], 0x00
  `-------> 0x00c97999      mov   edi, dword [ebp-0x1a0]
   | :|||   0x00c9799f      xor   edx, edx
   | :|||   0x00c979a1      mov   ecx, dword [ebp-0x100]
   | :|||   0x00c979a7      test  edi, edi
   |,=====< 0x00c979a9      jz    0xc97a3f
   ||:|||   0x00c979af      mov   esi, dword [ebp-0x1a4]
   ||:|||   0x00c979b5      nop   word [eax+eax*1], ax
  .-------> 0x00c979c0      cmp   dword [ebp-0x158], 0x00
  :||:|||   0x00c979c7      mov   al, byte [ebp-0xd0]
  :||:|||   0x00c979cd      mov   byte [ebp-0x9a], cl
  ========< 0x00c979d3      jz    0xc979f2
  :||:|||   0x00c979d5      movzx ecx, word [esi+edx*4]
  :||:|||   0x00c979d9      cmp   ecx, dword [ebp-0x150]
  ========< 0x00c979df      jnb   0xc979f2
  :||:|||   0x00c979e1      mov   edi, dword [ebp-0x154]
  :||:|||   0x00c979e7      mov   ecx, dword [edi+ecx*4]
  :||:|||   0x00c979ea      mov   edi, dword [ebp-0x1a0]
  ========< 0x00c979f0      jmp   0xc979f4
  --------> 0x00c979f2      xor   ecx, ecx
  --------> 0x00c979f4      test  ecx, ecx
  :||:|||   0x00c979f6      movzx eax, al
  :||:|||   0x00c979f9      mov   ecx, 0x00
  :||:|||   0x00c979fe      cmovnz ecx, eax
  :||:|||   0x00c97a01      cmp   dword [ebp-0x164], 0x00
  :||:|||   0x00c97a08      mov   dword [ebp-0xd0], ecx
  ========< 0x00c97a0e      jz    0xc97a27
  :||:|||   0x00c97a10      movzx ecx, word [esi+edx*4]
  :||:|||   0x00c97a14      cmp   ecx, dword [ebp-0x15c]
  ========< 0x00c97a1a      jnb   0xc97a27
  :||:|||   0x00c97a1c      mov   eax, dword [ebp-0x160]
  :||:|||   0x00c97a22      mov   ecx, dword [eax+ecx*4]
  ========< 0x00c97a25      jmp   0xc97a29
  --------> 0x00c97a27      xor   ecx, ecx
  --------> 0x00c97a29      movzx eax, byte [ebp-0x9a]
  :||:|||   0x00c97a30      test  ecx, ecx
  :||:|||   0x00c97a32      mov   ecx, 0x00
  :||:|||   0x00c97a37      cmovnz ecx, eax
  :||:|||   0x00c97a3a      inc   edx
  :||:|||   0x00c97a3b      cmp   edx, edi
  `=======< 0x00c97a3d      jb    0xc979c0
   |`-----> 0x00c97a3f      or    cl, byte [ebp-0xd0]
   | :|||   0x00c97a45      and   cl, byte [ebp-0x99]
   | :|||   0x00c97a4b      mov   dword [ebp-0x100], ecx
   | :|||   0x00c97a51      mov   dword [ebp-0x164], 0x00
   | :|||   0x00c97a5b      lea   ecx, dword [ebp-0xc4]
   | :|||   0x00c97a61      mov   dword [ebp-0x158], 0x00
   | :|||   0x00c97a6b      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
   | :|||   0x00c97a6f      call  0x4dc500
   | :|||   0x00c97a74      mov   ecx, dword [ebp-0xc8]
   | :|||   0x00c97a7a      mov   eax, dword [ebp-0x130]
   | :|||   0x00c97a80      inc   ecx
   | :|||   0x00c97a81      mov   dword [ebp-0xc8], ecx
   | :|||   0x00c97a87      cmp   ecx, eax
   | `====< 0x00c97a89      jb    0xc97880
   |  |`--> 0x00c97a8f      xor   ecx, ecx
   |  | |   0x00c97a91      mov   dword [ebp-0xd4], ecx
   |  | |   0x00c97a97      test  eax, eax
   |  |,==< 0x00c97a99      jz    0xc99c89
   |  |||   0x00c97a9f      nop
   | .----> 0x00c97aa0      cmp   dword [ebp-0x114], 0x00
   | :|||   0x00c97aa7      mov   eax, dword [ebp-0x134]
   | :|||   0x00c97aad      mov   byte [ebp-0x9a], 0x00
   | :|||   0x00c97ab4      mov   dword [ebp-0xb8], 0x00
   | :|||   0x00c97abe      lea   edi, dword [eax+ecx*4]
   |,=====< 0x00c97ac1      jz    0xc97af8
   ||:|||   0x00c97ac3      movzx ecx, word [edi]
   ||:|||   0x00c97ac6      cmp   ecx, dword [ebp-0x10c]
  ,=======< 0x00c97acc      jnb   0xc97af8
  |||:|||   0x00c97ace      mov   eax, dword [ebp-0x110]
  |||:|||   0x00c97ad4      mov   eax, dword [eax+ecx*4]
  |||:|||   0x00c97ad7      mov   dword [ebp-0xb8], eax
  |||:|||   0x00c97add      test  eax, eax
  ========< 0x00c97adf      jnz   0xc97af8
  |||:|||   0x00c97ae1      cmp   ecx, dword [ebp-0x104]
  ========< 0x00c97ae7      jnb   0xc97af8
  |||:|||   0x00c97ae9      mov   eax, dword [ebp-0x108]
  |||:|||   0x00c97aef      mov   eax, dword [eax+ecx*4]
  |||:|||   0x00c97af2      mov   dword [ebp-0xb8], eax
  `-`-----> 0x00c97af8      mov   eax, dword [ebp-0xcc]
   | :|||   0x00c97afe      mov   esi, dword [eax+0x14]
   | :|||   0x00c97b01      lea   eax, dword [ebp-0x230]
   | :|||   0x00c97b07      push  eax
   | :|||   0x00c97b08      call  0xb6b5c0
   | :|||   0x00c97b0d      add   esp, 0x04
   | :|||   0x00c97b10      cmp   esi, dword [eax]
   |,=====< 0x00c97b12      jnz   0xc97bd2
   ||:|||   0x00c97b18      push  edi
   ||:|||   0x00c97b19      call  0xc26c20
   ||:|||   0x00c97b1e      mov   eax, dword [edi]
   ||:|||   0x00c97b20      add   esp, 0x04
   ||:|||   0x00c97b23      mov   esi, dword [ebp-0xa0]
   ||:|||   0x00c97b29      mov   dword [ebp-0x24], eax
   ||:|||   0x00c97b2c      lea   ecx, dword [ebp-0x20]
   ||:|||   0x00c97b2f      mov   byte [ebp-0x04], 0x15                ; 21
   ||:|||   0x00c97b33      call  0x4f6c50
   ||:|||   0x00c97b38      mov   dword [ebp-0x1c], 0x00
   ||:|||   0x00c97b3f      mov   dword [ebp-0x18], 0x00
   ||:|||   0x00c97b46      mov   dword [ebp-0x14], 0x00
   ||:|||   0x00c97b4d      mov   edi, dword [esi+0x290]
   ||:|||   0x00c97b53      mov   byte [ebp-0x04], 0x16                ; 22
   ||:|||   0x00c97b57      cmp   edi, dword [esi+0x284]
  ,=======< 0x00c97b5d      jnz   0xc97b6a
  |||:|||   0x00c97b5f      lea   ecx, dword [esi+0x280]
  |||:|||   0x00c97b65      call  0xbe2880
  `-------> 0x00c97b6a      mov   ecx, dword [esi+0x28c]
   ||:|||   0x00c97b70      lea   edx, dword [edi+edi*4]
   ||:|||   0x00c97b73      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
   ||:|||   0x00c97b77      mov   dword [ecx+edx*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
   ||:|||   0x00c97b7e      mov   eax, dword [ebp-0x24]
   ||:|||   0x00c97b81      mov   dword [ecx+edx*4], eax
   ||:|||   0x00c97b84      mov   dword [ecx+edx*4+0x04], 0xffffffff   ; [0xffffffff:4]=-1 ; -1
   ||:|||   0x00c97b8c      mov   eax, dword [ebp-0x20]
   ||:|||   0x00c97b8f      mov   dword [ecx+edx*4+0x04], eax
   ||:|||   0x00c97b93      lea   eax, dword [edi+0x01]
   ||:|||   0x00c97b96      movss xmm0, dword [ebp-0x1c]
   ||:|||   0x00c97b9b      movss dword [ecx+edx*4+0x08], xmm0
   ||:|||   0x00c97ba1      movss xmm0, dword [ebp-0x18]
   ||:|||   0x00c97ba6      movss dword [ecx+edx*4+0x0c], xmm0
   ||:|||   0x00c97bac      movss xmm0, dword [ebp-0x14]
   ||:|||   0x00c97bb1      movss dword [ecx+edx*4+0x10], xmm0
   ||:|||   0x00c97bb7      lea   ecx, dword [ebp-0x20]
   ||:|||   0x00c97bba      mov   dword [esi+0x290], eax
   ||:|||   0x00c97bc0      call  0x4dc500
   ||:|||   0x00c97bc5      lea   ecx, dword [ebp-0x24]
   ||:|||   0x00c97bc8      call  0x4dc500
  ,=======< 0x00c97bcd      jmp   0xc99c70
  ||`-----> 0x00c97bd2      mov   eax, dword [ebp-0xcc]
  || :|||   0x00c97bd8      mov   esi, dword [eax+0x14]
  || :|||   0x00c97bdb      lea   eax, dword [ebp-0x234]
  || :|||   0x00c97be1      push  eax
  || :|||   0x00c97be2      call  0xb6b570
  || :|||   0x00c97be7      add   esp, 0x04
  || :|||   0x00c97bea      cmp   esi, dword [eax]
  ||,=====< 0x00c97bec      jnz   0xc97d7a
  |||:|||   0x00c97bf2      push  edi
  |||:|||   0x00c97bf3      call  0xcc0210
  |||:|||   0x00c97bf8      add   esp, 0x04
  |||:|||   0x00c97bfb      test  al, al
  ========< 0x00c97bfd      jz    0xc97cc9
  |||:|||   0x00c97c03      cmp   dword [ebp-0x148], 0x00
  ========< 0x00c97c0a      jz    0xc97c22
  |||:|||   0x00c97c0c      movzx ecx, word [edi]
  |||:|||   0x00c97c0f      cmp   ecx, dword [ebp-0x140]
  ========< 0x00c97c15      jnb   0xc97c22
  |||:|||   0x00c97c17      mov   eax, dword [ebp-0x144]
  |||:|||   0x00c97c1d      mov   eax, dword [eax+ecx*4]
  ========< 0x00c97c20      jmp   0xc97c24
  --------> 0x00c97c22      xor   eax, eax
  --------> 0x00c97c24      test  eax, eax
  ========< 0x00c97c26      jnz   0xc97cc9
  |||:|||   0x00c97c2c      mov   eax, dword [edi]
  |||:|||   0x00c97c2e      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c97c34      mov   dword [ebp-0x24], eax
  |||:|||   0x00c97c37      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c97c3a      mov   byte [ebp-0x04], 0x17                ; 23
  |||:|||   0x00c97c3e      call  0x4f6c50
  |||:|||   0x00c97c43      mov   dword [ebp-0x1c], 0x00
  |||:|||   0x00c97c4a      mov   dword [ebp-0x18], 0x00
  |||:|||   0x00c97c51      mov   dword [ebp-0x14], 0x00
  |||:|||   0x00c97c58      mov   edi, dword [esi+0x2cc]
  |||:|||   0x00c97c5e      mov   byte [ebp-0x04], 0x18                ; 24
  |||:|||   0x00c97c62      cmp   edi, dword [esi+0x2c0]
  ========< 0x00c97c68      jnz   0xc97c75
  |||:|||   0x00c97c6a      lea   ecx, dword [esi+0x2bc]
  |||:|||   0x00c97c70      call  0xbe2880
  --------> 0x00c97c75      mov   ecx, dword [esi+0x2c8]
  |||:|||   0x00c97c7b      lea   edx, dword [edi+edi*4]
  |||:|||   0x00c97c7e      mov   dword [ecx+edx*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c97c85      mov   eax, dword [ebp-0x24]
  |||:|||   0x00c97c88      mov   dword [ecx+edx*4], eax
  |||:|||   0x00c97c8b      mov   dword [ecx+edx*4+0x04], 0xffffffff   ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c97c93      mov   eax, dword [ebp-0x20]
  |||:|||   0x00c97c96      mov   dword [ecx+edx*4+0x04], eax
  |||:|||   0x00c97c9a      lea   eax, dword [edi+0x01]
  |||:|||   0x00c97c9d      movss xmm0, dword [ebp-0x1c]
  |||:|||   0x00c97ca2      movss dword [ecx+edx*4+0x08], xmm0
  |||:|||   0x00c97ca8      movss xmm0, dword [ebp-0x18]
  |||:|||   0x00c97cad      movss dword [ecx+edx*4+0x0c], xmm0
  |||:|||   0x00c97cb3      movss xmm0, dword [ebp-0x14]
  |||:|||   0x00c97cb8      movss dword [ecx+edx*4+0x10], xmm0
  |||:|||   0x00c97cbe      mov   dword [esi+0x2cc], eax
  ========< 0x00c97cc4      jmp   0xc98057
  --------> 0x00c97cc9      mov   eax, dword [edi]
  |||:|||   0x00c97ccb      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c97cd1      mov   dword [ebp-0x24], eax
  |||:|||   0x00c97cd4      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c97cd7      mov   byte [ebp-0x04], 0x19                ; 25
  |||:|||   0x00c97cdb      call  0x4f6c50
  |||:|||   0x00c97ce0      mov   dword [ebp-0x1c], 0x00
  |||:|||   0x00c97ce7      mov   dword [ebp-0x18], 0x00
  |||:|||   0x00c97cee      mov   dword [ebp-0x14], 0x00
  |||:|||   0x00c97cf5      mov   edi, dword [esi+0xc4]
  |||:|||   0x00c97cfb      mov   byte [ebp-0x04], 0x1a                ; 26
  |||:|||   0x00c97cff      cmp   edi, dword [esi+0xb8]
  ========< 0x00c97d05      jnz   0xc97d12
  |||:|||   0x00c97d07      lea   ecx, dword [esi+0xb4]
  |||:|||   0x00c97d0d      call  0xbe2880
  --------> 0x00c97d12      mov   ecx, dword [esi+0xc0]
  |||:|||   0x00c97d18      lea   edx, dword [edi+edi*4]
  |||:|||   0x00c97d1b      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c97d1f      mov   dword [ecx+edx*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c97d26      mov   eax, dword [ebp-0x24]
  |||:|||   0x00c97d29      mov   dword [ecx+edx*4], eax
  |||:|||   0x00c97d2c      mov   dword [ecx+edx*4+0x04], 0xffffffff   ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c97d34      mov   eax, dword [ebp-0x20]
  |||:|||   0x00c97d37      mov   dword [ecx+edx*4+0x04], eax
  |||:|||   0x00c97d3b      lea   eax, dword [edi+0x01]
  |||:|||   0x00c97d3e      movss xmm0, dword [ebp-0x1c]
  |||:|||   0x00c97d43      movss dword [ecx+edx*4+0x08], xmm0
  |||:|||   0x00c97d49      movss xmm0, dword [ebp-0x18]
  |||:|||   0x00c97d4e      movss dword [ecx+edx*4+0x0c], xmm0
  |||:|||   0x00c97d54      movss xmm0, dword [ebp-0x14]
  |||:|||   0x00c97d59      movss dword [ecx+edx*4+0x10], xmm0
  |||:|||   0x00c97d5f      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c97d62      mov   dword [esi+0xc4], eax
  |||:|||   0x00c97d68      call  0x4dc500
  |||:|||   0x00c97d6d      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c97d70      call  0x4dc500
  ========< 0x00c97d75      jmp   0xc99c70
  ||`-----> 0x00c97d7a      mov   eax, dword [ebp-0xcc]
  || :|||   0x00c97d80      mov   esi, dword [eax+0x14]
  || :|||   0x00c97d83      lea   eax, dword [ebp-0x1a0]
  || :|||   0x00c97d89      push  eax
  || :|||   0x00c97d8a      call  0xb6b590
  || :|||   0x00c97d8f      add   esp, 0x04
  || :|||   0x00c97d92      cmp   esi, dword [eax]
  ||,=====< 0x00c97d94      jnz   0xc97e4b
  |||:|||   0x00c97d9a      mov   eax, dword [edi]
  |||:|||   0x00c97d9c      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c97da2      mov   dword [ebp-0x24], eax
  |||:|||   0x00c97da5      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c97da8      mov   byte [ebp-0x04], 0x1b                ; 27
  |||:|||   0x00c97dac      call  0x4f6c50
  |||:|||   0x00c97db1      mov   dword [ebp-0x1c], 0x00
  |||:|||   0x00c97db8      mov   dword [ebp-0x18], 0x00
  |||:|||   0x00c97dbf      mov   dword [ebp-0x14], 0x00
  |||:|||   0x00c97dc6      mov   edi, dword [esi+0x2a4]
  |||:|||   0x00c97dcc      mov   byte [ebp-0x04], 0x1c                ; 28
  |||:|||   0x00c97dd0      cmp   edi, dword [esi+0x298]
  ========< 0x00c97dd6      jnz   0xc97de3
  |||:|||   0x00c97dd8      lea   ecx, dword [esi+0x294]
  |||:|||   0x00c97dde      call  0xbe2880
  --------> 0x00c97de3      mov   ecx, dword [esi+0x2a0]
  |||:|||   0x00c97de9      lea   edx, dword [edi+edi*4]
  |||:|||   0x00c97dec      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c97df0      mov   dword [ecx+edx*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c97df7      mov   eax, dword [ebp-0x24]
  |||:|||   0x00c97dfa      mov   dword [ecx+edx*4], eax
  |||:|||   0x00c97dfd      mov   dword [ecx+edx*4+0x04], 0xffffffff   ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c97e05      mov   eax, dword [ebp-0x20]
  |||:|||   0x00c97e08      mov   dword [ecx+edx*4+0x04], eax
  |||:|||   0x00c97e0c      lea   eax, dword [edi+0x01]
  |||:|||   0x00c97e0f      movss xmm0, dword [ebp-0x1c]
  |||:|||   0x00c97e14      movss dword [ecx+edx*4+0x08], xmm0
  |||:|||   0x00c97e1a      movss xmm0, dword [ebp-0x18]
  |||:|||   0x00c97e1f      movss dword [ecx+edx*4+0x0c], xmm0
  |||:|||   0x00c97e25      movss xmm0, dword [ebp-0x14]
  |||:|||   0x00c97e2a      movss dword [ecx+edx*4+0x10], xmm0
  |||:|||   0x00c97e30      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c97e33      mov   dword [esi+0x2a4], eax
  |||:|||   0x00c97e39      call  0x4dc500
  |||:|||   0x00c97e3e      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c97e41      call  0x4dc500
  ========< 0x00c97e46      jmp   0xc99c70
  ||`-----> 0x00c97e4b      mov   esi, dword [ebp-0xcc]
  || :|||   0x00c97e51      mov   eax, dword [esi+0x10]
  || :|||   0x00c97e54      cmp   eax, 0x04                            ; 4
  ||,=====< 0x00c97e57      jnz   0xc97fd5
  |||:|||   0x00c97e5d      push  edi
  |||:|||   0x00c97e5e      lea   esi, dword [eax+0x05]
  |||:|||   0x00c97e61      call  0xca0620
  |||:|||   0x00c97e66      add   esp, 0x04
  |||:|||   0x00c97e69      test  al, al
  |||:|||   0x00c97e6b      mov   eax, 0x04
  |||:|||   0x00c97e70      cmovnz esi, eax
  |||:|||   0x00c97e73      cmp   dword [ebp-0xac], 0xffffffff
  ========< 0x00c97e7a      jz    0xc97f2e
  |||:|||   0x00c97e80      cmp   byte [ebp-0xb9], 0x00
  ========< 0x00c97e87      jnz   0xc97e96
  |||:|||   0x00c97e89      cmp   byte [ebp-0xae], 0x00
  ========< 0x00c97e90      jz    0xc97f2e
  --------> 0x00c97e96      cmp   byte [ebp-0xa1], 0x00
  ========< 0x00c97e9d      jz    0xc97f2e
  |||:|||   0x00c97ea3      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c97ea9      push  eax
  |||:|||   0x00c97eaa      push  edi
  |||:|||   0x00c97eab      call  0xcd4f50
  |||:|||   0x00c97eb0      mov   byte [ebp-0x9a], al
  |||:|||   0x00c97eb6      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c97ebc      push  edi
  |||:|||   0x00c97ebd      push  eax
  |||:|||   0x00c97ebe      call  0xcd4f50
  |||:|||   0x00c97ec3      mov   byte [ebp-0xba], al
  |||:|||   0x00c97ec9      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c97ecf      push  eax
  |||:|||   0x00c97ed0      call  0xca0620
  |||:|||   0x00c97ed5      push  edi
  |||:|||   0x00c97ed6      mov   byte [ebp-0x99], al
  |||:|||   0x00c97edc      call  0xca0620
  |||:|||   0x00c97ee1      add   esp, 0x18
  |||:|||   0x00c97ee4      test  al, al
  |||:|||   0x00c97ee6      mov   al, byte [ebp-0x99]
  ========< 0x00c97eec      jnz   0xc97ef9
  |||:|||   0x00c97eee      test  al, al
  ========< 0x00c97ef0      jnz   0xc97ef9
  |||:|||   0x00c97ef2      mov   esi, 0x09
  ========< 0x00c97ef7      jmp   0xc97f2e
  --------> 0x00c97ef9      cmp   byte [ebp-0x9a], 0x00
  ========< 0x00c97f00      jz    0xc97f0d
  |||:|||   0x00c97f02      test  al, al
  ========< 0x00c97f04      jz    0xc97f0d
  |||:|||   0x00c97f06      mov   esi, 0x15                            ; 21
  ========< 0x00c97f0b      jmp   0xc97f2e
  --------> 0x00c97f0d      cmp   byte [ebp-0xba], 0x00
  ========< 0x00c97f14      jz    0xc97f2e
  |||:|||   0x00c97f16      test  al, al
  ========< 0x00c97f18      jz    0xc97f29
  |||:|||   0x00c97f1a      movzx esi, byte [ebp-0xae]
  |||:|||   0x00c97f21      xor   esi, 0x01
  |||:|||   0x00c97f24      add   esi, 0x16                            ; 22
  ========< 0x00c97f27      jmp   0xc97f2e
  --------> 0x00c97f29      mov   esi, 0x17                            ; 23
  --------> 0x00c97f2e      mov   ecx, dword [ebp-0xa0]
  |||:|||   0x00c97f34      lea   eax, dword [esi+esi*4]
  |||:|||   0x00c97f37      lea   esi, dword [ecx+eax*4]
  |||:|||   0x00c97f3a      mov   eax, dword [edi]
  |||:|||   0x00c97f3c      mov   dword [ebp-0x24], eax
  |||:|||   0x00c97f3f      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c97f42      mov   byte [ebp-0x04], 0x1d                ; 29
  |||:|||   0x00c97f46      call  0x4f6c50
  |||:|||   0x00c97f4b      mov   dword [ebp-0x1c], 0x00
  |||:|||   0x00c97f52      mov   dword [ebp-0x18], 0x00
  |||:|||   0x00c97f59      mov   dword [ebp-0x14], 0x00
  |||:|||   0x00c97f60      mov   edi, dword [esi+0x10]
  |||:|||   0x00c97f63      mov   byte [ebp-0x04], 0x1e                ; 30
  |||:|||   0x00c97f67      cmp   edi, dword [esi+0x04]
  ========< 0x00c97f6a      jnz   0xc97f73
  |||:|||   0x00c97f6c      mov   ecx, esi
  |||:|||   0x00c97f6e      call  0xbe2880
  --------> 0x00c97f73      mov   ecx, dword [esi+0x0c]
  |||:|||   0x00c97f76      lea   edx, dword [edi+edi*4]
  |||:|||   0x00c97f79      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c97f7d      mov   dword [ecx+edx*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c97f84      mov   eax, dword [ebp-0x24]
  |||:|||   0x00c97f87      mov   dword [ecx+edx*4], eax
  |||:|||   0x00c97f8a      mov   dword [ecx+edx*4+0x04], 0xffffffff   ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c97f92      mov   eax, dword [ebp-0x20]
  |||:|||   0x00c97f95      mov   dword [ecx+edx*4+0x04], eax
  |||:|||   0x00c97f99      lea   eax, dword [edi+0x01]
  |||:|||   0x00c97f9c      movss xmm0, dword [ebp-0x1c]
  |||:|||   0x00c97fa1      movss dword [ecx+edx*4+0x08], xmm0
  |||:|||   0x00c97fa7      movss xmm0, dword [ebp-0x18]
  |||:|||   0x00c97fac      movss dword [ecx+edx*4+0x0c], xmm0
  |||:|||   0x00c97fb2      movss xmm0, dword [ebp-0x14]
  |||:|||   0x00c97fb7      movss dword [ecx+edx*4+0x10], xmm0
  |||:|||   0x00c97fbd      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c97fc0      mov   dword [esi+0x10], eax
  |||:|||   0x00c97fc3      call  0x4dc500
  |||:|||   0x00c97fc8      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c97fcb      call  0x4dc500
  ========< 0x00c97fd0      jmp   0xc99c70
  ||`-----> 0x00c97fd5      cmp   eax, 0x1b                            ; 27
  ||,=====< 0x00c97fd8      jnz   0xc98070
  |||:|||   0x00c97fde      push  edi
  |||:|||   0x00c97fdf      call  0xcc0210
  |||:|||   0x00c97fe4      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c97fea      add   esp, 0x04
  |||:|||   0x00c97fed      test  al, al
  |||:|||   0x00c97fef      mov   eax, dword [edi]
  |||:|||   0x00c97ff1      mov   dword [ebp-0x24], eax
  ========< 0x00c97ff4      jnz   0xc98023
  |||:|||   0x00c97ff6      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c97ff9      mov   byte [ebp-0x04], 0x1f                ; 31
  |||:|||   0x00c97ffd      call  0x4f6c50
  |||:|||   0x00c98002      mov   dword [ebp-0x1c], 0x00
  |||:|||   0x00c98009      mov   dword [ebp-0x18], 0x00
  |||:|||   0x00c98010      mov   dword [ebp-0x14], 0x00
  |||:|||   0x00c98017      mov   byte [ebp-0x04], 0x20                ; 32
  |||:|||   0x00c9801b      lea   ecx, dword [esi+0x21c]
  ========< 0x00c98021      jmp   0xc9804e
  --------> 0x00c98023      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c98026      mov   byte [ebp-0x04], 0x21                ; '!' ; 33
  |||:|||   0x00c9802a      call  0x4f6c50
  |||:|||   0x00c9802f      mov   dword [ebp-0x1c], 0x00
  |||:|||   0x00c98036      mov   dword [ebp-0x18], 0x00
  |||:|||   0x00c9803d      mov   dword [ebp-0x14], 0x00
  |||:|||   0x00c98044      mov   byte [ebp-0x04], 0x22                ; '"' ; 34
  --------> 0x00c98048      lea   ecx, dword [esi+0x294]
  --------> 0x00c9804e      lea   eax, dword [ebp-0x24]
  --------> 0x00c98051      push  eax
  |||:|||   0x00c98052      call  0xca2740
  --------> 0x00c98057      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c9805a      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c9805e      call  0x4dc500
  |||:|||   0x00c98063      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c98066      call  0x4dc500
  ========< 0x00c9806b      jmp   0xc99c70
  ||`-----> 0x00c98070      cmp   eax, 0x0a                            ; 0xa ; 10
  ||,=====< 0x00c98073      jnz   0xc980e4
  |||:|||   0x00c98075      push  edi
  |||:|||   0x00c98076      call  0xcc0210
  |||:|||   0x00c9807b      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98081      add   esp, 0x04
  |||:|||   0x00c98084      test  al, al
  |||:|||   0x00c98086      mov   eax, dword [edi]
  |||:|||   0x00c98088      mov   dword [ebp-0x24], eax
  ========< 0x00c9808b      jnz   0xc980ba
  |||:|||   0x00c9808d      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c98090      mov   byte [ebp-0x04], 0x23                ; '#' ; 35
  |||:|||   0x00c98094      call  0x4f6c50
  |||:|||   0x00c98099      mov   dword [ebp-0x1c], 0x00
  |||:|||   0x00c980a0      mov   dword [ebp-0x18], 0x00
  |||:|||   0x00c980a7      mov   dword [ebp-0x14], 0x00
  |||:|||   0x00c980ae      mov   byte [ebp-0x04], 0x24                ; '$' ; 36
  |||:|||   0x00c980b2      lea   ecx, dword [esi+0xc8]
  ========< 0x00c980b8      jmp   0xc9804e
  --------> 0x00c980ba      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c980bd      mov   byte [ebp-0x04], 0x25                ; '%' ; 37
  |||:|||   0x00c980c1      call  0x4f6c50
  |||:|||   0x00c980c6      mov   dword [ebp-0x1c], 0x00
  |||:|||   0x00c980cd      mov   dword [ebp-0x18], 0x00
  |||:|||   0x00c980d4      mov   dword [ebp-0x14], 0x00
  |||:|||   0x00c980db      mov   byte [ebp-0x04], 0x26                ; '&' ; 38
  ========< 0x00c980df      jmp   0xc98048
  ||`-----> 0x00c980e4      cmp   eax, 0x0f                            ; 0xf ; 15
  ||,=====< 0x00c980e7      jnz   0xc98327
  |||:|||   0x00c980ed      cmp   dword [ebp-0x130], 0x01
  |||:|||   0x00c980f4      mov   ecx, dword [ebp-0xac]
  ========< 0x00c980fa      jz    0xc9811f
  |||:|||   0x00c980fc      cmp   ecx, 0xffffffff                      ; -1
  ========< 0x00c980ff      jnz   0xc98128
  |||:|||   0x00c98101      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98107      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c9810a      push  edi
  |||:|||   0x00c9810b      call  0xc94c10
  |||:|||   0x00c98110      mov   byte [ebp-0x04], 0x2b                ; '+' ; 43
  |||:|||   0x00c98114      lea   ecx, dword [esi+0x12c]
  ========< 0x00c9811a      jmp   0xc98051
  --------> 0x00c9811f      cmp   ecx, 0xffffffff                      ; -1
  ========< 0x00c98122      jz    0xc982ff
  --------> 0x00c98128      cmp   byte [ebp-0xa1], 0x00
  ========< 0x00c9812f      jz    0xc982ff
  |||:|||   0x00c98135      cmp   byte [ebp-0xae], 0x00
  ========< 0x00c9813c      jz    0xc982ff
  |||:|||   0x00c98142      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  |||:|||   0x00c98147      xor   esi, esi
  |||:|||   0x00c98149      mov   byte [ebp-0x9a], 0x01
  |||:|||   0x00c98150      mov   eax, dword [eax+0x1f8]
  |||:|||   0x00c98156      mov   dword [ebp-0x180], 0x00
  |||:|||   0x00c98160      mov   dword [ebp-0x17c], esi
  |||:|||   0x00c98166      mov   edx, dword [eax*4+0x2027ed0]
  |||:|||   0x00c9816d      mov   dword [ebp-0x184], edx
  |||:|||   0x00c98173      test  edx, edx
  ========< 0x00c98175      jz    0xc98198
  |||:|||   0x00c98177      mov   eax, dword [edx]
  |||:|||   0x00c98179      lea   ecx, dword [ebp-0x180]
  |||:|||   0x00c9817f      push  esi
  |||:|||   0x00c98180      push  ecx
  |||:|||   0x00c98181      mov   ecx, edx
  |||:|||   0x00c98183      call  dword [eax+0x3c]                     ; 60
  |||:|||   0x00c98186      mov   ecx, dword [ebp-0xac]
  |||:|||   0x00c9818c      mov   esi, dword [ebp-0x17c]
  |||:|||   0x00c98192      mov   edx, dword [ebp-0x184]
  --------> 0x00c98198      mov   byte [ebp-0x04], 0x27                ; ''' ; 39
  |||:|||   0x00c9819c      test  edx, edx
  ========< 0x00c9819e      jz    0xc9826a
  |||:|||   0x00c981a4      movzx ecx, cx
  |||:|||   0x00c981a7      cmp   ecx, esi
  ========< 0x00c981a9      jnb   0xc9826a
  |||:|||   0x00c981af      mov   eax, dword [ebp-0x180]
  |||:|||   0x00c981b5      mov   ecx, dword [eax+ecx*4]
  |||:|||   0x00c981b8      test  ecx, ecx
  ========< 0x00c981ba      jz    0xc9826a
  |||:|||   0x00c981c0      lea   eax, dword [ebp-0x1ac]
  |||:|||   0x00c981c6      push  eax
  |||:|||   0x00c981c7      call  0x6e2140
  |||:|||   0x00c981cc      xor   ecx, ecx
  |||:|||   0x00c981ce      mov   dword [ebp-0xb8], ecx
  |||:|||   0x00c981d4      cmp   dword [ebp-0x1a8], ecx
  ========< 0x00c981da      jbe   0xc9826a
  --------> 0x00c981e0      mov   eax, dword [ebp-0x1ac]
  |||:|||   0x00c981e6      lea   ecx, dword [eax+ecx*4]
  |||:|||   0x00c981e9      call  0xb014f0
  |||:|||   0x00c981ee      add   eax, 0x20                            ; 32
  |||:|||   0x00c981f1      push  eax
  |||:|||   0x00c981f2      call  0xa95090
  |||:|||   0x00c981f7      mov   edx, eax
  |||:|||   0x00c981f9      xorps xmm0, xmm0
  |||:|||   0x00c981fc      psrldq xmm0, 0x0c
  |||:|||   0x00c98201      xorps xmm1, xmm1
  |||:|||   0x00c98204      movd  ecx, xmm0
  |||:|||   0x00c98208      add   esp, 0x04
  |||:|||   0x00c9820b      xorps xmm0, xmm0
  |||:|||   0x00c9820e      mov   esi, dword [edx+0x0c]
  |||:|||   0x00c98211      and   esi, ecx
  |||:|||   0x00c98213      psrldq xmm0, 0x08
  |||:|||   0x00c98218      not   ecx
  |||:|||   0x00c9821a      movd  eax, xmm0
  |||:|||   0x00c9821e      xor   esi, ecx
  |||:|||   0x00c98220      mov   ecx, dword [edx+0x08]
  |||:|||   0x00c98223      and   ecx, eax
  |||:|||   0x00c98225      not   eax
  |||:|||   0x00c98227      xor   ecx, eax
  |||:|||   0x00c98229      movd  eax, xmm1
  |||:|||   0x00c9822d      and   esi, ecx
  |||:|||   0x00c9822f      mov   ecx, dword [edx]
  |||:|||   0x00c98231      and   ecx, eax
  |||:|||   0x00c98233      not   eax
  |||:|||   0x00c98235      xor   ecx, eax
  |||:|||   0x00c98237      mov   eax, dword [edx+0x04]
  |||:|||   0x00c9823a      and   eax, 0x200000
  |||:|||   0x00c9823f      and   esi, ecx
  |||:|||   0x00c98241      xor   eax, 0xffdfffff
  |||:|||   0x00c98246      and   esi, eax
  |||:|||   0x00c98248      cmp   esi, 0xffffffff                      ; -1
  ========< 0x00c9824b      jnz   0xc982f8
  |||:|||   0x00c98251      mov   ecx, dword [ebp-0xb8]
  |||:|||   0x00c98257      inc   ecx
  |||:|||   0x00c98258      mov   dword [ebp-0xb8], ecx
  |||:|||   0x00c9825e      cmp   ecx, dword [ebp-0x1a8]
  ========< 0x00c98264      jb    0xc981e0
  --------> 0x00c9826a      mov   al, byte [ebp-0x9a]
  --------> 0x00c98270      mov   dword [ebp-0x184], 0x00
  |||:|||   0x00c9827a      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c9827e      test  al, al
  ========< 0x00c98280      jz    0xc982ff
  |||:|||   0x00c98282      lea   eax, dword [ebp-0x11a]
  |||:|||   0x00c98288      mov   word [ebp-0x11a], 0x101              ; 257
  |||:|||   0x00c98291      push  eax
  |||:|||   0x00c98292      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c98298      mov   byte [ebp-0x118], 0x01
  |||:|||   0x00c9829f      push  edi
  |||:|||   0x00c982a0      push  eax
  |||:|||   0x00c982a1      call  0xc4f2c0
  |||:|||   0x00c982a6      add   esp, 0x0c
  |||:|||   0x00c982a9      test  al, al
  ========< 0x00c982ab      jz    0xc982ff
  |||:|||   0x00c982ad      cmp   byte [ebp-0xda], 0x00
  ========< 0x00c982b4      jz    0xc982d1
  |||:|||   0x00c982b6      push  dword [ebp-0xb4]
  |||:|||   0x00c982bc      mov   ecx, dword [ebp-0xe0]
  |||:|||   0x00c982c2      push  dword [ebp-0xe8]
  |||:|||   0x00c982c8      call  0xbb38a0
  |||:|||   0x00c982cd      test  al, al
  ========< 0x00c982cf      jnz   0xc982ff
  --------> 0x00c982d1      push  edi
  |||:|||   0x00c982d2      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c982d5      call  0xc94c10
  |||:|||   0x00c982da      mov   ecx, dword [ebp-0xa0]
  |||:|||   0x00c982e0      mov   eax, dword [ebp-0xac]
  |||:|||   0x00c982e6      mov   byte [ebp-0x04], 0x29                ; ')' ; 41
  |||:|||   0x00c982ea      mov   dword [ebp-0x20], eax
  |||:|||   0x00c982ed      lea   ecx, dword [ecx+0x12c]
  ========< 0x00c982f3      jmp   0xc9804e
  --------> 0x00c982f8      xor   al, al
  ========< 0x00c982fa      jmp   0xc98270
  --------> 0x00c982ff      cmp   byte [ebp+0x20], 0x00
  ========< 0x00c98303      jz    0xc99c70
  |||:|||   0x00c98309      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c9830f      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c98312      push  edi
  |||:|||   0x00c98313      call  0xc94c10
  |||:|||   0x00c98318      mov   byte [ebp-0x04], 0x2a                ; '*' ; 42
  |||:|||   0x00c9831c      lea   ecx, dword [esi+0xdc]
  ========< 0x00c98322      jmp   0xc98051
  ||`-----> 0x00c98327      cmp   eax, 0x0e                            ; 0xe ; 14
  ||,=====< 0x00c9832a      jnz   0xc983f2
  |||:|||   0x00c98330      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  |||:|||   0x00c98335      xor   dl, dl
  |||:|||   0x00c98337      xor   esi, esi
  |||:|||   0x00c98339      mov   dword [ebp-0xa8], edx
  |||:|||   0x00c9833f      mov   eax, dword [eax+0x1f0]
  |||:|||   0x00c98345      mov   dword [ebp-0x18c], 0x00
  |||:|||   0x00c9834f      mov   dword [ebp-0x188], esi
  |||:|||   0x00c98355      mov   ecx, dword [eax*4+0x2027ed0]
  |||:|||   0x00c9835c      mov   dword [ebp-0x190], ecx
  |||:|||   0x00c98362      test  ecx, ecx
  ========< 0x00c98364      jz    0xc98385
  |||:|||   0x00c98366      mov   eax, dword [ecx]
  |||:|||   0x00c98368      lea   edx, dword [ebp-0x18c]
  |||:|||   0x00c9836e      push  esi
  |||:|||   0x00c9836f      push  edx
  |||:|||   0x00c98370      call  dword [eax+0x3c]                     ; 60
  |||:|||   0x00c98373      mov   esi, dword [ebp-0x188]
  |||:|||   0x00c98379      mov   ecx, dword [ebp-0x190]
  |||:|||   0x00c9837f      mov   edx, dword [ebp-0xa8]
  --------> 0x00c98385      mov   byte [ebp-0x04], 0x2c                ; ',' ; 44
  |||:|||   0x00c98389      test  ecx, ecx
  ========< 0x00c9838b      jz    0xc983b0
  |||:|||   0x00c9838d      movzx ecx, word [edi]
  |||:|||   0x00c98390      cmp   ecx, esi
  ========< 0x00c98392      jnb   0xc983b0
  |||:|||   0x00c98394      mov   eax, dword [ebp-0x18c]
  |||:|||   0x00c9839a      mov   eax, dword [eax+ecx*4]
  |||:|||   0x00c9839d      test  eax, eax
  ========< 0x00c9839f      jz    0xc983b0
  |||:|||   0x00c983a1      cmp   dword [eax+0x10], 0xffffffff
  |||:|||   0x00c983a5      mov   eax, 0x01
  |||:|||   0x00c983aa      movzx edx, dl
  |||:|||   0x00c983ad      cmovnz edx, eax
  --------> 0x00c983b0      test  dl, dl
  ========< 0x00c983b2      jz    0xc983e3
  |||:|||   0x00c983b4      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c983ba      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c983bd      push  edi
  |||:|||   0x00c983be      call  0xc94c10
  |||:|||   0x00c983c3      push  eax
  |||:|||   0x00c983c4      lea   ecx, dword [esi+0x118]
  |||:|||   0x00c983ca      mov   byte [ebp-0x04], 0x2d                ; '-' ; 45
  |||:|||   0x00c983ce      call  0xca2740
  |||:|||   0x00c983d3      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c983d6      call  0x4dc500
  |||:|||   0x00c983db      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c983de      call  0x4dc500
  --------> 0x00c983e3      mov   dword [ebp-0x190], 0x00
  ========< 0x00c983ed      jmp   0xc99c6c
  ||`-----> 0x00c983f2      cmp   eax, 0x0c                            ; 0xc ; 12
  ||,=====< 0x00c983f5      jnz   0xc98496
  |||:|||   0x00c983fb      cmp   byte [ebp-0xad], 0x00
  ========< 0x00c98402      jz    0xc98422
  |||:|||   0x00c98404      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c9840a      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c9840d      push  edi
  |||:|||   0x00c9840e      call  0xc94c10
  |||:|||   0x00c98413      mov   byte [ebp-0x04], 0x2f                ; '/' ; 47
  |||:|||   0x00c98417      lea   ecx, dword [esi+0xb4]
  ========< 0x00c9841d      jmp   0xc98051
  --------> 0x00c98422      cmp   byte [esi+0x20], 0x00
  |||:|||   0x00c98426      setz  byte [ebp-0x1b8]
  |||:|||   0x00c9842d      cmp   dword [ebp-0xac], 0xffffffff
  ========< 0x00c98434      jz    0xc9846e
  |||:|||   0x00c98436      push  dword [ebp-0x1b8]
  |||:|||   0x00c9843c      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c98442      push  eax
  |||:|||   0x00c98443      push  edi
  |||:|||   0x00c98444      call  0xd89a20
  |||:|||   0x00c98449      add   esp, 0x0c
  |||:|||   0x00c9844c      test  al, al
  ========< 0x00c9844e      jz    0xc9846e
  |||:|||   0x00c98450      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98456      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c98459      push  edi
  |||:|||   0x00c9845a      call  0xc94c10
  |||:|||   0x00c9845f      mov   byte [ebp-0x04], 0x30                ; '0' ; 48
  |||:|||   0x00c98463      lea   ecx, dword [esi+0xf0]
  ========< 0x00c98469      jmp   0xc98051
  --------> 0x00c9846e      cmp   byte [ebp+0x20], 0x00
  ========< 0x00c98472      jz    0xc99c70
  |||:|||   0x00c98478      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c9847e      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c98481      push  edi
  |||:|||   0x00c98482      call  0xc94c10
  |||:|||   0x00c98487      mov   byte [ebp-0x04], 0x31                ; '1' ; 49
  |||:|||   0x00c9848b      lea   ecx, dword [esi+0xdc]
  ========< 0x00c98491      jmp   0xc98051
  ||`-----> 0x00c98496      cmp   eax, 0x14                            ; 20
  ||,=====< 0x00c98499      jnz   0xc98596
  |||:|||   0x00c9849f      mov   esi, dword [ebp-0xb8]
  |||:|||   0x00c984a5      lea   eax, dword [ebp-0x248]
  |||:|||   0x00c984ab      push  eax
  |||:|||   0x00c984ac      mov   ecx, esi
  |||:|||   0x00c984ae      call  0x6e2140
  |||:|||   0x00c984b3      cmp   dword [eax+0x04], 0x01
  ========< 0x00c984b7      jbe   0xc9856a
  |||:|||   0x00c984bd      mov   eax, dword [ebp-0xc0]
  |||:|||   0x00c984c3      mov   eax, dword [eax+0x04]
  |||:|||   0x00c984c6      test  eax, eax
  ========< 0x00c984c8      jnz   0xc984e8
  |||:|||   0x00c984ca      cmp   dword [esi+0x34], eax
  ========< 0x00c984cd      jbe   0xc9856a
  |||:|||   0x00c984d3      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c984d9      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c984dc      push  edi
  |||:|||   0x00c984dd      call  0xc94c10
  |||:|||   0x00c984e2      mov   byte [ebp-0x04], 0x32                ; '2' ; 50
  ========< 0x00c984e6      jmp   0xc98511
  --------> 0x00c984e8      cmp   eax, 0x01                            ; 1
  ========< 0x00c984eb      jnz   0xc9856a
  |||:|||   0x00c984ed      cmp   byte [ebp-0xa1], 0x00
  ========< 0x00c984f4      jz    0xc98535
  |||:|||   0x00c984f6      cmp   dword [ebp-0xe4], esi
  ========< 0x00c984fc      jnz   0xc9856a
  |||:|||   0x00c984fe      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98504      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c98507      push  edi
  |||:|||   0x00c98508      call  0xc94c10
  |||:|||   0x00c9850d      mov   byte [ebp-0x04], 0x33                ; '3' ; 51
  --------> 0x00c98511      push  eax
  |||:|||   0x00c98512      lea   ecx, dword [esi+0x190]
  |||:|||   0x00c98518      call  0xca2740
  |||:|||   0x00c9851d      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c98520      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c98524      call  0x4dc500
  |||:|||   0x00c98529      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c9852c      call  0x4dc500
  |||:|||   0x00c98531      mov   al, 0x01
  ========< 0x00c98533      jmp   0xc98570
  --------> 0x00c98535      lea   eax, dword [ebp-0x250]
  |||:|||   0x00c9853b      mov   ecx, esi
  |||:|||   0x00c9853d      push  eax
  |||:|||   0x00c9853e      call  0x6e2140
  |||:|||   0x00c98543      lea   ecx, dword [ebp-0xac]
  |||:|||   0x00c98549      push  ecx
  |||:|||   0x00c9854a      mov   ecx, eax
  |||:|||   0x00c9854c      call  0xc9ae00
  |||:|||   0x00c98551      test  al, al
  ========< 0x00c98553      jz    0xc9856a
  |||:|||   0x00c98555      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c9855b      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c9855e      push  edi
  |||:|||   0x00c9855f      call  0xc94c10
  |||:|||   0x00c98564      mov   byte [ebp-0x04], 0x34                ; '4' ; 52
  ========< 0x00c98568      jmp   0xc98511
  --------> 0x00c9856a      mov   al, byte [ebp-0x9a]
  --------> 0x00c98570      test  al, al
  ========< 0x00c98572      jnz   0xc99c70
  |||:|||   0x00c98578      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c9857e      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c98581      push  edi
  |||:|||   0x00c98582      call  0xc94c10
  |||:|||   0x00c98587      mov   byte [ebp-0x04], 0x35                ; '5' ; 53
  |||:|||   0x00c9858b      lea   ecx, dword [esi+0xb4]
  ========< 0x00c98591      jmp   0xc98051
  ||`-----> 0x00c98596      cmp   eax, 0x1c                            ; 28
  ||,=====< 0x00c98599      jnz   0xc985b9
  |||:|||   0x00c9859b      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c985a1      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c985a4      push  edi
  |||:|||   0x00c985a5      call  0xc94c10
  |||:|||   0x00c985aa      mov   byte [ebp-0x04], 0x36                ; '6' ; 54
  |||:|||   0x00c985ae      lea   ecx, dword [esi+0x230]
  ========< 0x00c985b4      jmp   0xc98051
  ||`-----> 0x00c985b9      cmp   eax, 0x01                            ; 1
  ||,=====< 0x00c985bc      jnz   0xc98622
  |||:|||   0x00c985be      push  0x02                                 ; 2
  |||:|||   0x00c985c0      push  edi
  |||:|||   0x00c985c1      call  0xc967c0
  |||:|||   0x00c985c6      add   esp, 0x08
  |||:|||   0x00c985c9      test  al, al
  ========< 0x00c985cb      jz    0xc98604
  |||:|||   0x00c985cd      push  edi
  |||:|||   0x00c985ce      call  0xcc0210
  |||:|||   0x00c985d3      add   esp, 0x04
  |||:|||   0x00c985d6      test  al, al
  ========< 0x00c985d8      jnz   0xc98604
  |||:|||   0x00c985da      push  0x01                                 ; 1
  |||:|||   0x00c985dc      push  edi
  |||:|||   0x00c985dd      call  0xc96d40
  |||:|||   0x00c985e2      add   esp, 0x08
  |||:|||   0x00c985e5      test  al, al
  ========< 0x00c985e7      jnz   0xc98604
  |||:|||   0x00c985e9      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c985ef      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c985f2      push  edi
  |||:|||   0x00c985f3      call  0xc94c10
  |||:|||   0x00c985f8      mov   byte [ebp-0x04], 0x37                ; '7' ; 55
  |||:|||   0x00c985fc      lea   ecx, dword [esi+0x14]
  ========< 0x00c985ff      jmp   0xc98051
  --------> 0x00c98604      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c9860a      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c9860d      push  edi
  |||:|||   0x00c9860e      call  0xc94c10
  |||:|||   0x00c98613      mov   byte [ebp-0x04], 0x38                ; '8' ; 56
  |||:|||   0x00c98617      lea   ecx, dword [esi+0xb4]
  ========< 0x00c9861d      jmp   0xc98051
  ||`-----> 0x00c98622      cmp   eax, 0x11                            ; 17
  ||,=====< 0x00c98625      jnz   0xc9868e
  |||:|||   0x00c98627      push  0x04                                 ; 4
  |||:|||   0x00c98629      push  edi
  |||:|||   0x00c9862a      call  0xc967c0
  |||:|||   0x00c9862f      add   esp, 0x08
  |||:|||   0x00c98632      test  al, al
  ========< 0x00c98634      jz    0xc98670
  |||:|||   0x00c98636      push  edi
  |||:|||   0x00c98637      call  0xcc0210
  |||:|||   0x00c9863c      add   esp, 0x04
  |||:|||   0x00c9863f      test  al, al
  ========< 0x00c98641      jnz   0xc98670
  |||:|||   0x00c98643      push  0x01                                 ; 1
  |||:|||   0x00c98645      push  edi
  |||:|||   0x00c98646      call  0xc96d40
  |||:|||   0x00c9864b      add   esp, 0x08
  |||:|||   0x00c9864e      test  al, al
  ========< 0x00c98650      jnz   0xc98670
  |||:|||   0x00c98652      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98658      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c9865b      push  edi
  |||:|||   0x00c9865c      call  0xc94c10
  |||:|||   0x00c98661      mov   byte [ebp-0x04], 0x39                ; '9' ; 57
  |||:|||   0x00c98665      lea   ecx, dword [esi+0x154]
  ========< 0x00c9866b      jmp   0xc98051
  --------> 0x00c98670      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98676      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c98679      push  edi
  |||:|||   0x00c9867a      call  0xc94c10
  |||:|||   0x00c9867f      mov   byte [ebp-0x04], 0x3a                ; ':' ; 58
  |||:|||   0x00c98683      lea   ecx, dword [esi+0xb4]
  ========< 0x00c98689      jmp   0xc98051
  ||`-----> 0x00c9868e      cmp   eax, 0x12                            ; 18
  ||,=====< 0x00c98691      jnz   0xc986fa
  |||:|||   0x00c98693      push  0x03                                 ; 3
  |||:|||   0x00c98695      push  edi
  |||:|||   0x00c98696      call  0xc967c0
  |||:|||   0x00c9869b      add   esp, 0x08
  |||:|||   0x00c9869e      test  al, al
  ========< 0x00c986a0      jz    0xc986dc
  |||:|||   0x00c986a2      push  edi
  |||:|||   0x00c986a3      call  0xcc0210
  |||:|||   0x00c986a8      add   esp, 0x04
  |||:|||   0x00c986ab      test  al, al
  ========< 0x00c986ad      jnz   0xc986dc
  |||:|||   0x00c986af      push  0x01                                 ; 1
  |||:|||   0x00c986b1      push  edi
  |||:|||   0x00c986b2      call  0xc96d40
  |||:|||   0x00c986b7      add   esp, 0x08
  |||:|||   0x00c986ba      test  al, al
  ========< 0x00c986bc      jnz   0xc986dc
  |||:|||   0x00c986be      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c986c4      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c986c7      push  edi
  |||:|||   0x00c986c8      call  0xc94c10
  |||:|||   0x00c986cd      mov   byte [ebp-0x04], 0x3b                ; ';' ; 59
  |||:|||   0x00c986d1      lea   ecx, dword [esi+0x168]
  ========< 0x00c986d7      jmp   0xc98051
  --------> 0x00c986dc      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c986e2      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c986e5      push  edi
  |||:|||   0x00c986e6      call  0xc94c10
  |||:|||   0x00c986eb      mov   byte [ebp-0x04], 0x3c                ; '<' ; 60
  |||:|||   0x00c986ef      lea   ecx, dword [esi+0xb4]
  ========< 0x00c986f5      jmp   0xc98051
  ||`-----> 0x00c986fa      cmp   eax, 0x1d                            ; 29
  ||,=====< 0x00c986fd      jz    0xc99aa3
  |||:|||   0x00c98703      cmp   eax, 0x1f                            ; 31
  ========< 0x00c98706      jz    0xc99aa3
  |||:|||   0x00c9870c      cmp   eax, 0x1e                            ; 30
  ========< 0x00c9870f      jnz   0xc987c3
  |||:|||   0x00c98715      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  |||:|||   0x00c9871a      lea   ecx, dword [ebp-0x1fc]
  |||:|||   0x00c98720      push  0x01                                 ; 1
  |||:|||   0x00c98722      push  0x00
  |||:|||   0x00c98724      mov   eax, dword [eax+0x1a4]
  |||:|||   0x00c9872a      mov   dword [ebp-0xa8], eax
  |||:|||   0x00c98730      lea   eax, dword [ebp-0xa8]
  |||:|||   0x00c98736      push  eax
  |||:|||   0x00c98737      call  0xb0dfd0
  |||:|||   0x00c9873c      push  edi
  |||:|||   0x00c9873d      lea   ecx, dword [ebp-0x1fc]
  |||:|||   0x00c98743      mov   byte [ebp-0x04], 0x45                ; 'E' ; 69
  |||:|||   0x00c98747      call  0xa6c940
  |||:|||   0x00c9874c      push  edi
  |||:|||   0x00c9874d      test  eax, eax
  ========< 0x00c9874f      jz    0xc9876b
  |||:|||   0x00c98751      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98757      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c9875a      call  0xc94c10
  |||:|||   0x00c9875f      mov   byte [ebp-0x04], 0x46                ; 'F' ; 70
  |||:|||   0x00c98763      lea   ecx, dword [esi+0x258]
  ========< 0x00c98769      jmp   0xc9879e
  --------> 0x00c9876b      call  0xca0620
  |||:|||   0x00c98770      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98776      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c98779      add   esp, 0x04
  |||:|||   0x00c9877c      push  edi
  |||:|||   0x00c9877d      test  al, al
  ========< 0x00c9877f      jz    0xc9878f
  |||:|||   0x00c98781      call  0xc94c10
  |||:|||   0x00c98786      mov   byte [ebp-0x04], 0x47                ; 'G' ; 71
  |||:|||   0x00c9878a      lea   ecx, dword [esi+0x50]
  ========< 0x00c9878d      jmp   0xc9879e
  --------> 0x00c9878f      call  0xc94c10
  |||:|||   0x00c98794      mov   byte [ebp-0x04], 0x48                ; 'H' ; 72
  |||:|||   0x00c98798      lea   ecx, dword [esi+0xb4]
  --------> 0x00c9879e      push  eax
  |||:|||   0x00c9879f      call  0xca2740
  |||:|||   0x00c987a4      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c987a7      call  0x4dc500
  |||:|||   0x00c987ac      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c987af      call  0x4dc500
  |||:|||   0x00c987b4      mov   dword [ebp-0x1fc], 0x00
  ========< 0x00c987be      jmp   0xc99c6c
  --------> 0x00c987c3      cmp   byte [esi+0x03], 0x00
  ========< 0x00c987c7      jz    0xc9887e
  |||:|||   0x00c987cd      mov   eax, dword [ebp-0xb8]
  |||:|||   0x00c987d3      test  eax, eax
  ========< 0x00c987d5      jz    0xc992a3
  |||:|||   0x00c987db      lea   ecx, dword [ebp-0x1b0]
  |||:|||   0x00c987e1      push  ecx
  |||:|||   0x00c987e2      mov   ecx, eax
  |||:|||   0x00c987e4      call  0xdb1640
  |||:|||   0x00c987e9      mov   ecx, eax
  |||:|||   0x00c987eb      mov   byte [ebp-0x04], 0x4a                ; 'J' ; 74
  |||:|||   0x00c987ef      call  0xb014f0
  |||:|||   0x00c987f4      lea   ecx, dword [ebp-0x1b0]
  |||:|||   0x00c987fa      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c987fe      mov   esi, eax
  |||:|||   0x00c98800      call  0x4dc500
  |||:|||   0x00c98805      mov   ecx, esi
  |||:|||   0x00c98807      call  0xa73e70
  |||:|||   0x00c9880c      test  eax, eax
  ========< 0x00c9880e      jz    0xc99c70
  |||:|||   0x00c98814      mov   ecx, dword [ebp-0xb8]
  |||:|||   0x00c9881a      lea   eax, dword [ebp-0x1c4]
  |||:|||   0x00c98820      push  eax
  |||:|||   0x00c98821      call  0xdb1640
  |||:|||   0x00c98826      push  eax
  |||:|||   0x00c98827      mov   byte [ebp-0x04], 0x4b                ; 'K' ; 75
  |||:|||   0x00c9882b      call  0xcc0720
  |||:|||   0x00c98830      add   esp, 0x04
  |||:|||   0x00c98833      mov   byte [ebp-0xba], al
  |||:|||   0x00c98839      lea   ecx, dword [ebp-0x1c4]
  |||:|||   0x00c9883f      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c98843      call  0x4dc500
  |||:|||   0x00c98848      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c9884e      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c98851      push  edi
  |||:|||   0x00c98852      call  0xc94c10
  |||:|||   0x00c98857      cmp   byte [ebp-0xba], 0x00
  ========< 0x00c9885e      jz    0xc9886f
  |||:|||   0x00c98860      mov   byte [ebp-0x04], 0x4c                ; 'L' ; 76
  |||:|||   0x00c98864      lea   ecx, dword [esi+0x2d0]
  ========< 0x00c9886a      jmp   0xc98051
  --------> 0x00c9886f      mov   byte [ebp-0x04], 0x4d                ; 'M' ; 77
  |||:|||   0x00c98873      lea   ecx, dword [esi+0x17c]
  ========< 0x00c98879      jmp   0xc98051
  --------> 0x00c9887e      cmp   dword [ebp-0xac], 0xffffffff
  ========< 0x00c98885      jz    0xc9934c
  |||:|||   0x00c9888b      cmp   byte [ebp-0xae], 0x00
  ========< 0x00c98892      jnz   0xc98eee
  |||:|||   0x00c98898      cmp   byte [ebp-0xb9], 0x00
  ========< 0x00c9889f      jnz   0xc98d95
  |||:|||   0x00c988a5      lea   ecx, dword [ebp-0xf8]
  |||:|||   0x00c988ab      call  0x4f6c50
  |||:|||   0x00c988b0      cmp   byte [ebp-0xa1], 0x00
  |||:|||   0x00c988b7      mov   byte [ebp-0x04], 0x4e                ; 'N' ; 78
  ========< 0x00c988bb      jnz   0xc988cb
  |||:|||   0x00c988bd      mov   eax, dword [ebp-0xac]
  |||:|||   0x00c988c3      mov   dword [ebp-0xf8], eax
  ========< 0x00c988c9      jmp   0xc988f0
  --------> 0x00c988cb      mov   ecx, dword [ebp-0xe4]
  |||:|||   0x00c988d1      lea   eax, dword [ebp-0x1b4]
  |||:|||   0x00c988d7      push  eax
  |||:|||   0x00c988d8      call  0xdb1640
  |||:|||   0x00c988dd      lea   ecx, dword [ebp-0x1b4]
  |||:|||   0x00c988e3      mov   eax, dword [eax]
  |||:|||   0x00c988e5      mov   dword [ebp-0xf8], eax
  |||:|||   0x00c988eb      call  0x4dc500
  --------> 0x00c988f0      mov   ecx, dword [ebp-0xb8]
  |||:|||   0x00c988f6      lea   eax, dword [ebp-0xfc]
  |||:|||   0x00c988fc      push  eax
  |||:|||   0x00c988fd      call  0xdb1640
  |||:|||   0x00c98902      lea   ecx, dword [ebp-0xfc]
  |||:|||   0x00c98908      mov   byte [ebp-0x04], 0x4f                ; 'O' ; 79
  |||:|||   0x00c9890c      call  0xb014f0
  |||:|||   0x00c98911      lea   ecx, dword [ebp-0xf8]
  |||:|||   0x00c98917      mov   esi, eax
  |||:|||   0x00c98919      call  0xb01530
  |||:|||   0x00c9891e      cmp   byte [eax+0x40], 0x00
  ========< 0x00c98922      jz    0xc98d47
  |||:|||   0x00c98928      cmp   byte [esi+0x40], 0x00
  ========< 0x00c9892c      jnz   0xc98945
  |||:|||   0x00c9892e      lea   eax, dword [ebp-0xfc]
  |||:|||   0x00c98934      push  eax
  |||:|||   0x00c98935      call  0xcc0720
  |||:|||   0x00c9893a      add   esp, 0x04
  |||:|||   0x00c9893d      test  al, al
  ========< 0x00c9893f      jz    0xc98d47
  --------> 0x00c98945      cmp   byte [ebp-0xd5], 0x00
  ========< 0x00c9894c      jnz   0xc9895e
  |||:|||   0x00c9894e      cmp   byte [ebp-0xd6], 0x00
  |||:|||   0x00c98955      mov   byte [ebp-0x99], 0x00
  ========< 0x00c9895c      jz    0xc98965
  --------> 0x00c9895e      mov   byte [ebp-0x99], 0x01
  --------> 0x00c98965      mov   ecx, dword [ebp-0xe8]
  |||:|||   0x00c9896b      call  0xb7baa0
  |||:|||   0x00c98970      test  al, al
  ========< 0x00c98972      jnz   0xc98982
  |||:|||   0x00c98974      mov   byte [ebp-0x9a], al
  |||:|||   0x00c9897a      cmp   byte [ebp-0x99], al
  ========< 0x00c98980      jz    0xc98989
  --------> 0x00c98982      mov   byte [ebp-0x9a], 0x01
  --------> 0x00c98989      cmp   byte [ebp-0xa1], 0x00
  |||:|||   0x00c98990      mov   byte [ebp-0x99], 0x00
  ========< 0x00c98997      jnz   0xc989c9
  |||:|||   0x00c98999      lea   ecx, dword [ebp-0xac]
  |||:|||   0x00c9899f      call  0xb014f0
  |||:|||   0x00c989a4      test  eax, eax
  ========< 0x00c989a6      jz    0xc98d32
  |||:|||   0x00c989ac      lea   eax, dword [ebp-0x99]
  |||:|||   0x00c989b2      push  eax
  |||:|||   0x00c989b3      lea   eax, dword [ebp-0x9a]
  |||:|||   0x00c989b9      push  eax
  |||:|||   0x00c989ba      lea   eax, dword [ebp-0xf8]
  |||:|||   0x00c989c0      push  eax
  |||:|||   0x00c989c1      push  esi
  |||:|||   0x00c989c2      call  0xc9ad80
  ========< 0x00c989c7      jmp   0xc989f0
  --------> 0x00c989c9      mov   ecx, dword [ebp-0xe4]
  |||:|||   0x00c989cf      lea   eax, dword [ebp-0x99]
  |||:|||   0x00c989d5      push  eax
  |||:|||   0x00c989d6      lea   eax, dword [ebp-0x9a]
  |||:|||   0x00c989dc      push  eax
  |||:|||   0x00c989dd      lea   eax, dword [ebp-0x154]
  |||:|||   0x00c989e3      push  eax
  |||:|||   0x00c989e4      call  0x6e2140
  |||:|||   0x00c989e9      push  eax
  |||:|||   0x00c989ea      push  esi
  |||:|||   0x00c989eb      call  0xc9ad30
  --------> 0x00c989f0      add   esp, 0x10
  |||:|||   0x00c989f3      cmp   byte [ebp-0x9a], 0x00
  ========< 0x00c989fa      jz    0xc98d32
  |||:|||   0x00c98a00      cmp   byte [ebp-0x99], 0x00
  ========< 0x00c98a07      jz    0xc98d32
  |||:|||   0x00c98a0d      cmp   byte [ebp-0xda], 0x00
  ========< 0x00c98a14      jz    0xc98a6a
  |||:|||   0x00c98a16      push  dword [ebp-0xb4]
  |||:|||   0x00c98a1c      mov   ecx, dword [ebp-0xe0]
  |||:|||   0x00c98a22      push  dword [ebp-0xe8]
  |||:|||   0x00c98a28      call  0xbb38a0
  |||:|||   0x00c98a2d      test  al, al
  ========< 0x00c98a2f      jz    0xc98a6a
  |||:|||   0x00c98a31      cmp   byte [ebp+0x20], 0x00
  ========< 0x00c98a35      jz    0xc98d76
  |||:|||   0x00c98a3b      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98a41      lea   ecx, dword [ebp-0x24]
  |||:|||   0x00c98a44      push  edi
  |||:|||   0x00c98a45      call  0xc94c10
  |||:|||   0x00c98a4a      push  eax
  |||:|||   0x00c98a4b      lea   ecx, dword [esi+0xdc]
  |||:|||   0x00c98a51      mov   byte [ebp-0x04], 0x5b                ; '[' ; 91
  |||:|||   0x00c98a55      call  0xca2740
  |||:|||   0x00c98a5a      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c98a5d      call  0x4dc500
  |||:|||   0x00c98a62      lea   ecx, dword [ebp-0x24]
  ========< 0x00c98a65      jmp   0xc98d71
  --------> 0x00c98a6a      cmp   dword [ebp-0xf4], 0x00
  ========< 0x00c98a71      jz    0xc98d76
  |||:|||   0x00c98a77      lea   eax, dword [esi+0x20]
  |||:|||   0x00c98a7a      push  eax
  |||:|||   0x00c98a7b      call  0xa95090
  |||:|||   0x00c98a80      mov   edx, eax
  |||:|||   0x00c98a82      xorps xmm0, xmm0
  |||:|||   0x00c98a85      psrldq xmm0, 0x0c
  |||:|||   0x00c98a8a      xorps xmm1, xmm1
  |||:|||   0x00c98a8d      movd  ecx, xmm0
  |||:|||   0x00c98a91      add   esp, 0x04
  |||:|||   0x00c98a94      xorps xmm0, xmm0
  |||:|||   0x00c98a97      mov   esi, dword [edx+0x0c]
  |||:|||   0x00c98a9a      and   esi, ecx
  |||:|||   0x00c98a9c      psrldq xmm0, 0x08
  |||:|||   0x00c98aa1      not   ecx
  |||:|||   0x00c98aa3      movd  eax, xmm0
  |||:|||   0x00c98aa7      xor   esi, ecx
  |||:|||   0x00c98aa9      mov   ecx, dword [edx+0x08]
  |||:|||   0x00c98aac      and   ecx, eax
  |||:|||   0x00c98aae      not   eax
  |||:|||   0x00c98ab0      xor   ecx, eax
  |||:|||   0x00c98ab2      movd  eax, xmm1
  |||:|||   0x00c98ab6      and   esi, ecx
  |||:|||   0x00c98ab8      mov   ecx, dword [edx]
  |||:|||   0x00c98aba      and   ecx, eax
  |||:|||   0x00c98abc      not   eax
  |||:|||   0x00c98abe      xor   ecx, eax
  |||:|||   0x00c98ac0      mov   eax, dword [edx+0x04]
  |||:|||   0x00c98ac3      and   eax, 0x400                           ; 1024
  |||:|||   0x00c98ac8      and   esi, ecx
  |||:|||   0x00c98aca      xor   eax, 0xfffffbff                      ; 4294966271
  |||:|||   0x00c98acf      and   esi, eax
  |||:|||   0x00c98ad1      cmp   esi, 0xffffffff                      ; -1
  ========< 0x00c98ad4      jz    0xc98c28
  |||:|||   0x00c98ada      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  |||:|||   0x00c98adf      xor   edx, edx
  |||:|||   0x00c98ae1      mov   eax, dword [eax+0x208]
  |||:|||   0x00c98ae7      mov   dword [ebp-0x20], 0x00
  |||:|||   0x00c98aee      mov   dword [ebp-0x1c], edx
  |||:|||   0x00c98af1      mov   dword [ebp-0x18], edx
  |||:|||   0x00c98af4      mov   ecx, dword [eax*4+0x2027ed0]
  |||:|||   0x00c98afb      mov   dword [ebp-0x14], edx
  |||:|||   0x00c98afe      mov   dword [ebp-0x24], ecx
  |||:|||   0x00c98b01      test  ecx, ecx
  ========< 0x00c98b03      jz    0xc98b18
  |||:|||   0x00c98b05      mov   eax, dword [ecx]
  |||:|||   0x00c98b07      lea   edx, dword [ebp-0x18]
  |||:|||   0x00c98b0a      push  edx
  |||:|||   0x00c98b0b      lea   edx, dword [ebp-0x20]
  |||:|||   0x00c98b0e      push  edx
  |||:|||   0x00c98b0f      call  dword [eax+0x3c]                     ; 60
  |||:|||   0x00c98b12      mov   edx, dword [ebp-0x1c]
  |||:|||   0x00c98b15      mov   ecx, dword [ebp-0x24]
  --------> 0x00c98b18      xor   esi, esi
  |||:|||   0x00c98b1a      mov   byte [ebp-0x04], 0x51                ; 'Q' ; 81
  |||:|||   0x00c98b1e      test  ecx, ecx
  ========< 0x00c98b20      jz    0xc98b42
  |||:|||   0x00c98b22      movzx eax, word [ebp-0xfc]
  |||:|||   0x00c98b29      cmp   eax, edx
  ========< 0x00c98b2b      jnb   0xc98b42
  |||:|||   0x00c98b2d      mov   esi, dword [ebp-0x20]
  |||:|||   0x00c98b30      mov   esi, dword [esi+eax*4]
  |||:|||   0x00c98b33      test  esi, esi
  ========< 0x00c98b35      jnz   0xc98b42
  |||:|||   0x00c98b37      cmp   eax, dword [ebp-0x14]
  ========< 0x00c98b3a      jnb   0xc98b42
  |||:|||   0x00c98b3c      mov   esi, dword [ebp-0x18]
  |||:|||   0x00c98b3f      mov   esi, dword [esi+eax*4]
  --------> 0x00c98b42      mov   eax, dword [ebp-0xcc]
  |||:|||   0x00c98b48      xor   ecx, ecx
  |||:|||   0x00c98b4a      mov   al, byte [eax+0x06]
  |||:|||   0x00c98b4d      test  al, al
  |||:|||   0x00c98b4f      lea   eax, dword [ebp-0xfc]
  |||:|||   0x00c98b55      push  eax
  |||:|||   0x00c98b56      setnz cl
  |||:|||   0x00c98b59      inc   ecx
  |||:|||   0x00c98b5a      mov   dword [ebp-0xa8], ecx
  |||:|||   0x00c98b60      lea   ecx, dword [ebp-0x98]
  |||:|||   0x00c98b66      call  0xb98750
  |||:|||   0x00c98b6b      lea   eax, dword [ebp-0x98]
  |||:|||   0x00c98b71      mov   ecx, esi
  |||:|||   0x00c98b73      push  eax
  |||:|||   0x00c98b74      push  dword [ebp-0xa8]
  |||:|||   0x00c98b7a      push  0x01                                 ; 1
  |||:|||   0x00c98b7c      push  0x00
  |||:|||   0x00c98b7e      push  0x01                                 ; 1
  |||:|||   0x00c98b80      push  dword [ebp-0xf4]
  |||:|||   0x00c98b86      call  0xda4410
  |||:|||   0x00c98b8b      test  eax, eax
  ========< 0x00c98b8d      jz    0xc98c09
  |||:|||   0x00c98b8f      mov   ecx, eax
  |||:|||   0x00c98b91      call  0x62a730
  |||:|||   0x00c98b96      push  edi
  |||:|||   0x00c98b97      mov   eax, dword [eax+0xec]
  |||:|||   0x00c98b9d      dec   eax
  |||:|||   0x00c98b9e      cmp   eax, 0x01                            ; 1
  ========< 0x00c98ba1      jnbe  0xc98bbd
  |||:|||   0x00c98ba3      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98ba9      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98bac      call  0xc94c10
  |||:|||   0x00c98bb1      mov   byte [ebp-0x04], 0x52                ; 'R' ; 82
  |||:|||   0x00c98bb5      lea   ecx, dword [esi+0x17c]
  ========< 0x00c98bbb      jmp   0xc98bf3
  --------> 0x00c98bbd      call  0xcc0210
  |||:|||   0x00c98bc2      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98bc8      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98bcb      add   esp, 0x04
  |||:|||   0x00c98bce      push  edi
  |||:|||   0x00c98bcf      test  al, al
  ========< 0x00c98bd1      jz    0xc98be4
  |||:|||   0x00c98bd3      call  0xc94c10
  |||:|||   0x00c98bd8      mov   byte [ebp-0x04], 0x53                ; 'S' ; 83
  |||:|||   0x00c98bdc      lea   ecx, dword [esi+0x2a8]
  ========< 0x00c98be2      jmp   0xc98bf3
  --------> 0x00c98be4      call  0xc94c10
  |||:|||   0x00c98be9      mov   byte [ebp-0x04], 0x54                ; 'T' ; 84
  |||:|||   0x00c98bed      lea   ecx, dword [esi+0x2e4]
  --------> 0x00c98bf3      push  eax
  |||:|||   0x00c98bf4      call  0xca2740
  |||:|||   0x00c98bf9      lea   ecx, dword [ebp-0x34]
  |||:|||   0x00c98bfc      call  0x4dc500
  |||:|||   0x00c98c01      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98c04      call  0x4dc500
  --------> 0x00c98c09      lea   ecx, dword [ebp-0xfc]
  |||:|||   0x00c98c0f      call  0x4dc500
  |||:|||   0x00c98c14      lea   ecx, dword [ebp-0xf8]
  |||:|||   0x00c98c1a      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c98c1e      call  0x4dc500
  ========< 0x00c98c23      jmp   0xc99c70
  --------> 0x00c98c28      xor   al, al
  |||:|||   0x00c98c2a      mov   dword [ebp-0xb8], eax
  |||:|||   0x00c98c30      cmp   byte [ebp-0xa1], al
  ========< 0x00c98c36      jz    0xc98d02
  |||:|||   0x00c98c3c      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  |||:|||   0x00c98c41      lea   ecx, dword [ebp-0x1e4]
  |||:|||   0x00c98c47      push  0x01                                 ; 1
  |||:|||   0x00c98c49      push  0x00
  |||:|||   0x00c98c4b      mov   eax, dword [eax+0x1a4]
  |||:|||   0x00c98c51      mov   dword [ebp-0xa8], eax
  |||:|||   0x00c98c57      lea   eax, dword [ebp-0xa8]
  |||:|||   0x00c98c5d      push  eax
  |||:|||   0x00c98c5e      call  0xb0dfd0
  |||:|||   0x00c98c63      push  ecx
  |||:|||   0x00c98c64      mov   ecx, esp
  |||:|||   0x00c98c66      mov   byte [ebp-0x04], 0x56                ; 'V' ; 86
  |||:|||   0x00c98c6a      mov   dword [ecx], 0xffffffff              ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c98c70      mov   eax, dword [ebp-0xf8]
  |||:|||   0x00c98c76      mov   dword [ecx], eax
  |||:|||   0x00c98c78      lea   eax, dword [ebp-0x14c]
  |||:|||   0x00c98c7e      push  eax
  |||:|||   0x00c98c7f      call  0xdb0c80
  |||:|||   0x00c98c84      add   esp, 0x08
  |||:|||   0x00c98c87      lea   eax, dword [ebp-0x14c]
  |||:|||   0x00c98c8d      mov   byte [ebp-0x04], 0x57                ; 'W' ; 87
  |||:|||   0x00c98c91      push  eax
  |||:|||   0x00c98c92      lea   ecx, dword [ebp-0x1e4]
  |||:|||   0x00c98c98      call  0xa6c940
  |||:|||   0x00c98c9d      mov   esi, eax
  |||:|||   0x00c98c9f      test  esi, esi
  ========< 0x00c98ca1      jz    0xc98ce3
  |||:|||   0x00c98ca3      mov   ecx, esi
  |||:|||   0x00c98ca5      call  0xc86860
  |||:|||   0x00c98caa      test  al, al
  ========< 0x00c98cac      jz    0xc98ce3
  |||:|||   0x00c98cae      push  edi
  |||:|||   0x00c98caf      lea   ecx, dword [ebp-0x1e4]
  |||:|||   0x00c98cb5      call  0xa6c940
  |||:|||   0x00c98cba      test  eax, eax
  ========< 0x00c98cbc      jz    0xc98ce3
  |||:|||   0x00c98cbe      push  0x01                                 ; 1
  |||:|||   0x00c98cc0      push  dword [esi+0x10]
  |||:|||   0x00c98cc3      mov   ecx, eax
  |||:|||   0x00c98cc5      call  0xc7d860
  |||:|||   0x00c98cca      mov   ecx, dword [ebp-0xb8]
  |||:|||   0x00c98cd0      test  al, al
  |||:|||   0x00c98cd2      movzx ecx, cl
  |||:|||   0x00c98cd5      mov   eax, 0x01
  |||:|||   0x00c98cda      cmovnz ecx, eax
  |||:|||   0x00c98cdd      mov   dword [ebp-0xb8], ecx
  --------> 0x00c98ce3      lea   ecx, dword [ebp-0x14c]
  |||:|||   0x00c98ce9      call  0x4dc500
  |||:|||   0x00c98cee      mov   eax, dword [ebp-0xb8]
  |||:|||   0x00c98cf4      mov   dword [ebp-0x1e4], 0x00
  |||:|||   0x00c98cfe      mov   byte [ebp-0x04], 0x4f                ; 'O' ; 79
  --------> 0x00c98d02      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98d08      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98d0b      push  edi
  |||:|||   0x00c98d0c      test  al, al
  ========< 0x00c98d0e      jz    0xc98d21
  |||:|||   0x00c98d10      call  0xc94c10
  |||:|||   0x00c98d15      mov   byte [ebp-0x04], 0x59                ; 'Y' ; 89
  |||:|||   0x00c98d19      lea   ecx, dword [esi+0x26c]
  ========< 0x00c98d1f      jmp   0xc98d60
  --------> 0x00c98d21      call  0xc94c10
  |||:|||   0x00c98d26      mov   byte [ebp-0x04], 0x5a                ; 'Z' ; 90
  |||:|||   0x00c98d2a      lea   ecx, dword [esi+0x2e4]
  ========< 0x00c98d30      jmp   0xc98d60
  --------> 0x00c98d32      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98d38      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98d3b      push  edi
  |||:|||   0x00c98d3c      call  0xc94c10
  |||:|||   0x00c98d41      mov   byte [ebp-0x04], 0x5c                ; '\' ; 92
  ========< 0x00c98d45      jmp   0xc98d5a
  --------> 0x00c98d47      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98d4d      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98d50      push  edi
  |||:|||   0x00c98d51      call  0xc94c10
  |||:|||   0x00c98d56      mov   byte [ebp-0x04], 0x50                ; 'P' ; 80
  --------> 0x00c98d5a      lea   ecx, dword [esi+0xb4]
  --------> 0x00c98d60      push  eax
  |||:|||   0x00c98d61      call  0xca2740
  |||:|||   0x00c98d66      lea   ecx, dword [ebp-0x34]
  |||:|||   0x00c98d69      call  0x4dc500
  |||:|||   0x00c98d6e      lea   ecx, dword [ebp-0x38]
  --------> 0x00c98d71      call  0x4dc500
  --------> 0x00c98d76      lea   ecx, dword [ebp-0xfc]
  |||:|||   0x00c98d7c      call  0x4dc500
  |||:|||   0x00c98d81      lea   ecx, dword [ebp-0xf8]
  |||:|||   0x00c98d87      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c98d8b      call  0x4dc500
  ========< 0x00c98d90      jmp   0xc99c70
  --------> 0x00c98d95      mov   eax, dword [ebp-0xb8]
  |||:|||   0x00c98d9b      mov   dword [ebp-0xa8], 0x00
  |||:|||   0x00c98da5      test  eax, eax
  ========< 0x00c98da7      jz    0xc98dd7
  |||:|||   0x00c98da9      lea   ecx, dword [ebp-0x1c0]
  |||:|||   0x00c98daf      push  ecx
  |||:|||   0x00c98db0      mov   ecx, eax
  |||:|||   0x00c98db2      call  0xdb1640
  |||:|||   0x00c98db7      mov   ecx, eax
  |||:|||   0x00c98db9      mov   byte [ebp-0x04], 0x6d                ; 'm' ; 109
  |||:|||   0x00c98dbd      call  0xb014f0
  |||:|||   0x00c98dc2      lea   ecx, dword [ebp-0x1c0]
  |||:|||   0x00c98dc8      mov   dword [ebp-0xa8], eax
  |||:|||   0x00c98dce      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c98dd2      call  0x4dc500
  --------> 0x00c98dd7      cmp   byte [ebp-0xa1], 0x00
  ========< 0x00c98dde      jz    0xc99c70
  |||:|||   0x00c98de4      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c98dea      push  eax
  |||:|||   0x00c98deb      push  edi
  |||:|||   0x00c98dec      call  0xcd4f50
  |||:|||   0x00c98df1      add   esp, 0x08
  |||:|||   0x00c98df4      test  al, al
  ========< 0x00c98df6      jz    0xc98e26
  |||:|||   0x00c98df8      lea   eax, dword [ebp-0xec]
  |||:|||   0x00c98dfe      push  eax
  |||:|||   0x00c98dff      call  0xca0620
  |||:|||   0x00c98e04      add   esp, 0x04
  |||:|||   0x00c98e07      test  al, al
  ========< 0x00c98e09      jz    0xc98e6d
  |||:|||   0x00c98e0b      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98e11      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98e14      push  edi
  |||:|||   0x00c98e15      call  0xc94c10
  |||:|||   0x00c98e1a      mov   byte [ebp-0x04], 0x6e                ; 'n' ; 110
  |||:|||   0x00c98e1e      lea   ecx, dword [esi+0x1a4]
  ========< 0x00c98e24      jmp   0xc98e53
  --------> 0x00c98e26      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c98e2c      push  edi
  |||:|||   0x00c98e2d      push  eax
  |||:|||   0x00c98e2e      call  0xcd4f50
  |||:|||   0x00c98e33      add   esp, 0x08
  |||:|||   0x00c98e36      test  al, al
  ========< 0x00c98e38      jz    0xc98e6d
  |||:|||   0x00c98e3a      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98e40      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98e43      push  edi
  |||:|||   0x00c98e44      call  0xc94c10
  |||:|||   0x00c98e49      mov   byte [ebp-0x04], 0x6f                ; 'o' ; 111
  |||:|||   0x00c98e4d      lea   ecx, dword [esi+0x1cc]
  --------> 0x00c98e53      push  eax
  |||:|||   0x00c98e54      call  0xca2740
  |||:|||   0x00c98e59      lea   ecx, dword [ebp-0x34]
  |||:|||   0x00c98e5c      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c98e60      call  0x4dc500
  |||:|||   0x00c98e65      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98e68      call  0x4dc500
  --------> 0x00c98e6d      mov   edx, dword [ebp-0xa8]
  |||:|||   0x00c98e73      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98e79      test  edx, edx
  ========< 0x00c98e7b      jz    0xc98eae
  |||:|||   0x00c98e7d      push  esi
  |||:|||   0x00c98e7e      push  dword [ebp-0xe0]
  |||:|||   0x00c98e84      push  dword [ebp-0xb4]
  |||:|||   0x00c98e8a      push  dword [ebp-0xda]
  |||:|||   0x00c98e90      push  ecx
  |||:|||   0x00c98e91      mov   ecx, esp
  |||:|||   0x00c98e93      push  edx
  |||:|||   0x00c98e94      push  dword [ebp-0xcc]
  |||:|||   0x00c98e9a      mov   dword [ecx], 0xffffffff              ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c98ea0      mov   eax, dword [edi]
  |||:|||   0x00c98ea2      mov   dword [ecx], eax
  |||:|||   0x00c98ea4      call  0xc9a140
  |||:|||   0x00c98ea9      add   esp, 0x1c
  ========< 0x00c98eac      jmp   0xc98eb4
  --------> 0x00c98eae      mov   al, byte [ebp-0x9a]
  --------> 0x00c98eb4      test  al, al
  ========< 0x00c98eb6      jnz   0xc99c70
  |||:|||   0x00c98ebc      push  edi
  |||:|||   0x00c98ebd      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98ec0      call  0xc94c10
  |||:|||   0x00c98ec5      mov   byte [ebp-0x04], 0x70                ; 'p' ; 112
  --------> 0x00c98ec9      lea   ecx, dword [esi+0xb4]
  --------> 0x00c98ecf      push  eax
  |||:|||   0x00c98ed0      call  0xca2740
  |||:|||   0x00c98ed5      lea   ecx, dword [ebp-0x34]
  |||:|||   0x00c98ed8      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c98edc      call  0x4dc500
  |||:|||   0x00c98ee1      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98ee4      call  0x4dc500
  ========< 0x00c98ee9      jmp   0xc99c70
  --------> 0x00c98eee      cmp   byte [ebp-0xa1], 0x00
  ========< 0x00c98ef5      jz    0xc992a3
  |||:|||   0x00c98efb      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  |||:|||   0x00c98f00      lea   ecx, dword [ebp-0x208]
  |||:|||   0x00c98f06      push  0x01                                 ; 1
  |||:|||   0x00c98f08      push  0x00
  |||:|||   0x00c98f0a      mov   eax, dword [eax+0x1a4]
  |||:|||   0x00c98f10      mov   dword [ebp-0xa8], eax
  |||:|||   0x00c98f16      lea   eax, dword [ebp-0xa8]
  |||:|||   0x00c98f1c      push  eax
  |||:|||   0x00c98f1d      call  0xb0dfd0
  |||:|||   0x00c98f22      push  edi
  |||:|||   0x00c98f23      lea   ecx, dword [ebp-0x208]
  |||:|||   0x00c98f29      mov   byte [ebp-0x04], 0x5d                ; ']' ; 93
  |||:|||   0x00c98f2d      call  0xa6c940
  |||:|||   0x00c98f32      cmp   byte [ebp-0xda], 0x00
  |||:|||   0x00c98f39      mov   esi, eax
  ========< 0x00c98f3b      jz    0xc98f80
  |||:|||   0x00c98f3d      push  dword [ebp-0xb4]
  |||:|||   0x00c98f43      mov   ecx, dword [ebp-0xe0]
  |||:|||   0x00c98f49      push  dword [ebp-0xe8]
  |||:|||   0x00c98f4f      call  0xbb38a0
  |||:|||   0x00c98f54      test  al, al
  ========< 0x00c98f56      jz    0xc98f80
  |||:|||   0x00c98f58      cmp   byte [ebp+0x20], 0x00
  ========< 0x00c98f5c      jz    0xc9928b
  |||:|||   0x00c98f62      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98f68      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98f6b      push  edi
  |||:|||   0x00c98f6c      call  0xc94c10
  |||:|||   0x00c98f71      mov   byte [ebp-0x04], 0x5e                ; '^' ; 94
  |||:|||   0x00c98f75      lea   ecx, dword [esi+0xdc]
  ========< 0x00c98f7b      jmp   0xc99275
  --------> 0x00c98f80      cmp   byte [ebp-0x100], 0x00
  ========< 0x00c98f87      jz    0xc98ff1
  |||:|||   0x00c98f89      push  0x01                                 ; 1
  |||:|||   0x00c98f8b      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c98f91      push  eax
  |||:|||   0x00c98f92      push  edi
  |||:|||   0x00c98f93      call  0xd89a20
  |||:|||   0x00c98f98      add   esp, 0x0c
  |||:|||   0x00c98f9b      test  al, al
  ========< 0x00c98f9d      jz    0xc98fbd
  |||:|||   0x00c98f9f      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98fa5      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98fa8      push  edi
  |||:|||   0x00c98fa9      call  0xc94c10
  |||:|||   0x00c98fae      mov   byte [ebp-0x04], 0x60                ; '`' ; 96
  |||:|||   0x00c98fb2      lea   ecx, dword [esi+0xf0]
  ========< 0x00c98fb8      jmp   0xc99275
  --------> 0x00c98fbd      push  0x01                                 ; 1
  |||:|||   0x00c98fbf      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c98fc5      push  edi
  |||:|||   0x00c98fc6      push  eax
  |||:|||   0x00c98fc7      call  0xd89a20
  |||:|||   0x00c98fcc      add   esp, 0x0c
  |||:|||   0x00c98fcf      test  al, al
  ========< 0x00c98fd1      jz    0xc98ff1
  |||:|||   0x00c98fd3      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c98fd9      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c98fdc      push  edi
  |||:|||   0x00c98fdd      call  0xc94c10
  |||:|||   0x00c98fe2      mov   byte [ebp-0x04], 0x61                ; 'a' ; 97
  |||:|||   0x00c98fe6      lea   ecx, dword [esi+0x104]
  ========< 0x00c98fec      jmp   0xc99275
  --------> 0x00c98ff1      cmp   byte [ebp+0x20], 0x00
  ========< 0x00c98ff5      jz    0xc9904e
  |||:|||   0x00c98ff7      mov   eax, dword [0x201e2dc]               ; [0x201e2dc:4]=0
  |||:|||   0x00c98ffc      cmp   dword [eax+0x2a8], 0x07
  ========< 0x00c99003      jnz   0xc9904e
  |||:|||   0x00c99005      lea   eax, dword [ebp-0x117]
  |||:|||   0x00c9900b      mov   word [ebp-0x117], 0x101              ; 257
  |||:|||   0x00c99014      push  eax
  |||:|||   0x00c99015      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c9901b      mov   byte [ebp-0x115], 0x01
  |||:|||   0x00c99022      push  edi
  |||:|||   0x00c99023      push  eax
  |||:|||   0x00c99024      call  0xc4f2c0
  |||:|||   0x00c99029      add   esp, 0x0c
  |||:|||   0x00c9902c      test  al, al
  ========< 0x00c9902e      jz    0xc9904e
  |||:|||   0x00c99030      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99036      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99039      push  edi
  |||:|||   0x00c9903a      call  0xc94c10
  |||:|||   0x00c9903f      mov   byte [ebp-0x04], 0x62                ; 'b' ; 98
  |||:|||   0x00c99043      lea   ecx, dword [esi+0x12c]
  ========< 0x00c99049      jmp   0xc99275
  --------> 0x00c9904e      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c99054      push  eax
  |||:|||   0x00c99055      push  edi
  |||:|||   0x00c99056      call  0xcd4f50
  |||:|||   0x00c9905b      add   esp, 0x08
  |||:|||   0x00c9905e      test  al, al
  ========< 0x00c99060      jz    0xc990a1
  |||:|||   0x00c99062      lea   eax, dword [ebp-0xec]
  |||:|||   0x00c99068      push  eax
  |||:|||   0x00c99069      call  0xca0620
  |||:|||   0x00c9906e      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99074      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99077      add   esp, 0x04
  |||:|||   0x00c9907a      push  edi
  |||:|||   0x00c9907b      test  al, al
  ========< 0x00c9907d      jz    0xc99093
  |||:|||   0x00c9907f      call  0xc94c10
  |||:|||   0x00c99084      mov   byte [ebp-0x04], 0x63                ; 'c' ; 99
  |||:|||   0x00c99088      lea   ecx, dword [esi+0x1a4]
  ========< 0x00c9908e      jmp   0xc99275
  --------> 0x00c99093      call  0xc94c10
  |||:|||   0x00c99098      mov   byte [ebp-0x04], 0x64                ; 'd' ; 100
  ========< 0x00c9909c      jmp   0xc9926f
  --------> 0x00c990a1      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c990a7      push  edi
  |||:|||   0x00c990a8      push  eax
  |||:|||   0x00c990a9      call  0xcd4f50
  |||:|||   0x00c990ae      add   esp, 0x08
  |||:|||   0x00c990b1      test  al, al
  ========< 0x00c990b3      jz    0xc991a7
  |||:|||   0x00c990b9      push  edi
  |||:|||   0x00c990ba      call  0xca0620
  |||:|||   0x00c990bf      add   esp, 0x04
  |||:|||   0x00c990c2      test  al, al
  ========< 0x00c990c4      jnz   0xc990f1
  |||:|||   0x00c990c6      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c990cc      push  eax
  |||:|||   0x00c990cd      call  0xca0620
  |||:|||   0x00c990d2      add   esp, 0x04
  |||:|||   0x00c990d5      test  al, al
  ========< 0x00c990d7      jnz   0xc990f1
  |||:|||   0x00c990d9      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c990df      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c990e2      push  edi
  |||:|||   0x00c990e3      call  0xc94c10
  |||:|||   0x00c990e8      mov   byte [ebp-0x04], 0x65                ; 'e' ; 101
  ========< 0x00c990ec      jmp   0xc9926f
  --------> 0x00c990f1      push  edi
  |||:|||   0x00c990f2      call  0xca0620
  |||:|||   0x00c990f7      add   esp, 0x04
  |||:|||   0x00c990fa      test  al, al
  ========< 0x00c990fc      jnz   0xc99162
  |||:|||   0x00c990fe      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c99104      push  eax
  |||:|||   0x00c99105      call  0xca0620
  |||:|||   0x00c9910a      add   esp, 0x04
  |||:|||   0x00c9910d      test  al, al
  ========< 0x00c9910f      jz    0xc99162
  |||:|||   0x00c99111      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99117      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c9911d      push  eax
  |||:|||   0x00c9911e      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99121      call  0xc94c10
  |||:|||   0x00c99126      push  eax
  |||:|||   0x00c99127      lea   ecx, dword [esi+0x1a4]
  |||:|||   0x00c9912d      mov   byte [ebp-0x04], 0x66                ; 'f' ; 102
  |||:|||   0x00c99131      call  0xca2740
  |||:|||   0x00c99136      lea   ecx, dword [ebp-0x34]
  |||:|||   0x00c99139      call  0x4dc500
  |||:|||   0x00c9913e      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99141      call  0x4dc500
  |||:|||   0x00c99146      mov   ecx, esi
  |||:|||   0x00c99148      mov   eax, dword [ecx+0x1b4]
  |||:|||   0x00c9914e      mov   ecx, dword [ecx+0x1b0]
  |||:|||   0x00c99154      lea   edx, dword [eax+eax*4]
  |||:|||   0x00c99157      mov   eax, dword [edi]
  |||:|||   0x00c99159      mov   dword [ecx+edx*4-0x10], eax
  ========< 0x00c9915d      jmp   0xc9928b
  --------> 0x00c99162      lea   eax, dword [ebp-0xac]
  |||:|||   0x00c99168      push  eax
  |||:|||   0x00c99169      call  0xca0620
  |||:|||   0x00c9916e      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99174      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99177      add   esp, 0x04
  |||:|||   0x00c9917a      push  edi
  |||:|||   0x00c9917b      test  al, al
  ========< 0x00c9917d      jz    0xc99193
  |||:|||   0x00c9917f      call  0xc94c10
  |||:|||   0x00c99184      mov   byte [ebp-0x04], 0x67                ; 'g' ; 103
  |||:|||   0x00c99188      lea   ecx, dword [esi+0x1b8]
  ========< 0x00c9918e      jmp   0xc99275
  --------> 0x00c99193      call  0xc94c10
  |||:|||   0x00c99198      mov   byte [ebp-0x04], 0x68                ; 'h' ; 104
  |||:|||   0x00c9919c      lea   ecx, dword [esi+0x1cc]
  ========< 0x00c991a2      jmp   0xc99275
  --------> 0x00c991a7      test  esi, esi
  ========< 0x00c991a9      jz    0xc991d8
  |||:|||   0x00c991ab      mov   ecx, esi
  |||:|||   0x00c991ad      call  0xc86860
  |||:|||   0x00c991b2      test  al, al
  ========< 0x00c991b4      jz    0xc991d8
  |||:|||   0x00c991b6      mov   eax, dword [ebp-0xac]
  |||:|||   0x00c991bc      cmp   eax, dword [edi]
  ========< 0x00c991be      jnz   0xc991d8
  |||:|||   0x00c991c0      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c991c6      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c991c9      push  edi
  |||:|||   0x00c991ca      call  0xc94c10
  |||:|||   0x00c991cf      mov   byte [ebp-0x04], 0x69                ; 'i' ; 105
  ========< 0x00c991d3      jmp   0xc9926f
  --------> 0x00c991d8      mov   eax, dword [ebp-0xb8]
  |||:|||   0x00c991de      test  eax, eax
  ========< 0x00c991e0      jz    0xc99252
  |||:|||   0x00c991e2      lea   ecx, dword [ebp-0x124]
  |||:|||   0x00c991e8      push  ecx
  |||:|||   0x00c991e9      mov   ecx, eax
  |||:|||   0x00c991eb      call  0xdb1640
  |||:|||   0x00c991f0      mov   ecx, eax
  |||:|||   0x00c991f2      mov   byte [ebp-0x04], 0x6a                ; 'j' ; 106
  |||:|||   0x00c991f6      call  0xb014f0
  |||:|||   0x00c991fb      mov   esi, eax
  |||:|||   0x00c991fd      mov   byte [ebp-0x04], 0x5d                ; ']' ; 93
  |||:|||   0x00c99201      lea   ecx, dword [ebp-0x124]
  |||:|||   0x00c99207      mov   dword [ebp-0xa8], esi
  |||:|||   0x00c9920d      call  0x4dc500
  |||:|||   0x00c99212      test  esi, esi
  |||:|||   0x00c99214      mov   esi, dword [ebp-0xa0]
  ========< 0x00c9921a      jz    0xc99258
  |||:|||   0x00c9921c      push  esi
  |||:|||   0x00c9921d      push  dword [ebp-0xe0]
  |||:|||   0x00c99223      push  dword [ebp-0xb4]
  |||:|||   0x00c99229      push  dword [ebp-0xda]
  |||:|||   0x00c9922f      push  ecx
  |||:|||   0x00c99230      mov   ecx, esp
  |||:|||   0x00c99232      push  dword [ebp-0xa8]
  |||:|||   0x00c99238      push  dword [ebp-0xcc]
  |||:|||   0x00c9923e      mov   dword [ecx], 0xffffffff              ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c99244      mov   eax, dword [edi]
  |||:|||   0x00c99246      mov   dword [ecx], eax
  |||:|||   0x00c99248      call  0xc9a140
  |||:|||   0x00c9924d      add   esp, 0x1c
  ========< 0x00c99250      jmp   0xc9925e
  --------> 0x00c99252      mov   esi, dword [ebp-0xa0]
  --------> 0x00c99258      mov   al, byte [ebp-0x9a]
  --------> 0x00c9925e      test  al, al
  ========< 0x00c99260      jnz   0xc9928d
  |||:|||   0x00c99262      push  edi
  |||:|||   0x00c99263      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99266      call  0xc94c10
  |||:|||   0x00c9926b      mov   byte [ebp-0x04], 0x6b                ; 'k' ; 107
  --------> 0x00c9926f      lea   ecx, dword [esi+0xb4]
  --------> 0x00c99275      push  eax
  |||:|||   0x00c99276      call  0xca2740
  |||:|||   0x00c9927b      lea   ecx, dword [ebp-0x34]
  |||:|||   0x00c9927e      call  0x4dc500
  |||:|||   0x00c99283      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99286      call  0x4dc500
  --------> 0x00c9928b      mov   al, 0x01
  --------> 0x00c9928d      mov   dword [ebp-0x208], 0x00
  |||:|||   0x00c99297      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c9929b      test  al, al
  ========< 0x00c9929d      jnz   0xc99c70
  --------> 0x00c992a3      mov   ecx, dword [edi]
  |||:|||   0x00c992a5      cmp   dword [ebp-0xac], ecx
  ========< 0x00c992ab      jnz   0xc9947f
  |||:|||   0x00c992b1      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c992b7      mov   dword [ebp-0x24], ecx
  |||:|||   0x00c992ba      lea   ecx, dword [ebp-0x20]
  |||:|||   0x00c992bd      mov   byte [ebp-0x04], 0x91                ; 145
  |||:|||   0x00c992c1      call  0x4f6c50
  |||:|||   0x00c992c6      mov   dword [ebp-0x1c], 0x00
  |||:|||   0x00c992cd      mov   dword [ebp-0x18], 0x00
  |||:|||   0x00c992d4      mov   dword [ebp-0x14], 0x00
  |||:|||   0x00c992db      mov   edi, dword [esi+0xc4]
  |||:|||   0x00c992e1      mov   byte [ebp-0x04], 0x92                ; 146
  |||:|||   0x00c992e5      cmp   edi, dword [esi+0xb8]
  ========< 0x00c992eb      jnz   0xc992f8
  |||:|||   0x00c992ed      lea   ecx, dword [esi+0xb4]
  |||:|||   0x00c992f3      call  0xbe2880
  --------> 0x00c992f8      mov   ecx, dword [esi+0xc0]
  |||:|||   0x00c992fe      lea   edx, dword [edi+edi*4]
  |||:|||   0x00c99301      mov   dword [ecx+edx*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c99308      mov   eax, dword [ebp-0x24]
  |||:|||   0x00c9930b      mov   dword [ecx+edx*4], eax
  |||:|||   0x00c9930e      mov   dword [ecx+edx*4+0x04], 0xffffffff   ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c99316      mov   eax, dword [ebp-0x20]
  |||:|||   0x00c99319      mov   dword [ecx+edx*4+0x04], eax
  |||:|||   0x00c9931d      lea   eax, dword [edi+0x01]
  |||:|||   0x00c99320      movss xmm0, dword [ebp-0x1c]
  |||:|||   0x00c99325      movss dword [ecx+edx*4+0x08], xmm0
  |||:|||   0x00c9932b      movss xmm0, dword [ebp-0x18]
  |||:|||   0x00c99330      movss dword [ecx+edx*4+0x0c], xmm0
  |||:|||   0x00c99336      movss xmm0, dword [ebp-0x14]
  |||:|||   0x00c9933b      movss dword [ecx+edx*4+0x10], xmm0
  |||:|||   0x00c99341      mov   dword [esi+0xc4], eax
  ========< 0x00c99347      jmp   0xc98057
  --------> 0x00c9934c      cmp   byte [ebp-0xda], 0x00
  ========< 0x00c99353      jz    0xc993b2
  |||:|||   0x00c99355      push  dword [ebp-0xb4]
  |||:|||   0x00c9935b      mov   ecx, dword [ebp-0xe0]
  |||:|||   0x00c99361      push  dword [ebp-0xe8]
  |||:|||   0x00c99367      call  0xbb38a0
  |||:|||   0x00c9936c      test  al, al
  ========< 0x00c9936e      jz    0xc993b2
  |||:|||   0x00c99370      cmp   byte [ebp+0x20], 0x00
  ========< 0x00c99374      jz    0xc99c70
  |||:|||   0x00c9937a      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99380      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99383      push  edi
  |||:|||   0x00c99384      call  0xc94c10
  |||:|||   0x00c99389      push  eax
  |||:|||   0x00c9938a      lea   ecx, dword [esi+0xdc]
  |||:|||   0x00c99390      mov   byte [ebp-0x04], 0x71                ; 'q' ; 113
  |||:|||   0x00c99394      call  0xca2740
  |||:|||   0x00c99399      lea   ecx, dword [ebp-0x34]
  |||:|||   0x00c9939c      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c993a0      call  0x4dc500
  |||:|||   0x00c993a5      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c993a8      call  0x4dc500
  ========< 0x00c993ad      jmp   0xc99c70
  --------> 0x00c993b2      cmp   dword [esi+0x10], 0x06
  ========< 0x00c993b6      jnz   0xc994b4
  |||:|||   0x00c993bc      mov   eax, dword [ebp-0xb8]
  |||:|||   0x00c993c2      test  eax, eax
  ========< 0x00c993c4      jz    0xc992a3
  |||:|||   0x00c993ca      lea   ecx, dword [ebp-0x120]
  |||:|||   0x00c993d0      push  ecx
  |||:|||   0x00c993d1      mov   ecx, eax
  |||:|||   0x00c993d3      call  0xdb1640
  |||:|||   0x00c993d8      mov   ecx, eax
  |||:|||   0x00c993da      mov   byte [ebp-0x04], 0x72                ; 'r' ; 114
  |||:|||   0x00c993de      call  0xb014f0
  |||:|||   0x00c993e3      lea   ecx, dword [ebp-0x120]
  |||:|||   0x00c993e9      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c993ed      mov   esi, eax
  |||:|||   0x00c993ef      call  0x4dc500
  |||:|||   0x00c993f4      push  edi
  |||:|||   0x00c993f5      call  0xcc0210
  |||:|||   0x00c993fa      add   esp, 0x04
  |||:|||   0x00c993fd      test  al, al
  ========< 0x00c993ff      jz    0xc9941f
  |||:|||   0x00c99401      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99407      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c9940a      push  edi
  |||:|||   0x00c9940b      call  0xc94c10
  |||:|||   0x00c99410      mov   byte [ebp-0x04], 0x73                ; 's' ; 115
  |||:|||   0x00c99414      lea   ecx, dword [esi+0x294]
  ========< 0x00c9941a      jmp   0xc98ecf
  --------> 0x00c9941f      push  esi
  |||:|||   0x00c99420      call  0xcfa700
  |||:|||   0x00c99425      add   esp, 0x04
  |||:|||   0x00c99428      push  edi
  |||:|||   0x00c99429      test  al, al
  ========< 0x00c9942b      jz    0xc9944a
  |||:|||   0x00c9942d      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99433      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99436      call  0xc94c10
  |||:|||   0x00c9943b      mov   byte [ebp-0x04], 0x74                ; 't' ; 116
  |||:|||   0x00c9943f      lea   ecx, dword [esi+0x140]
  ========< 0x00c99445      jmp   0xc98ecf
  --------> 0x00c9944a      call  0xca0620
  |||:|||   0x00c9944f      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99455      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99458      add   esp, 0x04
  |||:|||   0x00c9945b      push  edi
  |||:|||   0x00c9945c      test  al, al
  ========< 0x00c9945e      jz    0xc99471
  |||:|||   0x00c99460      call  0xc94c10
  |||:|||   0x00c99465      mov   byte [ebp-0x04], 0x75                ; 'u' ; 117
  |||:|||   0x00c99469      lea   ecx, dword [esi+0x50]
  ========< 0x00c9946c      jmp   0xc98ecf
  --------> 0x00c99471      call  0xc94c10
  |||:|||   0x00c99476      mov   byte [ebp-0x04], 0x76                ; 'v' ; 118
  ========< 0x00c9947a      jmp   0xc98ec9
  --------> 0x00c9947f      mov   edx, dword [ebp-0xf0]
  |||:|||   0x00c99485      mov   esi, dword [edx+0x10]
  |||:|||   0x00c99488      cmp   esi, dword [edx+0x04]
  ========< 0x00c9948b      jnz   0xc9949a
  |||:|||   0x00c9948d      mov   ecx, edx
  |||:|||   0x00c9948f      call  0x7aab00
  |||:|||   0x00c99494      mov   edx, dword [ebp-0xf0]
  --------> 0x00c9949a      mov   ecx, dword [edx+0x0c]
  |||:|||   0x00c9949d      mov   dword [ecx+esi*4], 0xffffffff        ; [0xffffffff:4]=-1 ; -1
  |||:|||   0x00c994a4      mov   eax, dword [edi]
  |||:|||   0x00c994a6      mov   dword [ecx+esi*4], eax
  |||:|||   0x00c994a9      lea   eax, dword [esi+0x01]
  |||:|||   0x00c994ac      mov   dword [edx+0x10], eax
  ========< 0x00c994af      jmp   0xc99c70
  --------> 0x00c994b4      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  |||:|||   0x00c994b9      lea   ecx, dword [ebp-0x214]
  |||:|||   0x00c994bf      push  0x01                                 ; 1
  |||:|||   0x00c994c1      push  0x00
  |||:|||   0x00c994c3      mov   byte [ebp-0x99], 0x01
  |||:|||   0x00c994ca      mov   eax, dword [eax+0x1a4]
  |||:|||   0x00c994d0      mov   dword [ebp-0xa8], eax
  |||:|||   0x00c994d6      lea   eax, dword [ebp-0xa8]
  |||:|||   0x00c994dc      push  eax
  |||:|||   0x00c994dd      mov   byte [ebp-0x9a], 0x00
  |||:|||   0x00c994e4      call  0xb0dfd0
  |||:|||   0x00c994e9      push  edi
  |||:|||   0x00c994ea      lea   ecx, dword [ebp-0x214]
  |||:|||   0x00c994f0      mov   byte [ebp-0x04], 0x77                ; 'w' ; 119
  |||:|||   0x00c994f4      call  0xa6c940
  |||:|||   0x00c994f9      test  eax, eax
  ========< 0x00c994fb      jnz   0xc99504
  |||:|||   0x00c994fd      xor   al, al
  ========< 0x00c994ff      jmp   0xc9965d
  --------> 0x00c99504      mov   esi, dword [0x201fc64]               ; [0x201fc64:4]=0
  |||:|||   0x00c9950a      xor   ecx, ecx
  |||:|||   0x00c9950c      mov   dword [ebp-0x48], 0x7f800000
  |||:|||   0x00c99513      mov   dword [ebp-0x44], 0x7f800000
  |||:|||   0x00c9951a      nop   word [eax+eax*1], ax
  --------> 0x00c99520      movss xmm0, dword [ebp+ecx*1+0x28]
  |||:|||   0x00c99526      ucomiss xmm0, dword [ebp+ecx*1-0x48]
  |||:|||   0x00c9952b      lahf
  |||:|||   0x00c9952c      test  ah, 0x44                             ; 68
  ========< 0x00c9952f      jp    0xc99541
  |||:|||   0x00c99531      add   ecx, 0x04
  |||:|||   0x00c99534      cmp   ecx, 0x08                            ; 8
  ========< 0x00c99537      jb    0xc99520
  |||:|||   0x00c99539      mov   eax, dword [ebp-0xb4]
  ========< 0x00c9953f      jmp   0xc99544
  --------> 0x00c99541      lea   eax, dword [ebp+0x28]
  --------> 0x00c99544      movss xmm0, dword [eax]
  |||:|||   0x00c99548      mov   ecx, esi
  |||:|||   0x00c9954a      movss dword [ebp-0x68], xmm0
  |||:|||   0x00c9954f      movss xmm0, dword [eax+0x04]
  |||:|||   0x00c99554      lea   eax, dword [ebp-0x68]
  |||:|||   0x00c99557      push  eax
  |||:|||   0x00c99558      movss dword [ebp-0x64], xmm0
  |||:|||   0x00c9955d      call  0xda51d0
  |||:|||   0x00c99562      test  eax, eax
  ========< 0x00c99564      jns   0xc9956d
  |||:|||   0x00c99566      xor   al, al
  ========< 0x00c99568      jmp   0xc9965d
  --------> 0x00c9956d      push  eax
  |||:|||   0x00c9956e      mov   ecx, esi
  |||:|||   0x00c99570      call  0xda6b90
  |||:|||   0x00c99575      mov   esi, eax
  |||:|||   0x00c99577      cmp   dword [esi+0x0c], 0x00
  ========< 0x00c9957b      jz    0xc99657
  |||:|||   0x00c99581      mov   ecx, dword [0x201f660]               ; [0x201f660:4]=0
  |||:|||   0x00c99587      lea   eax, dword [ebp-0xa8]
  |||:|||   0x00c9958d      push  0x01                                 ; 1
  |||:|||   0x00c9958f      push  0x00
  |||:|||   0x00c99591      push  eax
  |||:|||   0x00c99592      mov   ecx, dword [ecx+0x1f8]
  |||:|||   0x00c99598      mov   dword [ebp-0xa8], ecx
  |||:|||   0x00c9959e      lea   ecx, dword [ebp-0x240]
  |||:|||   0x00c995a4      call  0xb0dfd0
  |||:|||   0x00c995a9      push  dword [esi+0x08]
  |||:|||   0x00c995ac      lea   ecx, dword [ebp-0x240]
  |||:|||   0x00c995b2      mov   byte [ebp-0x04], 0x78                ; 'x' ; 120
  |||:|||   0x00c995b6      call  0xa6c940
  |||:|||   0x00c995bb      mov   esi, eax
  |||:|||   0x00c995bd      test  esi, esi
  ========< 0x00c995bf      jz    0xc9964d
  |||:|||   0x00c995c5      mov   ecx, dword [ebp-0xb8]
  |||:|||   0x00c995cb      lea   eax, dword [ebp-0x128]
  |||:|||   0x00c995d1      push  eax
  |||:|||   0x00c995d2      call  0xdb1640
  |||:|||   0x00c995d7      lea   eax, dword [ebp-0x1cc]
  |||:|||   0x00c995dd      mov   byte [ebp-0x04], 0x79                ; 'y' ; 121
  |||:|||   0x00c995e1      push  eax
  |||:|||   0x00c995e2      mov   ecx, esi
  |||:|||   0x00c995e4      call  0x6e2140
  |||:|||   0x00c995e9      mov   ecx, dword [ebp-0x1cc]
  |||:|||   0x00c995ef      call  0xb014f0
  |||:|||   0x00c995f4      lea   ecx, dword [eax+0x24]
  |||:|||   0x00c995f7      call  0xb01560
  |||:|||   0x00c995fc      lea   ecx, dword [ebp-0x128]
  |||:|||   0x00c99602      mov   esi, eax
  |||:|||   0x00c99604      call  0xb014f0
  |||:|||   0x00c99609      mov   ecx, eax
  |||:|||   0x00c9960b      call  0xa73940
  |||:|||   0x00c99610      push  eax
  |||:|||   0x00c99611      mov   ecx, esi
  |||:|||   0x00c99613      call  0xb7ba70
  |||:|||   0x00c99618      test  al, al
  ========< 0x00c9961a      jnz   0xc99642
  |||:|||   0x00c9961c      lea   eax, dword [ebp-0x128]
  |||:|||   0x00c99622      push  eax
  |||:|||   0x00c99623      lea   ecx, dword [ebp-0x1cc]
  |||:|||   0x00c99629      call  0xc9ae00
  |||:|||   0x00c9962e      test  al, al
  ========< 0x00c99630      jz    0xc9963b
  |||:|||   0x00c99632      mov   byte [ebp-0x9a], 0x01
  ========< 0x00c99639      jmp   0xc99642
  --------> 0x00c9963b      mov   byte [ebp-0x99], 0x00
  --------> 0x00c99642      lea   ecx, dword [ebp-0x128]
  |||:|||   0x00c99648      call  0x4dc500
  --------> 0x00c9964d      mov   dword [ebp-0x240], 0x00
  --------> 0x00c99657      mov   al, byte [ebp-0x99]
  --------> 0x00c9965d      mov   dword [ebp-0x214], 0x00
  |||:|||   0x00c99667      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c9966b      test  al, al
  ========< 0x00c9966d      jz    0xc99790
  |||:|||   0x00c99673      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  |||:|||   0x00c99678      lea   ecx, dword [ebp-0x220]
  |||:|||   0x00c9967e      mov   esi, dword [0x201fc64]               ; [0x201fc64:4]=0
  |||:|||   0x00c99684      push  0x01                                 ; 1
  |||:|||   0x00c99686      push  0x00
  |||:|||   0x00c99688      mov   eax, dword [eax+0x1a4]
  |||:|||   0x00c9968e      mov   dword [ebp-0xa8], eax
  |||:|||   0x00c99694      lea   eax, dword [ebp-0xa8]
  |||:|||   0x00c9969a      push  eax
  |||:|||   0x00c9969b      call  0xb0dfd0
  |||:|||   0x00c996a0      push  edi
  |||:|||   0x00c996a1      lea   ecx, dword [ebp-0x220]
  |||:|||   0x00c996a7      mov   byte [ebp-0x04], 0x7c                ; '|' ; 124
  |||:|||   0x00c996ab      call  0xa6c940
  |||:|||   0x00c996b0      mov   dword [ebp-0xa8], eax
  |||:|||   0x00c996b6      xor   ecx, ecx
  |||:|||   0x00c996b8      mov   dword [ebp-0x50], 0x7f800000
  |||:|||   0x00c996bf      mov   dword [ebp-0x4c], 0x7f800000
  |||:|||   0x00c996c6      nop   word [eax+eax*1], ax
  --------> 0x00c996d0      movss xmm0, dword [ebp+ecx*1+0x28]
  |||:|||   0x00c996d6      ucomiss xmm0, dword [ebp+ecx*1-0x50]
  |||:|||   0x00c996db      lahf
  |||:|||   0x00c996dc      test  ah, 0x44                             ; 68
  ========< 0x00c996df      jp    0xc996f1
  |||:|||   0x00c996e1      add   ecx, 0x04
  |||:|||   0x00c996e4      cmp   ecx, 0x08                            ; 8
  ========< 0x00c996e7      jb    0xc996d0
  |||:|||   0x00c996e9      mov   eax, dword [ebp-0xb4]
  ========< 0x00c996ef      jmp   0xc996f4
  --------> 0x00c996f1      lea   eax, dword [ebp+0x28]
  --------> 0x00c996f4      movss xmm0, dword [eax]
  |||:|||   0x00c996f8      mov   ecx, esi
  |||:|||   0x00c996fa      movss dword [ebp-0x58], xmm0
  |||:|||   0x00c996ff      movss xmm0, dword [eax+0x04]
  |||:|||   0x00c99704      lea   eax, dword [ebp-0x58]
  |||:|||   0x00c99707      push  eax
  |||:|||   0x00c99708      movss dword [ebp-0x54], xmm0
  |||:|||   0x00c9970d      call  0xda51d0
  |||:|||   0x00c99712      cmp   byte [ebp-0x9a], 0x00
  |||:|||   0x00c99719      mov   esi, eax
  ========< 0x00c9971b      jnz   0xc99752
  |||:|||   0x00c9971d      mov   ecx, dword [ebp-0xa8]
  |||:|||   0x00c99723      call  0xc86860
  |||:|||   0x00c99728      test  al, al
  ========< 0x00c9972a      jz    0xc99737
  |||:|||   0x00c9972c      mov   eax, dword [ebp-0xa8]
  |||:|||   0x00c99732      cmp   dword [eax+0x10], esi
  ========< 0x00c99735      jz    0xc99752
  --------> 0x00c99737      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c9973d      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99740      push  edi
  |||:|||   0x00c99741      call  0xc94c10
  |||:|||   0x00c99746      mov   byte [ebp-0x04], 0x7d                ; '}' ; 125
  |||:|||   0x00c9974a      lea   ecx, dword [esi+0x244]
  ========< 0x00c99750      jmp   0xc9976b
  --------> 0x00c99752      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99758      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c9975b      push  edi
  |||:|||   0x00c9975c      call  0xc94c10
  |||:|||   0x00c99761      mov   byte [ebp-0x04], 0x7e                ; '~' ; 126
  |||:|||   0x00c99765      lea   ecx, dword [esi+0xb4]
  --------> 0x00c9976b      push  eax
  |||:|||   0x00c9976c      call  0xca2740
  |||:|||   0x00c99771      lea   ecx, dword [ebp-0x34]
  |||:|||   0x00c99774      call  0x4dc500
  |||:|||   0x00c99779      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c9977c      call  0x4dc500
  |||:|||   0x00c99781      mov   dword [ebp-0x220], 0x00
  ========< 0x00c9978b      jmp   0xc99c6c
  --------> 0x00c99790      lea   ecx, dword [ebp-0xd0]
  |||:|||   0x00c99796      mov   byte [ebp-0x99], 0x00
  |||:|||   0x00c9979d      call  0x4f6c50
  |||:|||   0x00c997a2      mov   ecx, dword [ebp-0xb8]
  |||:|||   0x00c997a8      lea   eax, dword [ebp-0xc8]
  |||:|||   0x00c997ae      push  eax
  |||:|||   0x00c997af      mov   byte [ebp-0x04], 0x80                ; 128
  |||:|||   0x00c997b3      call  0xdb1640
  |||:|||   0x00c997b8      cmp   dword [ebp-0xc8], 0xffffffff
  |||:|||   0x00c997bf      mov   byte [ebp-0x04], 0x81                ; 129
  ========< 0x00c997c3      jz    0xc998f3
  |||:|||   0x00c997c9      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  |||:|||   0x00c997ce      lea   ecx, dword [ebp-0x22c]
  |||:|||   0x00c997d4      push  0x01                                 ; 1
  |||:|||   0x00c997d6      push  0x00
  |||:|||   0x00c997d8      mov   eax, dword [eax+0x1ec]
  |||:|||   0x00c997de      mov   dword [ebp-0xa8], eax
  |||:|||   0x00c997e4      lea   eax, dword [ebp-0xa8]
  |||:|||   0x00c997ea      push  eax
  |||:|||   0x00c997eb      call  0xc94af0
  |||:|||   0x00c997f0      lea   eax, dword [ebp-0xc8]
  |||:|||   0x00c997f6      mov   byte [ebp-0x04], 0x82                ; 130
  |||:|||   0x00c997fa      push  eax
  |||:|||   0x00c997fb      lea   ecx, dword [ebp-0x22c]
  |||:|||   0x00c99801      call  0xa6c940
  |||:|||   0x00c99806      test  eax, eax
  ========< 0x00c99808      jz    0xc998a0
  |||:|||   0x00c9980e      mov   ecx, eax
  |||:|||   0x00c99810      call  0x518880
  |||:|||   0x00c99815      mov   esi, eax
  |||:|||   0x00c99817      cmp   dword [esi], 0xffffffff
  ========< 0x00c9981a      jz    0xc998a0
  |||:|||   0x00c99820      mov   ecx, dword [0x201f660]               ; [0x201f660:4]=0
  |||:|||   0x00c99826      xor   edx, edx
  |||:|||   0x00c99828      xor   eax, eax
  |||:|||   0x00c9982a      mov   byte [ebp-0x99], 0x01
  |||:|||   0x00c99831      mov   ecx, dword [ecx+0x148]
  |||:|||   0x00c99837      mov   dword [ebp-0x198], edx
  |||:|||   0x00c9983d      mov   dword [ebp-0x194], eax
  |||:|||   0x00c99843      mov   ecx, dword [ecx*4+0x2027ed0]
  |||:|||   0x00c9984a      mov   dword [ebp-0x19c], ecx
  |||:|||   0x00c99850      test  ecx, ecx
  ========< 0x00c99852      jz    0xc99873
  |||:|||   0x00c99854      mov   eax, dword [ecx]
  |||:|||   0x00c99856      push  edx
  |||:|||   0x00c99857      lea   edx, dword [ebp-0x198]
  |||:|||   0x00c9985d      push  edx
  |||:|||   0x00c9985e      call  dword [eax+0x3c]                     ; 60
  |||:|||   0x00c99861      mov   eax, dword [ebp-0x194]
  |||:|||   0x00c99867      mov   edx, dword [ebp-0x198]
  |||:|||   0x00c9986d      mov   ecx, dword [ebp-0x19c]
  --------> 0x00c99873      mov   byte [ebp-0x04], 0x83                ; 131
  |||:|||   0x00c99877      test  ecx, ecx
  ========< 0x00c99879      jz    0xc99896
  |||:|||   0x00c9987b      movzx ecx, word [esi]
  |||:|||   0x00c9987e      cmp   ecx, eax
  ========< 0x00c99880      jnb   0xc99896
  |||:|||   0x00c99882      mov   ecx, dword [edx+ecx*4]
  |||:|||   0x00c99885      test  ecx, ecx
  ========< 0x00c99887      jz    0xc99896
  |||:|||   0x00c99889      call  0x518880
  |||:|||   0x00c9988e      mov   eax, dword [eax]
  |||:|||   0x00c99890      mov   dword [ebp-0xd0], eax
  --------> 0x00c99896      mov   dword [ebp-0x19c], 0x00
  --------> 0x00c998a0      cmp   byte [ebp-0x99], 0x00
  |||:|||   0x00c998a7      mov   dword [ebp-0x22c], 0x00
  |||:|||   0x00c998b1      mov   byte [ebp-0x04], 0x81                ; 129
  ========< 0x00c998b5      jz    0xc998f3
  |||:|||   0x00c998b7      cmp   dword [ebp-0xd0], 0xffffffff
  |||:|||   0x00c998be      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c998c1      mov   esi, dword [ebp-0xa0]
  ========< 0x00c998c7      jz    0xc998e4
  |||:|||   0x00c998c9      lea   eax, dword [ebp-0xd0]
  |||:|||   0x00c998cf      push  eax
  |||:|||   0x00c998d0      call  0xc94c10
  |||:|||   0x00c998d5      mov   byte [ebp-0x04], 0x86                ; 134
  |||:|||   0x00c998d9      lea   ecx, dword [esi+0x118]
  ========< 0x00c998df      jmp   0xc99a6e
  --------> 0x00c998e4      push  edi
  |||:|||   0x00c998e5      call  0xc94c10
  |||:|||   0x00c998ea      mov   byte [ebp-0x04], 0x87                ; 135
  ========< 0x00c998ee      jmp   0xc99a68
  --------> 0x00c998f3      push  edi
  |||:|||   0x00c998f4      call  0xcc0210
  |||:|||   0x00c998f9      add   esp, 0x04
  |||:|||   0x00c998fc      push  edi
  |||:|||   0x00c998fd      test  al, al
  ========< 0x00c998ff      jz    0xc99a3b
  |||:|||   0x00c99905      lea   ecx, dword [ebp-0x114]
  |||:|||   0x00c9990b      call  0xa6c900
  |||:|||   0x00c99910      mov   esi, eax
  |||:|||   0x00c99912      lea   eax, dword [ebp-0x160]
  |||:|||   0x00c99918      push  eax
  |||:|||   0x00c99919      mov   ecx, esi
  |||:|||   0x00c9991b      call  0x6e2140
  |||:|||   0x00c99920      cmp   dword [eax+0x04], 0x00
  ========< 0x00c99924      jz    0xc99a84
  |||:|||   0x00c9992a      lea   eax, dword [ebp-0xc4]
  |||:|||   0x00c99930      mov   ecx, esi
  |||:|||   0x00c99932      push  eax
  |||:|||   0x00c99933      call  0xdb1640
  |||:|||   0x00c99938      lea   eax, dword [ebp-0xc4]
  |||:|||   0x00c9993e      mov   byte [ebp-0x04], 0x88                ; 136
  |||:|||   0x00c99942      push  eax
  |||:|||   0x00c99943      call  0xcc0380
  |||:|||   0x00c99948      add   esp, 0x04
  |||:|||   0x00c9994b      test  al, al
  ========< 0x00c9994d      jnz   0xc9996d
  |||:|||   0x00c9994f      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99955      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99958      push  edi
  |||:|||   0x00c99959      call  0xc94c10
  |||:|||   0x00c9995e      mov   byte [ebp-0x04], 0x89                ; 137
  |||:|||   0x00c99962      lea   ecx, dword [esi+0x294]
  ========< 0x00c99968      jmp   0xc99a1d
  --------> 0x00c9996d      mov   ecx, dword [0x201e2d8]               ; [0x201e2d8:4]=0
  |||:|||   0x00c99973      call  0xab0f80
  |||:|||   0x00c99978      test  eax, eax
  ========< 0x00c9997a      jz    0xc99a33
  |||:|||   0x00c99980      cmp   dword [eax+0x04], 0x02
  ========< 0x00c99984      jnz   0xc99a33
  |||:|||   0x00c9998a      push  dword [ebp-0xe8]
  |||:|||   0x00c99990      mov   ecx, eax
  |||:|||   0x00c99992      call  0xbc4ed0
  |||:|||   0x00c99997      test  al, al
  ========< 0x00c99999      jz    0xc99a04
  |||:|||   0x00c9999b      lea   eax, dword [ebp-0xc4]
  |||:|||   0x00c999a1      push  eax
  |||:|||   0x00c999a2      call  0xcc04b0
  |||:|||   0x00c999a7      add   esp, 0x04
  |||:|||   0x00c999aa      test  al, al
  ========< 0x00c999ac      jnz   0xc999ef
  |||:|||   0x00c999ae      lea   eax, dword [ebp-0xc4]
  |||:|||   0x00c999b4      push  eax
  |||:|||   0x00c999b5      call  0xcc0580
  |||:|||   0x00c999ba      add   esp, 0x04
  |||:|||   0x00c999bd      test  al, al
  ========< 0x00c999bf      jnz   0xc999ef
  |||:|||   0x00c999c1      lea   eax, dword [ebp-0xc4]
  |||:|||   0x00c999c7      push  eax
  |||:|||   0x00c999c8      call  0xcc0650
  |||:|||   0x00c999cd      add   esp, 0x04
  |||:|||   0x00c999d0      test  al, al
  ========< 0x00c999d2      jnz   0xc999ef
  |||:|||   0x00c999d4      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c999da      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c999dd      push  edi
  |||:|||   0x00c999de      call  0xc94c10
  |||:|||   0x00c999e3      mov   byte [ebp-0x04], 0x8a                ; 138
  |||:|||   0x00c999e7      lea   ecx, dword [esi+0x280]
  ========< 0x00c999ed      jmp   0xc99a1d
  --------> 0x00c999ef      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c999f5      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c999f8      push  edi
  |||:|||   0x00c999f9      call  0xc94c10
  |||:|||   0x00c999fe      mov   byte [ebp-0x04], 0x8b                ; 139
  ========< 0x00c99a02      jmp   0xc99a17
  --------> 0x00c99a04      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99a0a      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99a0d      push  edi
  |||:|||   0x00c99a0e      call  0xc94c10
  |||:|||   0x00c99a13      mov   byte [ebp-0x04], 0x8c                ; 140
  --------> 0x00c99a17      lea   ecx, dword [esi+0xb4]
  --------> 0x00c99a1d      push  eax
  |||:|||   0x00c99a1e      call  0xca2740
  |||:|||   0x00c99a23      lea   ecx, dword [ebp-0x34]
  |||:|||   0x00c99a26      call  0x4dc500
  |||:|||   0x00c99a2b      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99a2e      call  0x4dc500
  --------> 0x00c99a33      lea   ecx, dword [ebp-0xc4]
  ========< 0x00c99a39      jmp   0xc99a7f
  --------> 0x00c99a3b      call  0xca0620
  |||:|||   0x00c99a40      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99a46      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99a49      add   esp, 0x04
  |||:|||   0x00c99a4c      push  edi
  |||:|||   0x00c99a4d      test  al, al
  ========< 0x00c99a4f      jz    0xc99a5f
  |||:|||   0x00c99a51      call  0xc94c10
  |||:|||   0x00c99a56      mov   byte [ebp-0x04], 0x8f                ; 143
  |||:|||   0x00c99a5a      lea   ecx, dword [esi+0x50]
  ========< 0x00c99a5d      jmp   0xc99a6e
  --------> 0x00c99a5f      call  0xc94c10
  |||:|||   0x00c99a64      mov   byte [ebp-0x04], 0x90                ; 144
  --------> 0x00c99a68      lea   ecx, dword [esi+0xb4]
  --------> 0x00c99a6e      push  eax
  |||:|||   0x00c99a6f      call  0xca2740
  |||:|||   0x00c99a74      lea   ecx, dword [ebp-0x34]
  |||:|||   0x00c99a77      call  0x4dc500
  |||:|||   0x00c99a7c      lea   ecx, dword [ebp-0x38]
  --------> 0x00c99a7f      call  0x4dc500
  --------> 0x00c99a84      lea   ecx, dword [ebp-0xc8]
  |||:|||   0x00c99a8a      call  0x4dc500
  |||:|||   0x00c99a8f      lea   ecx, dword [ebp-0xd0]
  |||:|||   0x00c99a95      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  |||:|||   0x00c99a99      call  0x4dc500
  ========< 0x00c99a9e      jmp   0xc99c70
  --`-----> 0x00c99aa3      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  || :|||   0x00c99aa8      lea   ecx, dword [ebp-0x170]
  || :|||   0x00c99aae      push  0x01                                 ; 1
  || :|||   0x00c99ab0      push  0x00
  || :|||   0x00c99ab2      mov   eax, dword [eax+0x1a4]
  || :|||   0x00c99ab8      mov   dword [ebp-0xa8], eax
  || :|||   0x00c99abe      lea   eax, dword [ebp-0xa8]
  || :|||   0x00c99ac4      push  eax
  || :|||   0x00c99ac5      call  0xb0dfd0
  || :|||   0x00c99aca      push  edi
  || :|||   0x00c99acb      lea   ecx, dword [ebp-0x170]
  || :|||   0x00c99ad1      mov   byte [ebp-0x04], 0x3d                ; '=' ; 61
  || :|||   0x00c99ad5      call  0xa6c940
  || :|||   0x00c99ada      mov   dword [ebp-0xa8], eax
  || :|||   0x00c99ae0      test  eax, eax
  ||,=====< 0x00c99ae2      jnz   0xc99b20
  |||:|||   0x00c99ae4      push  edi
  |||:|||   0x00c99ae5      call  0xca0620
  |||:|||   0x00c99aea      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99af0      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99af3      add   esp, 0x04
  |||:|||   0x00c99af6      push  edi
  |||:|||   0x00c99af7      test  al, al
  ========< 0x00c99af9      jz    0xc99b0c
  |||:|||   0x00c99afb      call  0xc94c10
  |||:|||   0x00c99b00      mov   byte [ebp-0x04], 0x3e                ; '>' ; 62
  |||:|||   0x00c99b04      lea   ecx, dword [esi+0x50]
  ========< 0x00c99b07      jmp   0xc99c4c
  --------> 0x00c99b0c      call  0xc94c10
  |||:|||   0x00c99b11      mov   byte [ebp-0x04], 0x3f                ; '?' ; 63
  |||:|||   0x00c99b15      lea   ecx, dword [esi+0xb4]
  ========< 0x00c99b1b      jmp   0xc99c4c
  ||`-----> 0x00c99b20      mov   dword [ebp-0x60], 0x7f800000
  || :|||   0x00c99b27      xor   ecx, ecx
  || :|||   0x00c99b29      mov   dword [ebp-0x5c], 0x7f800000
  ||.-----> 0x00c99b30      movss xmm0, dword [ebp+ecx*1+0x28]
  ||::|||   0x00c99b36      ucomiss xmm0, dword [ebp+ecx*1-0x60]
  ||::|||   0x00c99b3b      lahf
  ||::|||   0x00c99b3c      test  ah, 0x44                             ; 68
  ========< 0x00c99b3f      jp    0xc99b51
  ||::|||   0x00c99b41      add   ecx, 0x04
  ||::|||   0x00c99b44      cmp   ecx, 0x08                            ; 8
  ||`=====< 0x00c99b47      jb    0xc99b30
  || :|||   0x00c99b49      mov   eax, dword [ebp-0xb4]
  ||,=====< 0x00c99b4f      jmp   0xc99b54
  --------> 0x00c99b51      lea   eax, dword [ebp+0x28]
  ||`-----> 0x00c99b54      movss xmm0, dword [eax]
  || :|||   0x00c99b58      mov   ecx, dword [0x201fc64]               ; [0x201fc64:4]=0
  || :|||   0x00c99b5e      movss dword [ebp-0x40], xmm0
  || :|||   0x00c99b63      movss xmm0, dword [eax+0x04]
  || :|||   0x00c99b68      lea   eax, dword [ebp-0x40]
  || :|||   0x00c99b6b      push  eax
  || :|||   0x00c99b6c      movss dword [ebp-0x3c], xmm0
  || :|||   0x00c99b71      call  0xda51d0
  || :|||   0x00c99b76      mov   esi, eax
  || :|||   0x00c99b78      test  esi, esi
  ||,=====< 0x00c99b7a      js    0xc99c2d
  |||:|||   0x00c99b80      mov   ecx, dword [ebp-0xa8]
  |||:|||   0x00c99b86      push  0x00
  |||:|||   0x00c99b88      push  esi
  |||:|||   0x00c99b89      call  0xc7d860
  |||:|||   0x00c99b8e      test  al, al
  ========< 0x00c99b90      jz    0xc99c2d
  |||:|||   0x00c99b96      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
  |||:|||   0x00c99b9b      lea   ecx, dword [ebp-0x1f0]
  |||:|||   0x00c99ba1      push  0x01                                 ; 1
  |||:|||   0x00c99ba3      push  0x00
  |||:|||   0x00c99ba5      mov   eax, dword [eax+0x1a4]
  |||:|||   0x00c99bab      mov   dword [ebp-0xa8], eax
  |||:|||   0x00c99bb1      lea   eax, dword [ebp-0xa8]
  |||:|||   0x00c99bb7      push  eax
  |||:|||   0x00c99bb8      call  0xb0dfd0
  |||:|||   0x00c99bbd      push  edi
  |||:|||   0x00c99bbe      lea   ecx, dword [ebp-0x1f0]
  |||:|||   0x00c99bc4      mov   byte [ebp-0x04], 0x40                ; '@' ; 64
  |||:|||   0x00c99bc8      call  0xa6c940
  |||:|||   0x00c99bcd      mov   ecx, eax
  |||:|||   0x00c99bcf      mov   dword [ebp-0xa8], eax
  |||:|||   0x00c99bd5      call  0xc86860
  |||:|||   0x00c99bda      test  al, al
  ========< 0x00c99bdc      jz    0xc99be9
  |||:|||   0x00c99bde      mov   eax, dword [ebp-0xa8]
  |||:|||   0x00c99be4      cmp   dword [eax+0x10], esi
  ========< 0x00c99be7      jz    0xc99c18
  --------> 0x00c99be9      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99bef      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99bf2      push  edi
  |||:|||   0x00c99bf3      call  0xc94c10
  |||:|||   0x00c99bf8      push  eax
  |||:|||   0x00c99bf9      lea   ecx, dword [esi+0x244]
  |||:|||   0x00c99bff      mov   byte [ebp-0x04], 0x41                ; 'A' ; 65
  |||:|||   0x00c99c03      call  0xca2740
  |||:|||   0x00c99c08      lea   ecx, dword [ebp-0x34]
  |||:|||   0x00c99c0b      call  0x4dc500
  |||:|||   0x00c99c10      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99c13      call  0x4dc500
  --------> 0x00c99c18      cmp   dword [ebp-0x1f0], 0x00
  ========< 0x00c99c1f      jz    0xc99c62
  |||:|||   0x00c99c21      mov   dword [ebp-0x1f0], 0x00
  ========< 0x00c99c2b      jmp   0xc99c62
  --`-----> 0x00c99c2d      cmp   byte [ebp+0x20], 0x00
  ||,=====< 0x00c99c31      jz    0xc99c62
  |||:|||   0x00c99c33      mov   esi, dword [ebp-0xa0]
  |||:|||   0x00c99c39      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99c3c      push  edi
  |||:|||   0x00c99c3d      call  0xc94c10
  |||:|||   0x00c99c42      mov   byte [ebp-0x04], 0x43                ; 'C' ; 67
  |||:|||   0x00c99c46      lea   ecx, dword [esi+0xdc]
  --------> 0x00c99c4c      push  eax
  |||:|||   0x00c99c4d      call  0xca2740
  |||:|||   0x00c99c52      lea   ecx, dword [ebp-0x34]
  |||:|||   0x00c99c55      call  0x4dc500
  |||:|||   0x00c99c5a      lea   ecx, dword [ebp-0x38]
  |||:|||   0x00c99c5d      call  0x4dc500
  --`-----> 0x00c99c62      mov   dword [ebp-0x170], 0x00
  --------> 0x00c99c6c      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
  `-------> 0x00c99c70      mov   ecx, dword [ebp-0xd4]
   | :|||   0x00c99c76      inc   ecx
   | :|||   0x00c99c77      mov   dword [ebp-0xd4], ecx
   | :|||   0x00c99c7d      cmp   ecx, dword [ebp-0x130]
   | `====< 0x00c99c83      jb    0xc97aa0
   |  |`--> 0x00c99c89      push  dword [ebp-0xc0]
   |  | |   0x00c99c8f      mov   esi, dword [ebp-0xa0]
   |  | |   0x00c99c95      push  esi
   |  | |   0x00c99c96      call  0xc9aa40
   |  | |   0x00c99c9b      xor   edx, edx
   |  | |   0x00c99c9d      add   esp, 0x08
   |  | |   0x00c99ca0      cmp   dword [esi+0x60], edx
   |  |,==< 0x00c99ca3      jbe   0xc99cdf
   |  |||   0x00c99ca5      mov   edi, dword [esi+0x5c]
   |  |||   0x00c99ca8      xor   ecx, ecx
   |  |||   0x00c99caa      nop   word [eax+eax*1], ax
   | .----> 0x00c99cb0      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c99cb6      lea   ecx, dword [ecx+0x14]
   | :|||   0x00c99cb9      inc   edx
   | :|||   0x00c99cba      mov   eax, dword [eax]
   | :|||   0x00c99cbc      mov   dword [edi+ecx*1-0x0c], eax
   | :|||   0x00c99cc0      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c99cc6      mov   eax, dword [eax+0x04]
   | :|||   0x00c99cc9      mov   dword [edi+ecx*1-0x08], eax
   | :|||   0x00c99ccd      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c99cd3      mov   eax, dword [eax+0x08]
   | :|||   0x00c99cd6      mov   dword [edi+ecx*1-0x04], eax
   | :|||   0x00c99cda      cmp   edx, dword [esi+0x60]
   | `====< 0x00c99cdd      jb    0xc99cb0
   |  |`--> 0x00c99cdf      xor   edx, edx
   |  | |   0x00c99ce1      cmp   dword [esi+0x2a4], edx
   |  |,==< 0x00c99ce7      jbe   0xc99d23
   |  |||   0x00c99ce9      mov   edi, dword [esi+0x2a0]
   |  |||   0x00c99cef      xor   ecx, ecx
   | .----> 0x00c99cf1      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c99cf7      lea   ecx, dword [ecx+0x14]
   | :|||   0x00c99cfa      inc   edx
   | :|||   0x00c99cfb      mov   eax, dword [eax]
   | :|||   0x00c99cfd      mov   dword [edi+ecx*1-0x0c], eax
   | :|||   0x00c99d01      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c99d07      mov   eax, dword [eax+0x04]
   | :|||   0x00c99d0a      mov   dword [edi+ecx*1-0x08], eax
   | :|||   0x00c99d0e      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c99d14      mov   eax, dword [eax+0x08]
   | :|||   0x00c99d17      mov   dword [edi+ecx*1-0x04], eax
   | :|||   0x00c99d1b      cmp   edx, dword [esi+0x2a4]
   | `====< 0x00c99d21      jb    0xc99cf1
   |  |`--> 0x00c99d23      xor   edi, edi
   |  | |   0x00c99d25      cmp   dword [esi+0x88], edi
   |  |,==< 0x00c99d2b      jbe   0xc99d57
   |  |||   0x00c99d2d      xor   edx, edx
   |  |||   0x00c99d2f      nop
   | .----> 0x00c99d30      mov   ecx, dword [esi+0x84]
   | :|||   0x00c99d36      cmp   dword [ecx+edx*1+0x04], 0xffffffff
   |,=====< 0x00c99d3b      jnz   0xc99d4b
   ||:|||   0x00c99d3d      mov   eax, dword [ebp-0xc0]
   ||:|||   0x00c99d43      mov   eax, dword [eax]
   ||:|||   0x00c99d45      mov   eax, dword [eax]
   ||:|||   0x00c99d47      mov   dword [ecx+edx*1+0x04], eax
   |`-----> 0x00c99d4b      inc   edi
   | :|||   0x00c99d4c      add   edx, 0x14                            ; 20
   | :|||   0x00c99d4f      cmp   edi, dword [esi+0x88]
   | `====< 0x00c99d55      jb    0xc99d30
   |  |`--> 0x00c99d57      xor   edi, edi
   |  | |   0x00c99d59      cmp   dword [esi+0x2f4], edi
   |  |,==< 0x00c99d5f      jbe   0xc99d8a
   |  |||   0x00c99d61      xor   edx, edx
   | .----> 0x00c99d63      mov   ecx, dword [esi+0x2f0]
   | :|||   0x00c99d69      cmp   dword [ecx+edx*1+0x04], 0xffffffff
   |,=====< 0x00c99d6e      jnz   0xc99d7e
   ||:|||   0x00c99d70      mov   eax, dword [ebp-0xc0]
   ||:|||   0x00c99d76      mov   eax, dword [eax]
   ||:|||   0x00c99d78      mov   eax, dword [eax]
   ||:|||   0x00c99d7a      mov   dword [ecx+edx*1+0x04], eax
   |`-----> 0x00c99d7e      inc   edi
   | :|||   0x00c99d7f      add   edx, 0x14                            ; 20
   | :|||   0x00c99d82      cmp   edi, dword [esi+0x2f4]
   | `====< 0x00c99d88      jb    0xc99d63
   |  |`--> 0x00c99d8a      xor   edi, edi
   |  | |   0x00c99d8c      cmp   dword [esi+0x2b8], edi
   |  |,==< 0x00c99d92      jbe   0xc99dc7
   |  |||   0x00c99d94      xor   edx, edx
   |  |||   0x00c99d96      nop   word [eax+eax*1], ax
   | .----> 0x00c99da0      mov   ecx, dword [esi+0x2b4]
   | :|||   0x00c99da6      cmp   dword [ecx+edx*1+0x04], 0xffffffff
   |,=====< 0x00c99dab      jnz   0xc99dbb
   ||:|||   0x00c99dad      mov   eax, dword [ebp-0xc0]
   ||:|||   0x00c99db3      mov   eax, dword [eax]
   ||:|||   0x00c99db5      mov   eax, dword [eax]
   ||:|||   0x00c99db7      mov   dword [ecx+edx*1+0x04], eax
   |`-----> 0x00c99dbb      inc   edi
   | :|||   0x00c99dbc      add   edx, 0x14                            ; 20
   | :|||   0x00c99dbf      cmp   edi, dword [esi+0x2b8]
   | `====< 0x00c99dc5      jb    0xc99da0
   |  |`--> 0x00c99dc7      xor   edi, edi
   |  | |   0x00c99dc9      cmp   dword [esi+0x100], edi
   |  |,==< 0x00c99dcf      jbe   0xc99dfa
   |  |||   0x00c99dd1      xor   edx, edx
   | .----> 0x00c99dd3      mov   ecx, dword [esi+0xfc]
   | :|||   0x00c99dd9      cmp   dword [ecx+edx*1+0x04], 0xffffffff
   |,=====< 0x00c99dde      jnz   0xc99dee
   ||:|||   0x00c99de0      mov   eax, dword [ebp-0xc0]
   ||:|||   0x00c99de6      mov   eax, dword [eax]
   ||:|||   0x00c99de8      mov   eax, dword [eax]
   ||:|||   0x00c99dea      mov   dword [ecx+edx*1+0x04], eax
   |`-----> 0x00c99dee      inc   edi
   | :|||   0x00c99def      add   edx, 0x14                            ; 20
   | :|||   0x00c99df2      cmp   edi, dword [esi+0x100]
   | `====< 0x00c99df8      jb    0xc99dd3
   |  |`--> 0x00c99dfa      xor   edx, edx
   |  | |   0x00c99dfc      cmp   dword [esi+0x128], edx
   |  |,==< 0x00c99e02      jbe   0xc99e42
   |  |||   0x00c99e04      mov   edi, dword [esi+0x124]
   |  |||   0x00c99e0a      xor   ecx, ecx
   |  |||   0x00c99e0c      nop   dword [eax], eax
   | .----> 0x00c99e10      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c99e16      lea   ecx, dword [ecx+0x14]
   | :|||   0x00c99e19      inc   edx
   | :|||   0x00c99e1a      mov   eax, dword [eax]
   | :|||   0x00c99e1c      mov   dword [edi+ecx*1-0x0c], eax
   | :|||   0x00c99e20      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c99e26      mov   eax, dword [eax+0x04]
   | :|||   0x00c99e29      mov   dword [edi+ecx*1-0x08], eax
   | :|||   0x00c99e2d      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c99e33      mov   eax, dword [eax+0x08]
   | :|||   0x00c99e36      mov   dword [edi+ecx*1-0x04], eax
   | :|||   0x00c99e3a      cmp   edx, dword [esi+0x128]
   | `====< 0x00c99e40      jb    0xc99e10
   |  |`--> 0x00c99e42      xor   edi, edi
   |  | |   0x00c99e44      cmp   dword [esi+0x114], edi
   |  |,==< 0x00c99e4a      jbe   0xc99e77
   |  |||   0x00c99e4c      xor   edx, edx
   |  |||   0x00c99e4e      nop
   | .----> 0x00c99e50      mov   ecx, dword [esi+0x110]
   | :|||   0x00c99e56      cmp   dword [ecx+edx*1+0x04], 0xffffffff
   |,=====< 0x00c99e5b      jnz   0xc99e6b
   ||:|||   0x00c99e5d      mov   eax, dword [ebp-0xc0]
   ||:|||   0x00c99e63      mov   eax, dword [eax]
   ||:|||   0x00c99e65      mov   eax, dword [eax]
   ||:|||   0x00c99e67      mov   dword [ecx+edx*1+0x04], eax
   |`-----> 0x00c99e6b      inc   edi
   | :|||   0x00c99e6c      add   edx, 0x14                            ; 20
   | :|||   0x00c99e6f      cmp   edi, dword [esi+0x114]
   | `====< 0x00c99e75      jb    0xc99e50
   |  |`--> 0x00c99e77      xor   edx, edx
   |  | |   0x00c99e79      cmp   dword [esi+0x150], edx
   |  |,==< 0x00c99e7f      jbe   0xc99ec2
   |  |||   0x00c99e81      mov   edi, dword [esi+0x14c]
   |  |||   0x00c99e87      xor   ecx, ecx
   |  |||   0x00c99e89      nop   dword [eax], eax
   | .----> 0x00c99e90      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c99e96      lea   ecx, dword [ecx+0x14]
   | :|||   0x00c99e99      inc   edx
   | :|||   0x00c99e9a      mov   eax, dword [eax]
   | :|||   0x00c99e9c      mov   dword [ecx+edi*1-0x0c], eax
   | :|||   0x00c99ea0      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c99ea6      mov   eax, dword [eax+0x04]
   | :|||   0x00c99ea9      mov   dword [ecx+edi*1-0x08], eax
   | :|||   0x00c99ead      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c99eb3      mov   eax, dword [eax+0x08]
   | :|||   0x00c99eb6      mov   dword [ecx+edi*1-0x04], eax
   | :|||   0x00c99eba      cmp   edx, dword [esi+0x150]
   | `====< 0x00c99ec0      jb    0xc99e90
   |  |`--> 0x00c99ec2      mov   eax, dword [ebp-0xc0]
   |  | |   0x00c99ec8      cmp   dword [eax+0x04], 0x00
   |  |,==< 0x00c99ecc      jz    0xc99f07
   |  |||   0x00c99ece      xor   edx, edx
   |  |||   0x00c99ed0      cmp   dword [esi+0x1a0], edx
   | ,====< 0x00c99ed6      jbe   0xc99f07
   | ||||   0x00c99ed8      xor   edi, edi
   | ||||   0x00c99eda      nop   word [eax+eax*1], ax
   |.-----> 0x00c99ee0      mov   ecx, dword [esi+0x19c]
   |:||||   0x00c99ee6      cmp   dword [ecx+edi*1+0x04], 0xffffffff
  ,=======< 0x00c99eeb      jnz   0xc99efb
  ||:||||   0x00c99eed      mov   eax, dword [eax]
  ||:||||   0x00c99eef      mov   eax, dword [eax]
  ||:||||   0x00c99ef1      mov   dword [ecx+edi*1+0x04], eax
  ||:||||   0x00c99ef5      mov   eax, dword [ebp-0xc0]
  `-------> 0x00c99efb      inc   edx
   |:||||   0x00c99efc      add   edi, 0x14                            ; 20
   |:||||   0x00c99eff      cmp   edx, dword [esi+0x1a0]
   |`=====< 0x00c99f05      jb    0xc99ee0
   | `-`--> 0x00c99f07      xor   edx, edx
   |  | |   0x00c99f09      cmp   dword [esi+0x1b4], edx
   |  |,==< 0x00c99f0f      jbe   0xc99f3a
   |  |||   0x00c99f11      xor   edi, edi
   | .----> 0x00c99f13      mov   ecx, dword [esi+0x1b0]
   | :|||   0x00c99f19      cmp   dword [ecx+edi*1+0x04], 0xffffffff
   |,=====< 0x00c99f1e      jnz   0xc99f28
   ||:|||   0x00c99f20      mov   eax, dword [eax]
   ||:|||   0x00c99f22      mov   eax, dword [eax]
   ||:|||   0x00c99f24      mov   dword [ecx+edi*1+0x04], eax
   |`-----> 0x00c99f28      mov   eax, dword [ebp-0xc0]
   | :|||   0x00c99f2e      inc   edx
   | :|||   0x00c99f2f      add   edi, 0x14                            ; 20
   | :|||   0x00c99f32      cmp   edx, dword [esi+0x1b4]
   | `====< 0x00c99f38      jb    0xc99f13
   |  |`--> 0x00c99f3a      xor   edx, edx
   |  | |   0x00c99f3c      cmp   dword [esi+0x1c8], edx
   |  |,==< 0x00c99f42      jbe   0xc99f77
   |  |||   0x00c99f44      xor   edi, edi
   |  |||   0x00c99f46      nop   word [eax+eax*1], ax
   | .----> 0x00c99f50      mov   ecx, dword [esi+0x1c4]
   | :|||   0x00c99f56      cmp   dword [ecx+edi*1+0x04], 0xffffffff
   |,=====< 0x00c99f5b      jnz   0xc99f6b
   ||:|||   0x00c99f5d      mov   eax, dword [ebp-0xc0]
   ||:|||   0x00c99f63      mov   eax, dword [eax]
   ||:|||   0x00c99f65      mov   eax, dword [eax]
   ||:|||   0x00c99f67      mov   dword [ecx+edi*1+0x04], eax
   |`-----> 0x00c99f6b      inc   edx
   | :|||   0x00c99f6c      add   edi, 0x14                            ; 20
   | :|||   0x00c99f6f      cmp   edx, dword [esi+0x1c8]
   | `====< 0x00c99f75      jb    0xc99f50
   |  |`--> 0x00c99f77      xor   edx, edx
   |  | |   0x00c99f79      cmp   dword [esi+0x1dc], edx
   |  |,==< 0x00c99f7f      jbe   0xc99faa
   |  |||   0x00c99f81      xor   edi, edi
   | .----> 0x00c99f83      mov   ecx, dword [esi+0x1d8]
   | :|||   0x00c99f89      cmp   dword [ecx+edi*1+0x04], 0xffffffff
   |,=====< 0x00c99f8e      jnz   0xc99f9e
   ||:|||   0x00c99f90      mov   eax, dword [ebp-0xc0]
   ||:|||   0x00c99f96      mov   eax, dword [eax]
   ||:|||   0x00c99f98      mov   eax, dword [eax]
   ||:|||   0x00c99f9a      mov   dword [ecx+edi*1+0x04], eax
   |`-----> 0x00c99f9e      inc   edx
   | :|||   0x00c99f9f      add   edi, 0x14                            ; 20
   | :|||   0x00c99fa2      cmp   edx, dword [esi+0x1dc]
   | `====< 0x00c99fa8      jb    0xc99f83
   |  |`--> 0x00c99faa      cmp   dword [esi+0x254], 0x00
   |  |,==< 0x00c99fb1      jnz   0xc99fc0
   |  |||   0x00c99fb3      cmp   dword [esi+0x27c], 0x00
   | ,====< 0x00c99fba      jnz   0xc99fc0
   | ||||   0x00c99fbc      xor   al, al
   |,=====< 0x00c99fbe      jmp   0xc99fc2
   ||`-`--> 0x00c99fc0      mov   al, 0x01
   |`-----> 0x00c99fc2      mov   ecx, dword [ebp-0xcc]
   |  | |   0x00c99fc8      mov   ecx, dword [ecx+0x10]
   |  | |   0x00c99fcb      cmp   ecx, 0x1d                            ; 29
   |  |,==< 0x00c99fce      jz    0xc99fd5
   |  |||   0x00c99fd0      cmp   ecx, 0x1f                            ; 31
   | ,====< 0x00c99fd3      jnz   0xc9a01e
   | ||`--> 0x00c99fd5      test  al, al
   | ||,==< 0x00c99fd7      jnz   0xc9a01e
   | ||||   0x00c99fd9      lea   edi, dword [esi+0x5c]
   | ||||   0x00c99fdc      cmp   byte [ebp+0x20], al
   |,=====< 0x00c99fdf      jz    0xc9a017
   ||||||   0x00c99fe1      mov   eax, dword [edi+0x04]
   ||||||   0x00c99fe4      lea   ecx, dword [esi+0xdc]
   ||||||   0x00c99fea      mov   edx, dword [edi]
   ||||||   0x00c99fec      mov   dword [ebp-0x124], edx
   ||||||   0x00c99ff2      lea   eax, dword [eax+eax*4]
   ||||||   0x00c99ff5      lea   eax, dword [edx+eax*4]
   ||||||   0x00c99ff8      mov   dword [ebp-0x120], eax
   ||||||   0x00c99ffe      lea   eax, dword [ebp-0x120]
   ||||||   0x00c9a004      push  eax
   ||||||   0x00c9a005      lea   eax, dword [ebp-0x124]
   ||||||   0x00c9a00b      push  eax
   ||||||   0x00c9a00c      push  dword [esi+0xec]
   ||||||   0x00c9a012      call  0xc94720
   |`-----> 0x00c9a017      mov   ecx, edi
   | ||||   0x00c9a019      call  0xbe2820
   | `-`--> 0x00c9a01e      xor   edx, edx
   |  | |   0x00c9a020      cmp   dword [esi+0x254], edx
   |  |,==< 0x00c9a026      jbe   0xc9a062
   |  |||   0x00c9a028      mov   edi, dword [esi+0x250]
   |  |||   0x00c9a02e      xor   ecx, ecx
   | .----> 0x00c9a030      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c9a036      lea   ecx, dword [ecx+0x14]
   | :|||   0x00c9a039      inc   edx
   | :|||   0x00c9a03a      mov   eax, dword [eax]
   | :|||   0x00c9a03c      mov   dword [ecx+edi*1-0x0c], eax
   | :|||   0x00c9a040      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c9a046      mov   eax, dword [eax+0x04]
   | :|||   0x00c9a049      mov   dword [ecx+edi*1-0x08], eax
   | :|||   0x00c9a04d      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c9a053      mov   eax, dword [eax+0x08]
   | :|||   0x00c9a056      mov   dword [ecx+edi*1-0x04], eax
   | :|||   0x00c9a05a      cmp   edx, dword [esi+0x254]
   | `====< 0x00c9a060      jb    0xc9a030
   |  |`--> 0x00c9a062      xor   edx, edx
   |  | |   0x00c9a064      cmp   dword [esi+0x27c], edx
   |  |,==< 0x00c9a06a      jbe   0xc9a097
   |  |||   0x00c9a06c      xor   edi, edi
   |  |||   0x00c9a06e      nop
   | .----> 0x00c9a070      mov   ecx, dword [esi+0x278]
   | :|||   0x00c9a076      cmp   dword [ecx+edi*1+0x04], 0xffffffff
   |,=====< 0x00c9a07b      jnz   0xc9a08b
   ||:|||   0x00c9a07d      mov   eax, dword [ebp-0xc0]
   ||:|||   0x00c9a083      mov   eax, dword [eax]
   ||:|||   0x00c9a085      mov   eax, dword [eax]
   ||:|||   0x00c9a087      mov   dword [ecx+edi*1+0x04], eax
   |`-----> 0x00c9a08b      inc   edx
   | :|||   0x00c9a08c      add   edi, 0x14                            ; 20
   | :|||   0x00c9a08f      cmp   edx, dword [esi+0x27c]
   | `====< 0x00c9a095      jb    0xc9a070
   |  |`--> 0x00c9a097      xor   edx, edx
   |  | |   0x00c9a099      cmp   dword [esi+0x268], edx
   |  |,==< 0x00c9a09f      jbe   0xc9a0e2
   |  |||   0x00c9a0a1      mov   edi, dword [esi+0x264]
   |  |||   0x00c9a0a7      xor   ecx, ecx
   |  |||   0x00c9a0a9      nop   dword [eax], eax
   | .----> 0x00c9a0b0      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c9a0b6      lea   ecx, dword [ecx+0x14]
   | :|||   0x00c9a0b9      inc   edx
   | :|||   0x00c9a0ba      mov   eax, dword [eax]
   | :|||   0x00c9a0bc      mov   dword [ecx+edi*1-0x0c], eax
   | :|||   0x00c9a0c0      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c9a0c6      mov   eax, dword [eax+0x04]
   | :|||   0x00c9a0c9      mov   dword [ecx+edi*1-0x08], eax
   | :|||   0x00c9a0cd      mov   eax, dword [ebp-0xb4]
   | :|||   0x00c9a0d3      mov   eax, dword [eax+0x08]
   | :|||   0x00c9a0d6      mov   dword [ecx+edi*1-0x04], eax
   | :|||   0x00c9a0da      cmp   edx, dword [esi+0x268]
   | `====< 0x00c9a0e0      jb    0xc9a0b0
   |  |`--> 0x00c9a0e2      lea   ecx, dword [ebp-0xec]
   |  | |   0x00c9a0e8      call  0x4dc500
   |  | `-> 0x00c9a0ed      mov   eax, dword [ebp-0xf0]
   |  |     0x00c9a0f3      cmp   dword [eax+0x10], 0x00
   |  |     0x00c9a0f7      setz  byte [ebp-0x99]
   |  `---> 0x00c9a0fe      lea   ecx, dword [ebp-0x13c]
   |        0x00c9a104      call  0xa9e320
   `------> 0x00c9a109      lea   ecx, dword [ebp-0xac]
            0x00c9a10f      call  0x4dc500
            0x00c9a114      mov   al, byte [ebp-0x99]
            0x00c9a11a      lea   esp, dword [ebp-0x25c]
            0x00c9a120      mov   ecx, dword [ebp-0x0c]
            0x00c9a123      mov   dword fs:[0x0], ecx
            0x00c9a12a      pop   ecx
            0x00c9a12b      pop   edi
            0x00c9a12c      pop   esi
            0x00c9a12d      mov   ecx, dword [ebp-0x10]
            0x00c9a130      xor   ecx, ebp
            0x00c9a132      call  0x18075f6
            0x00c9a137      mov   esp, ebp
            0x00c9a139      pop   ebp
            0x00c9a13a      ret
            0x00c9a13b      int3
            0x00c9a13c      int3
            0x00c9a13d      int3
            0x00c9a13e      int3
            0x00c9a13f      int3
            0x00c9a140      push  ebp
            0x00c9a141      mov   ebp, esp
            0x00c9a143      push  0xffffffff                           ; 255
            0x00c9a145      push  0x187e160
            0x00c9a14a      mov   eax, dword fs:[0x0]
            0x00c9a150      push  eax
            0x00c9a151      sub   esp, 0x1c
            0x00c9a154      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00c9a159      xor   eax, ebp
            0x00c9a15b      mov   dword [ebp-0x10], eax
            0x00c9a15e      push  ebx
            0x00c9a15f      push  esi
            0x00c9a160      push  edi
            0x00c9a161      push  eax
            0x00c9a162      lea   eax, dword [ebp-0x0c]
            0x00c9a165      mov   dword fs:[0x0], eax
            0x00c9a16b      mov   edi, dword [ebp+0x20]
            0x00c9a16e      mov   esi, dword [ebp+0x0c]
            0x00c9a171      mov   dword [ebp-0x28], edi
            0x00c9a174      lea   eax, dword [ebp+0x10]
            0x00c9a177      mov   dword [ebp-0x04], 0x00
            0x00c9a17e      push  eax
            0x00c9a17f      xor   bl, bl
            0x00c9a181      call  0xcc0210
            0x00c9a186      mov   cl, al
            0x00c9a188      add   esp, 0x04
            0x00c9a18b      mov   eax, dword [ebp+0x08]
            0x00c9a18e      mov   eax, dword [eax+0x10]
            0x00c9a191      cmp   eax, 0x27                            ; ''' ; 39
        ,=< 0x00c9a194      jnz   0xc9a26d
        |   0x00c9a19a      lea   ebx, dword [eax-0x23]
        |   0x00c9a19d      test  cl, cl
       ,==< 0x00c9a19f      jz    0xc9a21f
       ||   0x00c9a1a1      mov   eax, dword [0x201f660]               ; [0x201f660:4]=0
       ||   0x00c9a1a6      xor   edi, edi
       ||   0x00c9a1a8      xor   esi, esi
       ||   0x00c9a1aa      xor   ebx, ebx
       ||   0x00c9a1ac      mov   eax, dword [eax+0x108]
       ||   0x00c9a1b2      mov   dword [ebp-0x20], 0x00
       ||   0x00c9a1b9      mov   dword [ebp-0x1c], edi
       ||   0x00c9a1bc      mov   dword [ebp-0x18], esi
       ||   0x00c9a1bf      mov   ecx, dword [eax*4+0x2027ed0]
       ||   0x00c9a1c6      mov   dword [ebp-0x14], ebx
       ||   0x00c9a1c9      mov   dword [ebp-0x24], ecx
       ||   0x00c9a1cc      test  ecx, ecx
      ,===< 0x00c9a1ce      jz    0xc9a1eb
      |||   0x00c9a1d0      mov   eax, dword [ecx]
      |||   0x00c9a1d2      lea   edx, dword [ebp-0x18]
      |||   0x00c9a1d5      push  edx
      |||   0x00c9a1d6      lea   edx, dword [ebp-0x20]
      |||   0x00c9a1d9      push  edx
      |||   0x00c9a1da      call  dword [eax+0x3c]                     ; 60
      |||   0x00c9a1dd      mov   ecx, dword [ebp-0x24]
      |||   0x00c9a1e0      test  ecx, ecx
      |||   0x00c9a1e2      mov   ebx, dword [ebp-0x14]
      |||   0x00c9a1e5      mov   esi, dword [ebp-0x18]
      |||   0x00c9a1e8      mov   edi, dword [ebp-0x1c]
      `---> 0x00c9a1eb      mov   eax, dword [ebp+0x10]
      ,===< 0x00c9a1ee      jnz   0xc9a1f4
      |||   0x00c9a1f0      xor   ecx, ecx
     ,====< 0x00c9a1f2      jmp   0xc9a20e
     |`---> 0x00c9a1f4      movzx edx, ax
     | ||   0x00c9a1f7      xor   ecx, ecx
     | ||   0x00c9a1f9      cmp   edx, edi
     |,===< 0x00c9a1fb      jnb   0xc9a20e
     ||||   0x00c9a1fd      mov   ecx, dword [ebp-0x20]
     ||||   0x00c9a200      mov   ecx, dword [ecx+edx*4]
     ||||   0x00c9a203      test  ecx, ecx
    ,=====< 0x00c9a205      jnz   0xc9a20e
    |||||   0x00c9a207      cmp   edx, ebx
   ,======< 0x00c9a209      jnb   0xc9a20e
   ||||||   0x00c9a20b      mov   ecx, dword [esi+edx*4]
   ````---> 0x00c9a20e      xor   ebx, ebx
       ||   0x00c9a210      cmp   dword [ecx+0x28], 0x01
       ||   0x00c9a214      setnz bl
       ||   0x00c9a217      add   ebx, 0x20                            ; 32
       ||   0x00c9a21a      mov   edi, dword [ebp-0x28]
      ,===< 0x00c9a21d      jmp   0xc9a238
      |`--> 0x00c9a21f      lea   eax, dword [ebp+0x10]
      | |   0x00c9a222      push  eax
      | |   0x00c9a223      call  0xca0620
      | |   0x00c9a228      add   esp, 0x04
      | |   0x00c9a22b      mov   ecx, 0x09
      | |   0x00c9a230      test  al, al
      | |   0x00c9a232      mov   eax, dword [ebp+0x10]
      | |   0x00c9a235      cmovz ebx, ecx
      `---> 0x00c9a238      lea   ecx, dword [ebx+ebx*4]
        |   0x00c9a23b      mov   dword [ebp-0x24], eax
        |   0x00c9a23e      lea   esi, dword [edi+ecx*4]
        |   0x00c9a241      lea   ecx, dword [ebp-0x20]
        |   0x00c9a244      mov   byte [ebp-0x04], 0x02
        |   0x00c9a248      call  0x4f6c50
        |   0x00c9a24d      mov   dword [ebp-0x1c], 0x00
        |   0x00c9a254      mov   dword [ebp-0x18], 0x00
        |   0x00c9a25b      mov   dword [ebp-0x14], 0x00
        |   0x00c9a262      mov   byte [ebp-0x04], 0x03
        |   0x00c9a266      lea   eax, dword [ebp-0x24]
        |   0x00c9a269      mov   ecx, esi
       ,==< 0x00c9a26b      jmp   0xc9a2c7
       |`-> 0x00c9a26d      cmp   eax, 0x06                            ; 6
       |,=< 0x00c9a270      jnz   0xc9a2df
       ||   0x00c9a272      push  esi
       ||   0x00c9a273      call  0xcfa700
       ||   0x00c9a278      add   esp, 0x04
       ||   0x00c9a27b      test  al, al
       ||   0x00c9a27d      lea   eax, dword [ebp+0x10]
       ||   0x00c9a280      push  eax
      ,===< 0x00c9a281      jz    0xc9a297
      |||   0x00c9a283      lea   ecx, dword [ebp-0x24]
      |||   0x00c9a286      call  0xc94c10
      |||   0x00c9a28b      mov   byte [ebp-0x04], 0x04
      |||   0x00c9a28f      lea   ecx, dword [edi+0x140]
     ,====< 0x00c9a295      jmp   0xc9a2c7
     |`---> 0x00c9a297      call  0xca0620
     | ||   0x00c9a29c      add   esp, 0x04
     | ||   0x00c9a29f      invalid
            