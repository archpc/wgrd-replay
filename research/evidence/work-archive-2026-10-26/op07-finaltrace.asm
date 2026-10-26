            0x00b67c00      push  ebp
            0x00b67c01      mov   ebp, esp
            0x00b67c03      push  0xffffffff                           ; 255
            0x00b67c05      push  0x186d090
            0x00b67c0a      mov   eax, dword fs:[0x0]
            0x00b67c10      push  eax
            0x00b67c11      push  ecx
            0x00b67c12      push  esi
            0x00b67c13      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b67c18      xor   eax, ebp
            0x00b67c1a      push  eax
            0x00b67c1b      lea   eax, dword [ebp-0x0c]
            0x00b67c1e      mov   dword fs:[0x0], eax
            0x00b67c24      mov   esi, ecx
            0x00b67c26      mov   dword [ebp-0x10], esi
            0x00b67c29      mov   byte [esi+0x04], 0x00
            0x00b67c2d      mov   dword [esi+0x08], 0x00
            0x00b67c34      mov   dword [esi+0x0c], 0x00
            0x00b67c3b      mov   dword [esi], 0x19a3d34               ; [0x19a3d34:4]=0xb6a690
            0x00b67c41      push  esi
            0x00b67c42      mov   dword [ebp-0x04], 0x00
            0x00b67c49      mov   dword [0x203bee0], esi
            0x00b67c4f      call  0x517910
            0x00b67c54      add   esp, 0x04
            0x00b67c57      push  str.None                             ; 0x1949380 ; "None"
            0x00b67c5c      lea   ecx, dword [esi+0x10]
            0x00b67c5f      mov   dword [ebp-0x04], 0x01
            0x00b67c66      mov   dword [esi], 0x19a3d3c               ; [0x19a3d3c:4]=0xb6ac00
            0x00b67c6c      call  0x4e8400
            0x00b67c71      push  0x19a3e9c                            ; "DoNothing"
            0x00b67c76      lea   ecx, dword [esi+0x14]
            0x00b67c79      call  0x4e8400
            0x00b67c7e      push  0x19a3ea8                            ; "Move"
            0x00b67c83      lea   ecx, dword [esi+0x18]
            0x00b67c86      call  0x4e8400
            0x00b67c8b      push  0x19a3eb0                            ; "Stop"
            0x00b67c90      lea   ecx, dword [esi+0x1c]
            0x00b67c93      call  0x4e8400
            0x00b67c98      push  0x19a3eb8                            ; "StandBy"
            0x00b67c9d      lea   ecx, dword [esi+0x20]
            0x00b67ca0      call  0x4e8400
            0x00b67ca5      push  0x19a3ec0                            ; "Attack"
            0x00b67caa      lea   ecx, dword [esi+0x24]
            0x00b67cad      call  0x4e8400
            0x00b67cb2      push  str.Attack2                          ; 0x19a3ec8 ; "Attack2"
            0x00b67cb7      lea   ecx, dword [esi+0x28]
            0x00b67cba      call  0x4e8400
            0x00b67cbf      push  0x19a3ed0                            ; "FollowFormation"
            0x00b67cc4      lea   ecx, dword [esi+0x2c]
            0x00b67cc7      call  0x4e8400
            0x00b67ccc      push  0x19a3ee0                            ; "Shoot"
            0x00b67cd1      lea   ecx, dword [esi+0x30]
            0x00b67cd4      call  0x4e8400
            0x00b67cd9      push  str.Merge                            ; 0x19a3ee8 ; "Merge"
            0x00b67cde      lea   ecx, dword [esi+0x34]
            0x00b67ce1      call  0x4e8400
            0x00b67ce6      push  str.Regroup                          ; 0x19a3ef0 ; "Regroup"
            0x00b67ceb      lea   ecx, dword [esi+0x38]
            0x00b67cee      call  0x4e8400
            0x00b67cf3      push  0x19a3ef8                            ; "UnloadFromTransport"
            0x00b67cf8      lea   ecx, dword [esi+0x3c]
            0x00b67cfb      call  0x4e8400
            0x00b67d00      push  0x19a3f0c                            ; "Land"
            0x00b67d05      lea   ecx, dword [esi+0x40]
            0x00b67d08      call  0x4e8400
            0x00b67d0d      push  0x19a3f14                            ; "GoUp"
            0x00b67d12      lea   ecx, dword [esi+0x44]
            0x00b67d15      call  0x4e8400
            0x00b67d1a      push  0x19a3f1c                            ; "GoDown"
            0x00b67d1f      lea   ecx, dword [esi+0x48]
            0x00b67d22      call  0x4e8400
            0x00b67d27      push  0x19a3f24                            ; "MoveAndAttack"
            0x00b67d2c      lea   ecx, dword [esi+0x4c]
            0x00b67d2f      call  0x4e8400
            0x00b67d34      push  0x19a3f34                            ; "SplitCompany"
            0x00b67d39      lea   ecx, dword [esi+0x50]
            0x00b67d3c      call  0x4e8400
            0x00b67d41      push  0x19a3f44                            ; "Spread"
            0x00b67d46      lea   ecx, dword [esi+0x54]
            0x00b67d49      call  0x4e8400
            0x00b67d4e      push  0x19a3f4c                            ; "Reverse"
            0x00b67d53      lea   ecx, dword [esi+0x58]
            0x00b67d56      call  0x4e8400
            0x00b67d5b      push  0x19a3f54                            ; "SupplyUnit"
            0x00b67d60      lea   ecx, dword [esi+0x5c]
            0x00b67d63      call  0x4e8400
            0x00b67d68      push  0x19a3f60                            ; "AskForSupply"
            0x00b67d6d      lea   ecx, dword [esi+0x60]
            0x00b67d70      call  0x4e8400
            0x00b67d75      push  0x19a3f70                            ; "GoGetSupply"
            0x00b67d7a      lea   ecx, dword [esi+0x64]
            0x00b67d7d      call  0x4e8400
            0x00b67d82      push  0x19a3f7c                            ; "EnterDistrict"
            0x00b67d87      lea   ecx, dword [esi+0x68]
            0x00b67d8a      call  0x4e8400
            0x00b67d8f      push  0x19a3f8c                            ; "AirplanePatrol"
            0x00b67d94      lea   ecx, dword [esi+0x6c]
            0x00b67d97      call  0x4e8400
            0x00b67d9c      push  0x19a3f9c                            ; "AirplaneAttack"
            0x00b67da1      lea   ecx, dword [esi+0x70]
            0x00b67da4      call  0x4e8400
            0x00b67da9      push  0x19a3fac                            ; "LoadIntoTransport"
            0x00b67dae      lea   ecx, dword [esi+0x74]
            0x00b67db1      call  0x4e8400
            0x00b67db6      push  0x19a3fc0                            ; "LoadUnit"
            0x00b67dbb      lea   ecx, dword [esi+0x78]
            0x00b67dbe      call  0x4e8400
            0x00b67dc3      push  0x19a3fcc                            ; "GenericLoadUnit"
            0x00b67dc8      lea   ecx, dword [esi+0x7c]
            0x00b67dcb      call  0x4e8400
            0x00b67dd0      push  0x19a3fdc                            ; "AirplaneTakeOff"
            0x00b67dd5      lea   ecx, dword [esi+0x80]
            0x00b67ddb      call  0x4e8400
            0x00b67de0      push  0x19a3fec                            ; "AirplaneEvacuate"
            0x00b67de5      lea   ecx, dword [esi+0x84]
            0x00b67deb      call  0x4e8400
            0x00b67df0      push  str.AirplaneShoot                    ; 0x19a4000 ; "AirplaneShoot"
            0x00b67df5      lea   ecx, dword [esi+0x88]
            0x00b67dfb      call  0x4e8400
            0x00b67e00      push  str.BattleGroupDeploy                ; 0x19a4010 ; "BattleGroupDeploy"
            0x00b67e05      lea   ecx, dword [esi+0x8c]
            0x00b67e0b      call  0x4e8400
            0x00b67e10      push  str.BattleGroupMove                  ; 0x19a4024 ; "BattleGroupMove"
            0x00b67e15      lea   ecx, dword [esi+0x90]
            0x00b67e1b      call  0x4e8400
            0x00b67e20      push  str.BattleGroupOffensiveGrouping     ; 0x19a4034 ; "BattleGroupOffensiveGrouping"
            0x00b67e25      lea   ecx, dword [esi+0x94]
            0x00b67e2b      call  0x4e8400
            0x00b67e30      push  str.BattleGroupDefensiveGrouping     ; 0x19a4054 ; "BattleGroupDefensiveGrouping"
            0x00b67e35      lea   ecx, dword [esi+0x98]
            0x00b67e3b      call  0x4e8400
            0x00b67e40      push  str.BattleGroupRefit                 ; 0x19a4074 ; "BattleGroupRefit"
            0x00b67e45      lea   ecx, dword [esi+0x9c]
            0x00b67e4b      call  0x4e8400
            0x00b67e50      push  str.BattleGroupRegen                 ; 0x19a4088 ; "BattleGroupRegen"
            0x00b67e55      lea   ecx, dword [esi+0xa0]
            0x00b67e5b      call  0x4e8400
            0x00b67e60      push  str.BattleGroupRestOrSupply          ; 0x19a409c ; "BattleGroupRestOrSupply"
            0x00b67e65      lea   ecx, dword [esi+0xa4]
            0x00b67e6b      call  0x4e8400
            0x00b67e70      push  str.BattleGroupCancelOrders          ; 0x19a40b4 ; "BattleGroupCancelOrders"
            0x00b67e75      lea   ecx, dword [esi+0xa8]
            0x00b67e7b      call  0x4e8400
            0x00b67e80      push  str.BattleGroupAssignment            ; 0x19a40cc ; "BattleGroupAssignment"
            0x00b67e85      lea   ecx, dword [esi+0xac]
            0x00b67e8b      call  0x4e8400
            0x00b67e90      push  str.StrategicPawnTransform           ; 0x19a40e4 ; "StrategicPawnTransform"
            0x00b67e95      lea   ecx, dword [esi+0xb0]
            0x00b67e9b      call  0x4e8400
            0x00b67ea0      push  str.StrategicPawnAttack              ; 0x19a40fc ; "StrategicPawnAttack"
            0x00b67ea5      lea   ecx, dword [esi+0xb4]
            0x00b67eab      call  0x4e8400
            0x00b67eb0      push  str.StrategicPawnDefense             ; 0x19a4110 ; "StrategicPawnDefense"
            0x00b67eb5      lea   ecx, dword [esi+0xb8]
            0x00b67ebb      call  0x4e8400
            0x00b67ec0      push  str.BattleGroupBattle                ; 0x19a4128 ; "BattleGroupBattle"
            0x00b67ec5      lea   ecx, dword [esi+0xbc]
            0x00b67ecb      call  0x4e8400
            0x00b67ed0      push  str.BattleGroupTakeCityOwnership     ; 0x19a413c ; "BattleGroupTakeCityOwnership"
            0x00b67ed5      lea   ecx, dword [esi+0xc0]
            0x00b67edb      call  0x4e8400
            0x00b67ee0      push  str.BattleGroupRout                  ; 0x19a415c ; "BattleGroupRout"
            0x00b67ee5      lea   ecx, dword [esi+0xc4]
            0x00b67eeb      call  0x4e8400
            0x00b67ef0      push  str.NotReallyAnOrder_BattleGroupCapture ; 0x19a416c ; "NotReallyAnOrder_BattleGroupCapture"
            0x00b67ef5      lea   ecx, dword [esi+0xc8]
            0x00b67efb      call  0x4e8400
            0x00abd410      push  ebp
            0x00abd411      mov   ebp, esp
            0x00abd413      push  0xffffffff                           ; 255
            0x00abd415      push  0x1863876
            0x00abd41a      mov   eax, dword fs:[0x0]
            0x00abd420      push  eax
            0x00abd421      sub   esp, 0xfc
            0x00abd427      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00abd42c      xor   eax, ebp
            0x00abd42e      mov   dword [ebp-0x10], eax
            0x00abd431      push  esi
            0x00abd432      push  edi
            0x00abd433      push  eax
            0x00abd434      lea   eax, dword [ebp-0x0c]
            0x00abd437      mov   dword fs:[0x0], eax
            0x00abd43d      mov   edi, dword [ebp+0x14]
            0x00abd440      mov   eax, dword [ebp+0x08]
            0x00abd443      mov   esi, dword [ebp+0x18]
            0x00abd446      mov   dword [ebp-0xe0], eax
            0x00abd44c      mov   dword [ebp-0xd4], eax
            0x00abd452      mov   dword [ebp-0xdc], 0x00
            0x00abd45c      mov   ecx, dword [edi]
            0x00abd45e      mov   eax, dword [edi+0x04]
            0x00abd461      mov   dword [ebp-0x04], 0x00
            0x00abd468      lea   eax, dword [ecx+eax*4]
            0x00abd46b      push  eax
            0x00abd46c      push  ecx
            0x00abd46d      lea   ecx, dword [ebp-0x108]
            0x00abd473      call  0xab6660
            0x00abd478      mov   ecx, dword [esi]
            0x00abd47a      mov   eax, dword [esi+0x04]
            0x00abd47d      mov   dword [ebp-0x04], 0x01
            0x00abd484      lea   eax, dword [ecx+eax*4]
            0x00abd487      push  eax
            0x00abd488      push  ecx
            0x00abd489      lea   ecx, dword [ebp-0xf4]
            0x00abd48f      call  0xab6660
            0x00abd494      cmp   dword [edi+0x04], 0x00
            0x00abd498      mov   byte [ebp-0x04], 0x02
        ,=< 0x00abd49c      jz    0xabd4bf
        |   0x00abd49e      mov   ecx, dword [edi]
        |   0x00abd4a0      call  0xb01530
        |   0x00abd4a5      mov   ecx, dword [0x201e2dc]               ; [0x201e2dc:4]=0
        |   0x00abd4ab      push  dword [eax+0x3c]
        |   0x00abd4ae      call  0xbb2190
        |   0x00abd4b3      mov   edi, eax
        |   0x00abd4b5      mov   dword [ebp-0xd0], edi
        |   0x00abd4bb      test  edi, edi
       ,==< 0x00abd4bd      jnz   0xabd4cd
       |`-> 0x00abd4bf      mov   eax, dword [0x201e2dc]               ; [0x201e2dc:4]=0
       |    0x00abd4c4      mov   eax, dword [eax+0x74]
       |    0x00abd4c7      mov   dword [ebp-0xd0], eax
       `--> 0x00abd4cd      mov   ecx, dword [ebp-0xd4]
            0x00abd4d3      call  0x4f6c50
            0x00abd4d8      mov   ecx, dword [0x2025d00]               ; [0x2025d00:4]=0
            0x00abd4de      mov   eax, dword [ebp+0x10]
            0x00abd4e1      push  ecx
            0x00abd4e2      mov   edx, esp
            0x00abd4e4      mov   dword [ebp-0xdc], 0x01
            0x00abd4ee      mov   dword [edx], eax
            0x00abd4f0      call  0xb9cf20
            0x00abd4f5      lea   ecx, dword [ebp-0xcc]
            0x00abd4fb      mov   dword [ebp-0xd8], eax
            0x00abd501      call  0x598730
            0x00abd506      mov   esi, dword [ebp-0xc0]
            0x00abd50c      mov   edx, dword [ebp-0xc4]
            0x00abd512      mov   eax, edx
            0x00abd514      imul  ecx, esi, 0xb4
            0x00abd51a      mov   byte [ebp-0x04], 0x03
            0x00abd51e      add   ecx, eax
            0x00abd520      cmp   eax, ecx
        ,=< 0x00abd522      jz    0xabd53c
       .--> 0x00abd524      cmp   dword [eax], 0x47                    ; 'G'
      ,===< 0x00abd527      jnz   0xabd52f
      |:|   0x00abd529      cmp   dword [eax+0x04], 0x0b
     ,====< 0x00abd52d      jz    0xabd538
     |`---> 0x00abd52f      add   eax, 0xb4                            ; 180
     | :|   0x00abd534      cmp   eax, ecx
     | `==< 0x00abd536      jnz   0xabd524
     `----> 0x00abd538      cmp   eax, ecx
       ,==< 0x00abd53a      jnz   0xabd57c
       |`-> 0x00abd53c      cmp   esi, dword [ebp-0xcc]
       |,=< 0x00abd542      jnz   0xabd555
       ||   0x00abd544      lea   ecx, dword [ebp-0xcc]
       ||   0x00abd54a      call  0x9d6ad0
       ||   0x00abd54f      mov   edx, dword [ebp-0xc4]
       |`-> 0x00abd555      imul  ecx, esi, 0xb4
       |    0x00abd55b      lea   eax, dword [esi+0x01]
       |    0x00abd55e      mov   dword [ebp-0xc0], eax
       |    0x00abd564      mov   dword [ecx+edx*1], 0x47              ; 'G'
       |                                                               ; [0x47:4]=-1 ; 71
       |    0x00abd56b      mov   dword [ecx+edx*1+0x04], 0x0b         ; [0xb:4]=-1 ; 11
       |    0x00abd573      mov   eax, dword [ebp+0x10]
       |    0x00abd576      mov   dword [ecx+edx*1+0x08], eax
       |,=< 0x00abd57a      jmp   0xabd582
       `--> 0x00abd57c      mov   ecx, dword [ebp+0x10]
        |   0x00abd57f      mov   dword [eax+0x08], ecx
        `-> 0x00abd582      mov   esi, dword [ebp-0xc0]
            0x00abd588      mov   edx, dword [ebp-0xc4]
            0x00abd58e      mov   eax, edx
            0x00abd590      imul  ecx, esi, 0xb4
            0x00abd596      add   ecx, eax
            0x00abd598      cmp   eax, ecx
        ,=< 0x00abd59a      jz    0xabd5b8
        |   0x00abd59c      nop   dword [eax], eax
       .--> 0x00abd5a0      cmp   dword [eax], 0x48                    ; 'H'
      ,===< 0x00abd5a3      jnz   0xabd5ab
      |:|   0x00abd5a5      cmp   dword [eax+0x04], 0x0b
     ,====< 0x00abd5a9      jz    0xabd5b4
     |`---> 0x00abd5ab      add   eax, 0xb4                            ; 180
     | :|   0x00abd5b0      cmp   eax, ecx
     | `==< 0x00abd5b2      jnz   0xabd5a0
     `----> 0x00abd5b4      cmp   eax, ecx
       ,==< 0x00abd5b6      jnz   0xabd5f8
       |`-> 0x00abd5b8      cmp   esi, dword [ebp-0xcc]
       |,=< 0x00abd5be      jnz   0xabd5d1
       ||   0x00abd5c0      lea   ecx, dword [ebp-0xcc]
       ||   0x00abd5c6      call  0x9d6ad0
       ||   0x00abd5cb      mov   edx, dword [ebp-0xc4]
       |`-> 0x00abd5d1      imul  ecx, esi, 0xb4
       |    0x00abd5d7      lea   eax, dword [esi+0x01]
       |    0x00abd5da      mov   dword [ebp-0xc0], eax
       |    0x00abd5e0      mov   eax, dword [ebp+0x0c]
       |    0x00abd5e3      mov   dword [ecx+edx*1], 0x48              ; 'H'
       |                                                               ; [0x48:4]=-1 ; 72
       |    0x00abd5ea      mov   dword [ecx+edx*1+0x04], 0x0b         ; [0xb:4]=-1 ; 11
       |    0x00abd5f2      mov   dword [ecx+edx*1+0x08], eax
       |,=< 0x00abd5f6      jmp   0xabd5fe
       `--> 0x00abd5f8      mov   ecx, dword [ebp+0x0c]
        |   0x00abd5fb      mov   dword [eax+0x08], ecx
        `-> 0x00abd5fe      mov   esi, dword [ebp-0xc0]
            0x00abd604      mov   edx, dword [ebp-0xc4]
            0x00abd60a      mov   eax, edx
            0x00abd60c      imul  ecx, esi, 0xb4
            0x00abd612      add   ecx, eax
            0x00abd614      cmp   eax, ecx
        ,=< 0x00abd616      jz    0xabd630
       .--> 0x00abd618      cmp   dword [eax], 0x49                    ; 'I'
      ,===< 0x00abd61b      jnz   0xabd623
      |:|   0x00abd61d      cmp   dword [eax+0x04], 0x0b
     ,====< 0x00abd621      jz    0xabd62c
     |`---> 0x00abd623      add   eax, 0xb4                            ; 180
     | :|   0x00abd628      cmp   eax, ecx
     | `==< 0x00abd62a      jnz   0xabd618
     `----> 0x00abd62c      cmp   eax, ecx
       ,==< 0x00abd62e      jnz   0xabd678
       |`-> 0x00abd630      cmp   esi, dword [ebp-0xcc]
       |,=< 0x00abd636      jnz   0xabd649
       ||   0x00abd638      lea   ecx, dword [ebp-0xcc]
       ||   0x00abd63e      call  0x9d6ad0
       ||   0x00abd643      mov   edx, dword [ebp-0xc4]
       |`-> 0x00abd649      imul  ecx, esi, 0xb4
       |    0x00abd64f      lea   eax, dword [esi+0x01]
       |    0x00abd652      add   ecx, edx
       |    0x00abd654      mov   dword [ebp-0xc0], eax
       |    0x00abd65a      lea   eax, dword [ebp-0x108]
       |    0x00abd660      push  eax
       |    0x00abd661      mov   dword [ecx], 0x49                    ; 'I'
       |                                                               ; [0x49:4]=-1 ; 73
       |    0x00abd667      mov   dword [ecx+0x04], 0x0b               ; [0xb:4]=-1 ; 11
       |    0x00abd66e      add   ecx, 0x08
       |    0x00abd671      call  0x9bd5d0
       |,=< 0x00abd676      jmp   0xabd687
       `--> 0x00abd678      lea   ecx, dword [ebp-0x108]
        |   0x00abd67e      push  ecx
        |   0x00abd67f      lea   ecx, dword [eax+0x08]
        |   0x00abd682      call  0xa9f100
        `-> 0x00abd687      mov   esi, dword [ebp-0xc0]
            0x00abd68d      mov   edx, dword [ebp-0xc4]
            0x00abd693      mov   eax, edx
            0x00abd695      imul  ecx, esi, 0xb4
            0x00abd69b      add   ecx, eax
            0x00abd69d      cmp   eax, ecx
        ,=< 0x00abd69f      jz    0xabd6b9
       .--> 0x00abd6a1      cmp   dword [eax], 0x4a                    ; 'J'
      ,===< 0x00abd6a4      jnz   0xabd6ac
      |:|   0x00abd6a6      cmp   dword [eax+0x04], 0x0b
     ,====< 0x00abd6aa      jz    0xabd6b5
     |`---> 0x00abd6ac      add   eax, 0xb4                            ; 180
     | :|   0x00abd6b1      cmp   eax, ecx
     | `==< 0x00abd6b3      jnz   0xabd6a1
     `----> 0x00abd6b5      cmp   eax, ecx
       ,==< 0x00abd6b7      jnz   0xabd701
       |`-> 0x00abd6b9      cmp   esi, dword [ebp-0xcc]
       |,=< 0x00abd6bf      jnz   0xabd6d2
       ||   0x00abd6c1      lea   ecx, dword [ebp-0xcc]
       ||   0x00abd6c7      call  0x9d6ad0
       ||   0x00abd6cc      mov   edx, dword [ebp-0xc4]
       |`-> 0x00abd6d2      imul  ecx, esi, 0xb4
       |    0x00abd6d8      lea   eax, dword [esi+0x01]
       |    0x00abd6db      add   ecx, edx
       |    0x00abd6dd      mov   dword [ebp-0xc0], eax
       |    0x00abd6e3      lea   eax, dword [ebp-0xf4]
       |    0x00abd6e9      push  eax
       |    0x00abd6ea      mov   dword [ecx], 0x4a                    ; 'J'
       |                                                               ; [0x4a:4]=-1 ; 74
       |    0x00abd6f0      mov   dword [ecx+0x04], 0x0b               ; [0xb:4]=-1 ; 11
       |    0x00abd6f7      add   ecx, 0x08
       |    0x00abd6fa      call  0x9bd5d0
       |,=< 0x00abd6ff      jmp   0xabd710
       `--> 0x00abd701      lea   ecx, dword [ebp-0xf4]
        |   0x00abd707      push  ecx
        |   0x00abd708      lea   ecx, dword [eax+0x08]
        |   0x00abd70b      call  0xa9f100
        `-> 0x00abd710      mov   esi, dword [ebp-0xc0]
            0x00abd716      mov   edi, dword [ebp-0xc4]
            0x00abd71c      mov   eax, edi
            0x00abd71e      imul  ecx, esi, 0xb4
            0x00abd724      add   ecx, eax
            0x00abd726      cmp   eax, ecx
        ,=< 0x00abd728      jz    0xabd748
        |   0x00abd72a      nop   word [eax+eax*1], ax
       .--> 0x00abd730      cmp   dword [eax], 0x4b                    ; 'K'
      ,===< 0x00abd733      jnz   0xabd73b
      |:|   0x00abd735      cmp   dword [eax+0x04], 0x0b
     ,====< 0x00abd739      jz    0xabd744
     |`---> 0x00abd73b      add   eax, 0xb4                            ; 180
     | :|   0x00abd740      cmp   eax, ecx
     | `==< 0x00abd742      jnz   0xabd730
     `----> 0x00abd744      cmp   eax, ecx
       ,==< 0x00abd746      jnz   0xabd795
       |`-> 0x00abd748      cmp   esi, dword [ebp-0xcc]
       |,=< 0x00abd74e      jnz   0xabd761
       ||   0x00abd750      lea   ecx, dword [ebp-0xcc]
       ||   0x00abd756      call  0x9d6ad0
       ||   0x00abd75b      mov   edi, dword [ebp-0xc4]
       |`-> 0x00abd761      mov   ecx, dword [ebp+0x1c]
       |    0x00abd764      lea   eax, dword [esi+0x01]
       |    0x00abd767      imul  edx, esi, 0xb4
       |    0x00abd76d      add   edx, edi
       |    0x00abd76f      mov   dword [ebp-0xc0], eax
       |    0x00abd775      mov   dword [edx], 0x4b                    ; 'K'
       |                                                               ; [0x4b:4]=-1 ; 75
       |    0x00abd77b      mov   dword [edx+0x04], 0x0b               ; [0xb:4]=-1 ; 11
       |    0x00abd782      mov   eax, dword [ecx]
       |    0x00abd784      mov   dword [edx+0x08], eax
       |    0x00abd787      mov   eax, dword [ecx+0x04]
       |    0x00abd78a      mov   dword [edx+0x0c], eax
       |    0x00abd78d      mov   eax, dword [ecx+0x08]
       |    0x00abd790      mov   dword [edx+0x10], eax
       |,=< 0x00abd793      jmp   0xabd7a9
       `--> 0x00abd795      mov   edx, dword [ebp+0x1c]
        |   0x00abd798      mov   ecx, dword [edx]
        |   0x00abd79a      mov   dword [eax+0x08], ecx
        |   0x00abd79d      mov   ecx, dword [edx+0x04]
        |   0x00abd7a0      mov   dword [eax+0x0c], ecx
        |   0x00abd7a3      mov   ecx, dword [edx+0x08]
        |   0x00abd7a6      mov   dword [eax+0x10], ecx
        `-> 0x00abd7a9      mov   esi, dword [ebp-0xc0]
            0x00abd7af      mov   edi, dword [ebp-0xc4]
            0x00abd7b5      mov   eax, edi
            0x00abd7b7      imul  ecx, esi, 0xb4
            0x00abd7bd      add   ecx, eax
            0x00abd7bf      cmp   eax, ecx
        ,=< 0x00abd7c1      jz    0xabd7db
       .--> 0x00abd7c3      cmp   dword [eax], 0x4c                    ; 'L'
      ,===< 0x00abd7c6      jnz   0xabd7ce
      |:|   0x00abd7c8      cmp   dword [eax+0x04], 0x0b
     ,====< 0x00abd7cc      jz    0xabd7d7
     |`---> 0x00abd7ce      add   eax, 0xb4                            ; 180
     | :|   0x00abd7d3      cmp   eax, ecx
     | `==< 0x00abd7d5      jnz   0xabd7c3
     `----> 0x00abd7d7      cmp   eax, ecx
       ,==< 0x00abd7d9      jnz   0xabd822
       |`-> 0x00abd7db      cmp   esi, dword [ebp-0xcc]
       |,=< 0x00abd7e1      jnz   0xabd7f4
       ||   0x00abd7e3      lea   ecx, dword [ebp-0xcc]
       ||   0x00abd7e9      call  0x9d6ad0
       ||   0x00abd7ee      mov   edi, dword [ebp-0xc4]
       |`-> 0x00abd7f4      mov   ecx, dword [ebp+0x20]
       |    0x00abd7f7      lea   eax, dword [esi+0x01]
       |    0x00abd7fa      imul  edx, esi, 0xb4
       |    0x00abd800      add   edx, edi
       |    0x00abd802      mov   dword [ebp-0xc0], eax
       |    0x00abd808      mov   dword [edx], 0x4c                    ; 'L'
       |                                                               ; [0x4c:4]=-1 ; 76
       |    0x00abd80e      mov   dword [edx+0x04], 0x0b               ; [0xb:4]=-1 ; 11
       |    0x00abd815      mov   eax, dword [ecx]
       |    0x00abd817      mov   dword [edx+0x08], eax
       |    0x00abd81a      mov   eax, dword [ecx+0x04]
       |    0x00abd81d      mov   dword [edx+0x0c], eax
       |,=< 0x00abd820      jmp   0xabd830
       `--> 0x00abd822      mov   edx, dword [ebp+0x20]
        |   0x00abd825      mov   ecx, dword [edx]
        |   0x00abd827      mov   dword [eax+0x08], ecx
        |   0x00abd82a      mov   ecx, dword [edx+0x04]
        |   0x00abd82d      mov   dword [eax+0x0c], ecx
        `-> 0x00abd830      mov   esi, dword [ebp-0xc0]
            0x00abd836      mov   edx, dword [ebp-0xc4]
            0x00abd83c      mov   eax, edx
            0x00abd83e      imul  ecx, esi, 0xb4
            0x00abd844      add   ecx, eax
            0x00abd846      cmp   eax, ecx
        ,=< 0x00abd848      jz    0xabd868
        |   0x00abd84a      nop   word [eax+eax*1], ax
       .--> 0x00abd850      cmp   dword [eax], 0x4d                    ; 'M'
      ,===< 0x00abd853      jnz   0xabd85b
      |:|   0x00abd855      cmp   dword [eax+0x04], 0x0b
     ,====< 0x00abd859      jz    0xabd864
     |`---> 0x00abd85b      add   eax, 0xb4                            ; 180
     | :|   0x00abd860      cmp   eax, ecx
     | `==< 0x00abd862      jnz   0xabd850
     `----> 0x00abd864      cmp   eax, ecx
       ,==< 0x00abd866      jnz   0xabd8ac
       |`-> 0x00abd868      cmp   esi, dword [ebp-0xcc]
       |,=< 0x00abd86e      jnz   0xabd881
       ||   0x00abd870      lea   ecx, dword [ebp-0xcc]
       ||   0x00abd876      call  0x9d6ad0
       ||   0x00abd87b      mov   edx, dword [ebp-0xc4]
       |`-> 0x00abd881      push  dword [ebp+0x24]
       |    0x00abd884      imul  ecx, esi, 0xb4
       |    0x00abd88a      lea   eax, dword [esi+0x01]
       |    0x00abd88d      add   ecx, edx
       |    0x00abd88f      mov   dword [ebp-0xc0], eax
       |    0x00abd895      mov   dword [ecx], 0x4d                    ; 'M'
       |                                                               ; [0x4d:4]=-1 ; 77
       |    0x00abd89b      mov   dword [ecx+0x04], 0x0b               ; [0xb:4]=-1 ; 11
       |    0x00abd8a2      add   ecx, 0x08
       |    0x00abd8a5      call  0xabb0d0
       |,=< 0x00abd8aa      jmp   0xabd8c4
       `--> 0x00abd8ac      mov   ecx, dword [ebp+0x24]
        |   0x00abd8af      movups xmm0, xmmword [ecx]
        |   0x00abd8b2      movups xmmword [eax+0x08], xmm0
        |   0x00abd8b6      movups xmm0, xmmword [ecx+0x10]
        |   0x00abd8ba      movups xmmword [eax+0x18], xmm0
        |   0x00abd8be      mov   ecx, dword [ecx+0x20]
        |   0x00abd8c1      mov   dword [eax+0x28], ecx
        `-> 0x00abd8c4      mov   esi, dword [ebp-0xc0]
            0x00abd8ca      mov   edx, dword [ebp-0xc4]
            0x00abd8d0      mov   eax, edx
            0x00abd8d2      imul  ecx, esi, 0xb4
            0x00abd8d8      add   ecx, eax
            0x00abd8da      cmp   eax, ecx
        ,=< 0x00abd8dc      jz    0xabd8f8
        |   0x00abd8de      nop
       .--> 0x00abd8e0      cmp   dword [eax], 0x4e                    ; 'N'
      ,===< 0x00abd8e3      jnz   0xabd8eb
      |:|   0x00abd8e5      cmp   dword [eax+0x04], 0x0b
     ,====< 0x00abd8e9      jz    0xabd8f4
     |`---> 0x00abd8eb      add   eax, 0xb4                            ; 180
     | :|   0x00abd8f0      cmp   eax, ecx
     | `==< 0x00abd8f2      jnz   0xabd8e0
     `----> 0x00abd8f4      cmp   eax, ecx
       ,==< 0x00abd8f6      jnz   0xabd938
       |`-> 0x00abd8f8      cmp   esi, dword [ebp-0xcc]
       |,=< 0x00abd8fe      jnz   0xabd911
       ||   0x00abd900      lea   ecx, dword [ebp-0xcc]
       ||   0x00abd906      call  0x9d6ad0
       ||   0x00abd90b      mov   edx, dword [ebp-0xc4]
       |`-> 0x00abd911      imul  ecx, esi, 0xb4
       |    0x00abd917      lea   eax, dword [esi+0x01]
       |    0x00abd91a      mov   dword [ebp-0xc0], eax
       |    0x00abd920      mov   eax, dword [ebp+0x28]
       |    0x00abd923      mov   dword [ecx+edx*1], 0x4e              ; 'N'
       |                                                               ; [0x4e:4]=-1 ; 78
       |    0x00abd92a      mov   dword [ecx+edx*1+0x04], 0x0b         ; [0xb:4]=-1 ; 11
       |    0x00abd932      mov   dword [ecx+edx*1+0x08], eax
       |,=< 0x00abd936      jmp   0xabd93e
       `--> 0x00abd938      mov   ecx, dword [ebp+0x28]
        |   0x00abd93b      mov   dword [eax+0x08], ecx
        `-> 0x00abd93e      mov   esi, dword [ebp-0xc0]
            0x00abd944      mov   edx, dword [ebp-0xc4]
            0x00abd94a      mov   eax, edx
            0x00abd94c      imul  ecx, esi, 0xb4
            0x00abd952      add   ecx, eax
            0x00abd954      cmp   eax, ecx
        ,=< 0x00abd956      jz    0xabd970
       .--> 0x00abd958      cmp   dword [eax], 0x50                    ; 'P'
      ,===< 0x00abd95b      jnz   0xabd963
      |:|   0x00abd95d      cmp   dword [eax+0x04], 0x0b
     ,====< 0x00abd961      jz    0xabd96c
     |`---> 0x00abd963      add   eax, 0xb4                            ; 180
     | :|   0x00abd968      cmp   eax, ecx
     | `==< 0x00abd96a      jnz   0xabd958
     `----> 0x00abd96c      cmp   eax, ecx
       ,==< 0x00abd96e      jnz   0xabd9b0
       |`-> 0x00abd970      cmp   esi, dword [ebp-0xcc]
       |,=< 0x00abd976      jnz   0xabd989
       ||   0x00abd978      lea   ecx, dword [ebp-0xcc]
       ||   0x00abd97e      call  0x9d6ad0
       ||   0x00abd983      mov   edx, dword [ebp-0xc4]
       |`-> 0x00abd989      imul  ecx, esi, 0xb4
       |    0x00abd98f      lea   eax, dword [esi+0x01]
       |    0x00abd992      mov   dword [ebp-0xc0], eax
       |    0x00abd998      mov   al, byte [ebp+0x2c]
       |    0x00abd99b      mov   dword [ecx+edx*1], 0x50              ; 'P'
       |                                                               ; [0x50:4]=-1 ; 80
       |    0x00abd9a2      mov   dword [ecx+edx*1+0x04], 0x0b         ; [0xb:4]=-1 ; 11
       |    0x00abd9aa      mov   byte [ecx+edx*1+0x08], al
       |,=< 0x00abd9ae      jmp   0xabd9b6
       `--> 0x00abd9b0      mov   cl, byte [ebp+0x2c]
        |   0x00abd9b3      mov   byte [eax+0x08], cl
        `-> 0x00abd9b6      mov   esi, dword [ebp-0xc0]
            0x00abd9bc      mov   edx, dword [ebp-0xc4]
            0x00abd9c2      mov   eax, edx
            0x00abd9c4      imul  ecx, esi, 0xb4
            0x00abd9ca      add   ecx, eax
            0x00abd9cc      cmp   eax, ecx
        ,=< 0x00abd9ce      jz    0xabd9e8
       .--> 0x00abd9d0      cmp   dword [eax], 0x40                    ; '@'
      ,===< 0x00abd9d3      jnz   0xabd9db
      |:|   0x00abd9d5      cmp   dword [eax+0x04], 0xffffffff
     ,====< 0x00abd9d9      jz    0xabd9e4
     |`---> 0x00abd9db      add   eax, 0xb4                            ; 180
     | :|   0x00abd9e0      cmp   eax, ecx
     | `==< 0x00abd9e2      jnz   0xabd9d0
     `----> 0x00abd9e4      cmp   eax, ecx
       ,==< 0x00abd9e6      jnz   0xabda29
       |`-> 0x00abd9e8      cmp   esi, dword [ebp-0xcc]
       |,=< 0x00abd9ee      jnz   0xabda01
       ||   0x00abd9f0      lea   ecx, dword [ebp-0xcc]
       ||   0x00abd9f6      call  0x9d6ad0
       ||   0x00abd9fb      mov   edx, dword [ebp-0xc4]
       |`-> 0x00abda01      imul  ecx, esi, 0xb4
       |    0x00abda07      lea   eax, dword [esi+0x01]
       |    0x00abda0a      mov   dword [ebp-0xc0], eax
       |    0x00abda10      mov   dword [ecx+edx*1], 0x40              ; '@'
       |                                                               ; [0x40:4]=-1 ; 64
       |    0x00abda17      mov   dword [ecx+edx*1+0x04], 0xffffffff   ; [0xffffffff:4]=-1 ; -1
       |    0x00abda1f      mov   dword [ecx+edx*1+0x08], 0x02
       |,=< 0x00abda27      jmp   0xabda30
       `--> 0x00abda29      mov   dword [eax+0x08], 0x02
        `-> 0x00abda30      movaps xmm0, xmmword [0x198ccf0]           ; [0x198ccf0:16]=-1
            0x00abda37      lea   ecx, dword [ebp-0x74]
            0x00abda3a      mov   byte [ebp-0xb8], 0x00
            0x00abda41      mov   dword [ebp-0xb4], 0x00
            0x00abda4b      mov   dword [ebp-0xbc], 0x198b5d0
            0x00abda55      mov   dword [ebp-0xb0], 0x00
            0x00abda5f      mov   dword [ebp-0xac], 0x00
            0x00abda69      mov   dword [ebp-0xa8], 0x00
            0x00abda73      movups xmmword [ebp-0xa4], xmm0
            0x00abda7a      mov   dword [ebp-0x94], 0x00
            0x00abda84      mov   dword [ebp-0x90], 0x00
            0x00abda8e      mov   dword [ebp-0x8c], 0x00
            0x00abda98      mov   byte [ebp-0x88], 0x00
            0x00abda9f      mov   dword [ebp-0x84], 0x00
            0x00abdaa9      mov   dword [ebp-0x80], 0x00
            0x00abdab0      mov   dword [ebp-0x7c], 0x00
            0x00abdab7      mov   byte [ebp-0x78], 0x00
            0x00abdabb      call  0x4e6dd0
            0x00abdac0      mov   dword [ebp-0x70], 0x00
            0x00abdac7      mov   dword [ebp-0x6c], 0x00
            0x00abdace      mov   dword [ebp-0x64], 0x00
            0x00abdad5      mov   dword [ebp-0x60], 0x00
            0x00abdadc      mov   dword [ebp-0x5c], 0x00
            0x00abdae3      mov   dword [ebp-0x54], 0x00
            0x00abdaea      mov   dword [ebp-0x4c], 0x00
            0x00abdaf1      mov   dword [ebp-0x48], 0x00
            0x00abdaf8      xorps xmm0, xmm0
            0x00abdafb      mov   byte [ebp-0x04], 0x06
            0x00abdaff      lea   ecx, dword [ebp-0x1c]
            0x00abdb02      mov   dword [ebp-0x44], 0x00
            0x00abdb09      mov   dword [ebp-0x40], 0x00
            0x00abdb10      mov   dword [ebp-0x3c], 0x00
            0x00abdb17      movups xmmword [ebp-0x38], xmm0
            0x00abdb1b      mov   dword [ebp-0x28], 0x00
            0x00abdb22      mov   dword [ebp-0x24], 0x00
            0x00abdb29      mov   dword [ebp-0x20], 0x00
            0x00abdb30      call  0x4f6c50
            0x00abdb35      mov   dword [ebp-0x18], 0x00
            0x00abdb3c      mov   dword [ebp-0x14], 0x00
            0x00abdb43      mov   eax, dword [ebp-0xd0]
            0x00abdb49      push  0x00
            0x00abdb4b      push  0x01                                 ; 1
            0x00abdb4d      push  dword [ebp-0xd8]
            0x00abdb53      mov   dword [ebp-0xa8], eax
            0x00abdb59      lea   eax, dword [ebp-0xcc]
            0x00abdb5f      push  eax
            0x00abdb60      lea   eax, dword [ebp-0xbc]
            0x00abdb66      mov   byte [ebp-0x04], 0x07
            0x00abdb6a      push  eax
            0x00abdb6b      mov   dword [ebp-0x8c], 0x01
            0x00abdb75      call  0xaf9f60
            0x00abdb7a      mov   esi, dword [ebp-0xd4]
            0x00abdb80      lea   ecx, dword [ebp-0x1c]
            0x00abdb83      add   esp, 0x14
            0x00abdb86      mov   eax, dword [eax+0x20]
            0x00abdb89      mov   dword [esi], eax
            0x00abdb8b      call  0x4dc500
            0x00abdb90      lea   ecx, dword [ebp-0x58]
            0x00abdb93      call  0x975700
            0x00abdb98      cmp   dword [ebp-0x6c], 0x00
            0x00abdb9c      mov   byte [ebp-0x04], 0x08
            0x00abdba0      mov   dword [ebp-0x60], 0x00
        ,=< 0x00abdba7      jz    0xabdbbd
        |   0x00abdba9      push  dword [ebp-0x64]
        |   0x00abdbac      push  0x00
        |   0x00abdbae      call  0x5291c0
        |   0x00abdbb3      add   esp, 0x08
        |   0x00abdbb6      mov   dword [ebp-0x6c], 0x00
        `-> 0x00abdbbd      lea   ecx, dword [ebp-0x74]
            0x00abdbc0      call  0x4dc500
            0x00abdbc5      lea   ecx, dword [ebp-0xc4]
            0x00abdbcb      mov   byte [ebp-0x04], 0x09
            0x00abdbcf      call  0x9d6700
            0x00abdbd4      cmp   dword [ebp-0xcc], 0x00
        ,=< 0x00abdbdb      jz    0xabdbed
        |   0x00abdbdd      push  dword [ebp-0xc4]
        |   0x00abdbe3      push  0x00
        |   0x00abdbe5      call  0x5291c0
        |   0x00abdbea      add   esp, 0x08
        `-> 0x00abdbed      lea   ecx, dword [ebp-0xf4]
            0x00abdbf3      call  0x975700
            0x00abdbf8      lea   ecx, dword [ebp-0x108]
            0x00abdbfe      call  0x975700
            0x00abdc03      mov   eax, esi
            0x00abdc05      mov   ecx, dword [ebp-0x0c]
            0x00abdc08      mov   dword fs:[0x0], ecx
            0x00abdc0f      pop   ecx
            0x00abdc10      pop   edi
            0x00abdc11      pop   esi
            0x00abdc12      mov   ecx, dword [ebp-0x10]
            0x00abdc15      xor   ecx, ebp
            0x00abdc17      call  0x18075f6
            0x00abdc1c      mov   esp, ebp
            0x00abdc1e      pop   ebp
            0x00abdc1f      ret
            0x00abdc20      push  ebp
            0x00abdc21      mov   ebp, esp
            0x00abdc23      push  0xffffffff                           ; 255
            0x00abdc25      push  0x1863909
            0x00abdc2a      mov   eax, dword fs:[0x0]
            0x00abdc30      push  eax
            0x00abdc31      sub   esp, 0x64
            0x00abdc34      push  ebx
            0x00abdc35      push  esi
            0x00abdc36      push  edi
            0x00abdc37      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00abdc3c      xor   eax, ebp
            0x00abdc3e      push  eax
            0x00abdc3f      lea   eax, dword [ebp-0x0c]
            0x00abdc42      mov   dword fs:[0x0], eax
            0x00abdc48      mov   dword [ebp-0x10], 0x00
            0x00abdc4f      mov   dword [ebp-0x44], 0x00
            0x00abdc56      mov   dword [ebp-0x3c], 0x00
            0x00abdc5d      mov   dword [ebp-0x38], 0x00
            0x00abdc64      xor   eax, eax
            0x00abdc66      mov   dword [ebp-0x04], 0x01
            0x00abdc6d      mov   dword [ebp-0x58], 0x00
            0x00abdc74      mov   dword [ebp-0x50], 0x00
            0x00abdc7b      mov   dword [ebp-0x14], eax
            0x00abdc7e      mov   dword [ebp-0x4c], eax
            0x00abdc81      mov   edi, dword [ebp+0x0c]
            0x00abdc84      lea   ecx, dword [ebp-0x48]
            0x00abdc87      mov   byte [ebp-0x04], 0x02
            0x00abdc8b      push  dword [edi+0x10]
            0x00abdc8e      call  0x92a570
            0x00abdc93      mov   esi, dword [ebp-0x3c]
            0x00abdc96      xor   eax, eax
            0x00abdc98      mov   byte [ebp-0x18], 0x00
            0x00abdc9c      mov   dword [ebp-0x1c], eax
            0x00abdc9f      cmp   dword [edi+0x10], eax
        ,=< 0x00abdca2      jbe   0xabdd6a
        |   0x00abdca8      mov   ebx, dword [ebp-0x38]
        |   0x00abdcab      nop   dword [eax+eax*1], eax
       .--> 0x00abdcb0      lea   ecx, dword [eax*4]
       :|   0x00abdcb7      mov   eax, dword [edi+0x0c]
       :|   0x00abdcba      mov   dword [ebp+0x0c], ecx
       :|   0x00abdcbd      mov   eax, dword [eax+ecx*1]
       :|   0x00abdcc0      mov   ecx, dword [eax+0xdc]
       :|   0x00abdcc6      call  0xb9e1d0
       :|   0x00abdccb      test  byte [eax], 0x10
       :|   0x00abdcce      mov   eax, dword [edi+0x0c]
      ,===< 0x00abdcd1      jz    0xabdcfa
      |:|   0x00abdcd3      add   eax, dword [ebp+0x0c]
      |:|   0x00abdcd6      mov   dword [ebp+0x0c], eax
      |:|   0x00abdcd9      cmp   ebx, dword [ebp-0x44]
     ,====< 0x00abdcdc      jnz   0xabdcec
     ||:|   0x00abdcde      lea   ecx, dword [ebp-0x48]
     ||:|   0x00abdce1      call  0x92a100
     ||:|   0x00abdce6      mov   esi, dword [ebp-0x3c]
     ||:|   0x00abdce9      mov   eax, dword [ebp+0x0c]
     `----> 0x00abdcec      mov   eax, dword [eax]
      |:|   0x00abdcee      mov   ecx, dword [ebp-0x18]
      |:|   0x00abdcf1      mov   dword [esi+ebx*4], eax
      |:|   0x00abdcf4      inc   ebx
      |:|   0x00abdcf5      mov   dword [ebp-0x38], ebx
     ,====< 0x00abdcf8      jmp   0xabdd4c
     |`---> 0x00abdcfa      add   eax, dword [ebp+0x0c]
     | :|   0x00abdcfd      mov   ecx, dword [ebp-0x14]
     | :|   0x00abdd00      mov   dword [ebp-0x20], eax
     | :|   0x00abdd03      cmp   ecx, dword [ebp-0x58]
     |,===< 0x00abdd06      jnz   0xabdd16
     ||:|   0x00abdd08      lea   ecx, dword [ebp-0x5c]
     ||:|   0x00abdd0b      call  0x92a100
     ||:|   0x00abdd10      mov   eax, dword [ebp-0x20]
     ||:|   0x00abdd13      mov   ecx, dword [ebp-0x14]
     |`---> 0x00abdd16      mov   edx, dword [ebp-0x50]
     | :|   0x00abdd19      mov   eax, dword [eax]
     | :|   0x00abdd1b      mov   dword [edx+ecx*4], eax
     | :|   0x00abdd1e      inc   ecx
     | :|   0x00abdd1f      mov   eax, dword [edi+0x0c]
     | :|   0x00abdd22      add   eax, dword [ebp+0x0c]
     | :|   0x00abdd25      mov   dword [ebp-0x14], ecx
     | :|   0x00abdd28      mov   dword [ebp-0x4c], ecx
     | :|   0x00abdd2b      mov   eax, dword [eax]
     | :|   0x00abdd2d      mov   ecx, dword [eax+0xdc]
     | :|   0x00abdd33      call  0xb9e1d0
     | :|   0x00abdd38      mov   ecx, dword [ebp-0x18]
     | :|   0x00abdd3b      movzx ecx, cl
     | :|   0x00abdd3e      test  byte [eax], 0x04
     | :|   0x00abdd41      mov   eax, 0x01
     | :|   0x00abdd46      cmovnz ecx, eax
     | :|   0x00abdd49      mov   dword [ebp-0x18], ecx
     `----> 0x00abdd4c      mov   eax, dword [ebp-0x1c]
       :|   0x00abdd4f      inc   eax
       :|   0x00abdd50      mov   dword [ebp-0x1c], eax
       :|   0x00abdd53      cmp   eax, dword [edi+0x10]
       `==< 0x00abdd56      jb    0xabdcb0
        |   0x00abdd5c      test  cl, cl
       ,==< 0x00abdd5e      jz    0xabdd6a
       ||   0x00abdd60      movss xmm0, dword [0x202730c]              ; [0x202730c:4]=0
      ,===< 0x00abdd68      jmp   0xabdd72
      |``-> 0x00abdd6a      movss xmm0, dword [0x2027308]              ; [0x2027308:4]=0
      `---> 0x00abdd72      push  ecx
            0x00abdd73      movss dword [esp], xmm0
            0x00abdd78      lea   eax, dword [ebp-0x5c]
            0x00abdd7b      push  eax
            0x00abdd7c      lea   eax, dword [ebp-0x34]
            0x00abdd7f      push  eax
            0x00abdd80      call  0xac0f30
            0x00abdd85      add   esp, 0x0c
            0x00abdd88      mov   eax, dword [ebp+0x10]
            0x00abdd8b      mov   byte [ebp-0x04], 0x03
            0x00abdd8f      test  eax, eax
        ,=< 0x00abdd91      jnz   0xabde97
        |   0x00abdd97      push  dword [ebp+0x0c]
        |   0x00abdd9a      lea   eax, dword [ebp-0x34]
        |   0x00abdd9d      push  eax
        |   0x00abdd9e      lea   eax, dword [ebp-0x70]
        |   0x00abdda1      push  eax
        |   0x00abdda2      call  0xab95e0
        |   0x00abdda7      add   esp, 0x0c
        |   0x00abddaa      mov   ebx, dword [ebp+0x08]
        |   0x00abddad      lea   eax, dword [ebp-0x70]
        |   0x00abddb0      push  eax
        |   0x00abddb1      mov   ecx, ebx
        |   0x00abddb3      mov   byte [ebp-0x04], 0x04
        |   0x00abddb7      call  0xaba950
        |   0x00abddbc      lea   eax, dword [ebp-0x48]
        |   0x00abddbf      mov   byte [ebp-0x04], 0x05
        |   0x00abddc3      lea   ecx, dword [ebx+0x14]
        |   0x00abddc6      push  eax
        |   0x00abddc7      call  0x9009a0
        |   0x00abddcc      mov   dword [ebp-0x10], 0x03
        |   0x00abddd3      push  dword [ebp-0x60]
        |   0x00abddd6      mov   byte [ebp-0x04], 0x06
        |   0x00abddda      push  dword [ebp-0x64]
        |   0x00abdddd      call  0x9b21a0
        |   0x00abdde2      add   esp, 0x08
        |   0x00abdde5      mov   dword [ebp-0x60], 0x00
        |   0x00abddec      cmp   dword [ebp-0x6c], 0x00
       ,==< 0x00abddf0      jz    0xabde0d
       ||   0x00abddf2      mov   edi, dword [ebp-0x64]
       ||   0x00abddf5      test  edi, edi
      ,===< 0x00abddf7      jz    0xabde06
      |||   0x00abddf9      call  0x52b950
      |||   0x00abddfe      push  edi
      |||   0x00abddff      mov   ecx, eax
      |||   0x00abde01      call  0x52b8b0
      `---> 0x00abde06      mov   dword [ebp-0x6c], 0x00
       `--> 0x00abde0d      push  dword [ebp-0x24]
        |   0x00abde10      mov   byte [ebp-0x04], 0x07
        |   0x00abde14      push  dword [ebp-0x28]
        |   0x00abde17      call  0x9b21a0
        |   0x00abde1c      add   esp, 0x08
        |   0x00abde1f      mov   dword [ebp-0x24], 0x00
        |   0x00abde26      cmp   dword [ebp-0x30], 0x00
       ,==< 0x00abde2a      jz    0xabde47
       ||   0x00abde2c      mov   edi, dword [ebp-0x28]
       ||   0x00abde2f      test  edi, edi
      ,===< 0x00abde31      jz    0xabde40
      |||   0x00abde33      call  0x52b950
      |||   0x00abde38      push  edi
      |||   0x00abde39      mov   ecx, eax
      |||   0x00abde3b      call  0x52b8b0
      `---> 0x00abde40      mov   dword [ebp-0x30], 0x00
       `--> 0x00abde47      cmp   dword [ebp-0x58], 0x00
        |   0x00abde4b      mov   byte [ebp-0x04], 0x08
       ,==< 0x00abde4f      jz    0xabde65
       ||   0x00abde51      mov   edi, dword [ebp-0x50]
       ||   0x00abde54      test  edi, edi
      ,===< 0x00abde56      jz    0xabde65
      |||   0x00abde58      call  0x52b950
      |||   0x00abde5d      push  edi
      |||   0x00abde5e      mov   ecx, eax
      |||   0x00abde60      call  0x52b8b0
      ``--> 0x00abde65      mov   dword [ebp-0x04], 0x09
      ..--> 0x00abde6c      cmp   dword [ebp-0x44], 0x00
     ,====< 0x00abde70      jz    0xabde83
     |::|   0x00abde72      test  esi, esi
    ,=====< 0x00abde74      jz    0xabde83
    ||::|   0x00abde76      call  0x52b950
    ||::|   0x00abde7b      push  esi
    ||::|   0x00abde7c      mov   ecx, eax
    ||::|   0x00abde7e      call  0x52b8b0
    ``----> 0x00abde83      mov   eax, ebx
      ::|   0x00abde85      mov   ecx, dword [ebp-0x0c]
      ::|   0x00abde88      mov   dword fs:[0x0], ecx
      ::|   0x00abde8f      pop   ecx
      ::|   0x00abde90      pop   edi
      ::|   0x00abde91      pop   esi
      ::|   0x00abde92      pop   ebx
      ::|   0x00abde93      mov   esp, ebp
      ::|   0x00abde95      pop   ebp
      ::|   0x00abde96      ret
      ::`-> 0x00abde97      cmp   eax, 0x01                            ; 1
      ::,=< 0x00abde9a      jnz   0xabdf7a
      ::|   0x00abdea0      push  dword [ebp+0x0c]
      ::|   0x00abdea3      lea   eax, dword [ebp-0x34]
      ::|   0x00abdea6      push  eax
      ::|   0x00abdea7      lea   eax, dword [ebp-0x70]
      ::|   0x00abdeaa      push  eax
      ::|   0x00abdeab      call  0xab97a0
      ::|   0x00abdeb0      add   esp, 0x0c
      ::|   0x00abdeb3      mov   ebx, dword [ebp+0x08]
      ::|   0x00abdeb6      lea   eax, dword [ebp-0x70]
      ::|   0x00abdeb9      push  eax
      ::|   0x00abdeba      mov   ecx, ebx
      ::|   0x00abdebc      mov   byte [ebp-0x04], 0x0a
      ::|   0x00abdec0      call  0xaba950
      ::|   0x00abdec5      lea   eax, dword [ebp-0x48]
      ::|   0x00abdec8      mov   byte [ebp-0x04], 0x0b                ; 0xb ; 11
      ::|   0x00abdecc      lea   ecx, dword [ebx+0x14]
      ::|   0x00abdecf      push  eax
      ::|   0x00abded0      call  0x9009a0
      ::|   0x00abded5      mov   dword [ebp-0x10], 0x05
      ::|   0x00abdedc      push  dword [ebp-0x60]
      ::|   0x00abdedf      mov   byte [ebp-0x04], 0x0c                ; 0xc ; 12
      ::|   0x00abdee3      push  dword [ebp-0x64]
      ::|   0x00abdee6      call  0x9b21a0
      ::|   0x00abdeeb      add   esp, 0x08
      ::|   0x00abdeee      mov   dword [ebp-0x60], 0x00
      ::|   0x00abdef5      cmp   dword [ebp-0x6c], 0x00
     ,====< 0x00abdef9      jz    0xabdf16
     |::|   0x00abdefb      mov   edi, dword [ebp-0x64]
     |::|   0x00abdefe      test  edi, edi
    ,=====< 0x00abdf00      jz    0xabdf0f
    ||::|   0x00abdf02      call  0x52b950
    ||::|   0x00abdf07      push  edi
    ||::|   0x00abdf08      mov   ecx, eax
    ||::|   0x00abdf0a      call  0x52b8b0
    `-----> 0x00abdf0f      mov   dword [ebp-0x6c], 0x00
     `----> 0x00abdf16      push  dword [ebp-0x24]
      ::|   0x00abdf19      mov   byte [ebp-0x04], 0x0d                ; 0xd ; 13
      ::|   0x00abdf1d      push  dword [ebp-0x28]
      ::|   0x00abdf20      call  0x9b21a0
      ::|   0x00abdf25      add   esp, 0x08
      ::|   0x00abdf28      mov   dword [ebp-0x24], 0x00
      ::|   0x00abdf2f      cmp   dword [ebp-0x30], 0x00
     ,====< 0x00abdf33      jz    0xabdf50
     |::|   0x00abdf35      mov   edi, dword [ebp-0x28]
     |::|   0x00abdf38      test  edi, edi
    ,=====< 0x00abdf3a      jz    0xabdf49
    ||::|   0x00abdf3c      call  0x52b950
    ||::|   0x00abdf41      push  edi
    ||::|   0x00abdf42      mov   ecx, eax
    ||::|   0x00abdf44      call  0x52b8b0
    `-----> 0x00abdf49      mov   dword [ebp-0x30], 0x00
     `----> 0x00abdf50      cmp   dword [ebp-0x58], 0x00
      ::|   0x00abdf54      mov   byte [ebp-0x04], 0x0e                ; 0xe ; 14
     ,====< 0x00abdf58      jz    0xabdf6e
     |::|   0x00abdf5a      mov   edi, dword [ebp-0x50]
     |::|   0x00abdf5d      test  edi, edi
    ,=====< 0x00abdf5f      jz    0xabdf6e
    ||::|   0x00abdf61      call  0x52b950
    ||::|   0x00abdf66      push  edi
    ||::|   0x00abdf67      mov   ecx, eax
    ||::|   0x00abdf69      call  0x52b8b0
    ``----> 0x00abdf6e      mov   dword [ebp-0x04], 0x0f               ; 0xf ; 15
      `===< 0x00abdf75      jmp   0xabde6c
       :`-> 0x00abdf7a      cmp   eax, 0x02                            ; 2
       :    0x00abdf7d      lea   eax, dword [ebp-0x34]
       :,=< 0x00abdf80      jnz   0xabe05d
       :|   0x00abdf86      push  dword [ebp+0x0c]
       :|   0x00abdf89      push  eax
       :|   0x00abdf8a      lea   eax, dword [ebp-0x70]
       :|   0x00abdf8d      push  eax
       :|   0x00abdf8e      call  0xab99a0
       :|   0x00abdf93      add   esp, 0x0c
       :|   0x00abdf96      mov   ebx, dword [ebp+0x08]
       :|   0x00abdf99      lea   eax, dword [ebp-0x70]
       :|   0x00abdf9c      push  eax
       :|   0x00abdf9d      mov   ecx, ebx
       :|   0x00abdf9f      mov   byte [ebp-0x04], 0x10                ; 16
       :|   0x00abdfa3      call  0xaba950
       :|   0x00abdfa8      lea   eax, dword [ebp-0x48]
       :|   0x00abdfab      mov   byte [ebp-0x04], 0x11                ; 17
       :|   0x00abdfaf      lea   ecx, dword [ebx+0x14]
       :|   0x00abdfb2      push  eax
       :|   0x00abdfb3      call  0x9009a0
       :|   0x00abdfb8      mov   dword [ebp-0x10], 0x09
       :|   0x00abdfbf      push  dword [ebp-0x60]
       :|   0x00abdfc2      mov   byte [ebp-0x04], 0x12                ; 18
       :|   0x00abdfc6      push  dword [ebp-0x64]
       :|   0x00abdfc9      call  0x9b21a0
       :|   0x00abdfce      add   esp, 0x08
       :|   0x00abdfd1      mov   dword [ebp-0x60], 0x00
       :|   0x00abdfd8      cmp   dword [ebp-0x6c], 0x00
      ,===< 0x00abdfdc      jz    0xabdff9
      |:|   0x00abdfde      mov   edi, dword [ebp-0x64]
      |:|   0x00abdfe1      test  edi, edi
     ,====< 0x00abdfe3      jz    0xabdff2
     ||:|   0x00abdfe5      call  0x52b950
     ||:|   0x00abdfea      push  edi
     ||:|   0x00abdfeb      mov   ecx, eax
     ||:|   0x00abdfed      call  0x52b8b0
     `----> 0x00abdff2      mov   dword [ebp-0x6c], 0x00
      `---> 0x00abdff9      push  dword [ebp-0x24]
       :|   0x00abdffc      mov   byte [ebp-0x04], 0x13                ; 19
       :|   0x00abe000      push  dword [ebp-0x28]
       :|   0x00abe003      call  0x9b21a0
       :|   0x00abe008      add   esp, 0x08
       :|   0x00abe00b      mov   dword [ebp-0x24], 0x00
       :|   0x00abe012      cmp   dword [ebp-0x30], 0x00
      ,===< 0x00abe016      jz    0xabe033
      |:|   0x00abe018      mov   edi, dword [ebp-0x28]
      |:|   0x00abe01b      test  edi, edi
     ,====< 0x00abe01d      jz    0xabe02c
     ||:|   0x00abe01f      call  0x52b950
     ||:|   0x00abe024      push  edi
     ||:|   0x00abe025      mov   ecx, eax
     ||:|   0x00abe027      call  0x52b8b0
     `----> 0x00abe02c      mov   dword [ebp-0x30], 0x00
      `---> 0x00abe033      cmp   dword [ebp-0x58], 0x00
       :|   0x00abe037      mov   byte [ebp-0x04], 0x14                ; 20
      ,===< 0x00abe03b      jz    0xabe051
      |:|   0x00abe03d      mov   edi, dword [ebp-0x50]
      |:|   0x00abe040      test  edi, edi
     ,====< 0x00abe042      jz    0xabe051
     ||:|   0x00abe044      call  0x52b950
     ||:|   0x00abe049      push  edi
     ||:|   0x00abe04a      mov   ecx, eax
     ||:|   0x00abe04c      call  0x52b8b0
     ``---> 0x00abe051      mov   dword [ebp-0x04], 0x15               ; 21
       `==< 0x00abe058      jmp   0xabde6c
        `-> 0x00abe05d      mov   edi, dword [ebp+0x08]
            0x00abe060      mov   ecx, edi
            0x00abe062      push  eax
            0x00abe063      call  0xaba950
            0x00abe068      lea   eax, dword [ebp-0x48]
            0x00abe06b      mov   byte [ebp-0x04], 0x16                ; 22
            0x00abe06f      lea   ecx, dword [edi+0x14]
            0x00abe072      push  eax
            0x00abe073      call  0x9009a0
            0x00abe078      mov   dword [ebp-0x10], 0x11               ; 17
            0x00abe07f      push  dword [ebp-0x24]
            0x00abe082      mov   byte [ebp-0x04], 0x17                ; 23
            0x00abe086      push  dword [ebp-0x28]
            0x00abe089      call  0x9b21a0
            0x00abe08e      add   esp, 0x08
            0x00abe091      mov   dword [ebp-0x24], 0x00
            0x00abe098      cmp   dword [ebp-0x30], 0x00
        ,=< 0x00abe09c      jz    0xabe0b9
        |   0x00abe09e      mov   ebx, dword [ebp-0x28]
        |   0x00abe0a1      test  ebx, ebx
       ,==< 0x00abe0a3      jz    0xabe0b2
       ||   0x00abe0a5      call  0x52b950
       ||   0x00abe0aa      push  ebx
       ||   0x00abe0ab      mov   ecx, eax
       ||   0x00abe0ad      call  0x52b8b0
       `--> 0x00abe0b2      mov   dword [ebp-0x30], 0x00
        `-> 0x00abe0b9      cmp   dword [ebp-0x58], 0x00
            0x00abe0bd      mov   byte [ebp-0x04], 0x18                ; 24
        ,=< 0x00abe0c1      jz    0xabe0d7
        |   0x00abe0c3      mov   ebx, dword [ebp-0x50]
        |   0x00abe0c6      test  ebx, ebx
       ,==< 0x00abe0c8      jz    0xabe0d7
       ||   0x00abe0ca      call  0x52b950
       ||   0x00abe0cf      push  ebx
       ||   0x00abe0d0      mov   ecx, eax
       ||   0x00abe0d2      call  0x52b8b0
       ``-> 0x00abe0d7      cmp   dword [ebp-0x44], 0x00
            0x00abe0db      mov   dword [ebp-0x04], 0x19               ; 25
        ,=< 0x00abe0e2      jz    0xabe0f5
        |   0x00abe0e4      test  esi, esi
       ,==< 0x00abe0e6      jz    0xabe0f5
       ||   0x00abe0e8      call  0x52b950
       ||   0x00abe0ed      push  esi
       ||   0x00abe0ee      mov   ecx, eax
       ||   0x00abe0f0      call  0x52b8b0
       ``-> 0x00abe0f5      mov   eax, edi
            0x00abe0f7      mov   ecx, dword [ebp-0x0c]
            0x00abe0fa      mov   dword fs:[0x0], ecx
            0x00abe101      pop   ecx
            0x00abe102      pop   edi
            0x00abe103      pop   esi
            0x00abe104      pop   ebx
            0x00abe105      mov   esp, ebp
            0x00abe107      pop   ebp
            0x00abe108      ret
            0x00abe109      int3
            0x00abe10a      int3
            0x00abe10b      int3
            0x00abe10c      int3
            0x00abe10d      int3
            0x00abe10e      int3
            0x00abe10f      int3
            0x00abe110      push  ebp
            0x00abe111      mov   ebp, esp
            0x00abe113      push  0xffffffff                           ; 255
            0x00abe115      push  0x1810663
            0x00abe11a      mov   eax, dword fs:[0x0]
            0x00abe120      push  eax
            0x00abe121      push  ecx
            0x00abe122      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00abe127      xor   eax, ebp
            0x00abe129      push  eax
            0x00abe12a      lea   eax, dword [ebp-0x0c]
            0x00abe12d      mov   dword fs:[0x0], eax
            0x00abe133      cmp   dword [0x203a2ac], 0x00              ; [0x203a2ac:4]=0
        ,=< 0x00abe13a      jnz   0xabe141
        |   0x00abe13c      call  0xb05260
        `-> 0x00abe141      mov   eax, dword [0x2038304]               ; [0x2038304:4]=0
            0x00abe146      test  eax, eax
        ,=< 0x00abe148      jnz   0xabe1a5
        |   0x00abe14a      push  dword [0x1d6c084]
        |   0x00abe150      push  0x01                                 ; 1
        |   0x00abe152      push  0xac                                 ; 172
        |   0x00abe157      push  0x01                                 ; 1
        |   0x00abe159      call  0x529280
        |   0x00abe15e      add   esp, 0x10
        |   0x00abe161      mov   dword [ebp-0x10], eax
        |   0x00abe164      mov   dword [ebp-0x04], 0x00
        |   0x00abe16b      test  eax, eax
       ,==< 0x00abe16d      jz    0xabe19e
       ||   0x00abe16f      push  0x00
       ||   0x00abe171      push  0x18                                 ; 24
       ||   0x00abe173      push  str.TGroupModuleDescriptor           ; 0x199cb7c ; "TGroupModuleDescriptor"
       ||   0x00abe178      push  0xac0140
       ||   0x00abe17d      push  dword [0x203a2ac]
       ||   0x00abe183      mov   ecx, eax
       ||   0x00abe185      call  0x54f0b0
       ||   0x00abe18a      mov   dword [0x2038304], eax
       ||   0x00abe18f      mov   ecx, dword [ebp-0x0c]
       ||   0x00abe192      mov   dword fs:[0x0], ecx
       ||   0x00abe199      pop   ecx
       ||   0x00abe19a      mov   esp, ebp
       ||   0x00abe19c      pop   ebp
       ||   0x00abe19d      ret
       `--> 0x00abe19e      xor   eax, eax
        |   0x00abe1a0      mov   dword [0x2038304], eax
        `-> 0x00abe1a5      mov   ecx, dword [ebp-0x0c]
            0x00abe1a8      mov   dword fs:[0x0], ecx
            0x00abe1af      pop   ecx
            0x00abe1b0      mov   esp, ebp
            0x00abe1b2      pop   ebp
            0x00abe1b3      ret
            0x00abe1b4      int3
            0x00abe1b5      int3
            0x00abe1b6      int3
            0x00abe1b7      int3
            0x00abe1b8      int3
            0x00abe1b9      int3
            0x00abe1ba      int3
            0x00abe1bb      int3
            0x00abe1bc      int3
            0x00abe1bd      int3
            0x00abe1be      int3
            0x00abe1bf      int3
            0x00abe1c0      push  ebp
            0x00abe1c1      mov   ebp, esp
            0x00abe1c3      push  0xffffffff                           ; 255
            0x00abe1c5      push  0x1810663
            0x00abe1ca      mov   eax, dword fs:[0x0]
            0x00abe1d0      push  eax
            0x00abe1d1      push  ecx
            0x00abe1d2      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00abe1d7      xor   eax, ebp
            0x00abe1d9      push  eax
            0x00abe1da      lea   eax, dword [ebp-0x0c]
            0x00abe1dd      mov   dword fs:[0x0], eax
            0x00abe1e3      cmp   dword [0x203a2ac], 0x00              ; [0x203a2ac:4]=0
        ,=< 0x00abe1ea      jnz   0xabe1f1
        |   0x00abe1ec      call  0xb05260
        `-> 0x00abe1f1      mov   eax, dword [0x2038300]               ; [0x2038300:4]=0
            0x00abe1f6      test  eax, eax
        ,=< 0x00abe1f8      jnz   0xabe255
        |   0x00abe1fa      push  dword [0x1d6c084]
        |   0x00abe200      push  0x01                                 ; 1
        |   0x00abe202      push  0xac                                 ; 172
        |   0x00abe207      push  0x01                                 ; 1
        |   0x00abe209      call  0x529280
        |   0x00abe20e      add   esp, 0x10
        |   0x00abe211      mov   dword [ebp-0x10], eax
        |   0x00abe214      mov   dword [ebp-0x04], 0x00
        |   0x00abe21b      test  eax, eax
       ,==< 0x00abe21d      jz    0xabe24e
       ||   0x00abe21f      push  0x00
       ||   0x00abe221      push  0x18                                 ; 24
       ||   0x00abe223      push  str.TGroupableUnitModuleDescriptor   ; 0x199cb4c ; "TGroupableUnitModuleDescriptor"
       ||   0x00abe228      push  0xac01c0
       ||   0x00abe22d      push  dword [0x203a2ac]
       ||   0x00abe233      mov   ecx, eax
       ||   0x00abe235      call  0x54f0b0
       ||   0x00abe23a      mov   dword [0x2038300], eax
       ||   0x00abe23f      mov   ecx, dword [ebp-0x0c]
       ||   0x00abe242      mov   dword fs:[0x0], ecx
       ||   0x00abe249      pop   ecx
       ||   0x00abe24a      mov   esp, ebp
       ||   0x00abe24c      pop   ebp
       ||   0x00abe24d      ret
       `--> 0x00abe24e      xor   eax, eax
        |   0x00abe250      mov   dword [0x2038300], eax
        `-> 0x00abe255      mov   ecx, dword [ebp-0x0c]
            0x00abe258      mov   dword fs:[0x0], ecx
            0x00abe25f      pop   ecx
            0x00abe260      mov   esp, ebp
            0x00abe262      pop   ebp
            0x00abe263      ret
            0x00abe264      int3
            0x00abe265      int3
            0x00abe266      int3
            0x00abe267      int3
            0x00abe268      int3
            0x00abe269      int3
            0x00abe26a      int3
            0x00abe26b      int3
            0x00abe26c      int3
            0x00abe26d      int3
            0x00abe26e      int3
            0x00abe26f      int3
            0x00abe270      push  ebp
            0x00abe271      mov   ebp, esp
            0x00abe273      push  0xffffffff                           ; 255
            0x00abe275      push  0x1863938
            0x00abe27a      mov   eax, dword fs:[0x0]
            0x00abe280      push  eax
            0x00abe281      push  ecx
            0x00abe282      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00abe287      xor   eax, ebp
            0x00abe289      push  eax
            0x00abe28a      lea   eax, dword [ebp-0x0c]
            0x00abe28d      mov   dword fs:[0x0], eax
            0x00abe293      lea   ecx, dword [ebp-0x10]
            0x00abe296      call  0x4f6c50
            0x00abe29b      push  eax
            0x00abe29c      push  dword [ebp+0x08]
            0x00abe29f      mov   dword [ebp-0x04], 0x00
            0x00abe2a6      call  0xaff990
            0x00abe2ab      add   esp, 0x08
            0x00abe2ae      lea   ecx, dword [ebp-0x10]
            0x00abe2b1      call  0x4dc500
            0x00abe2b6      mov   ecx, dword [ebp-0x0c]
            0x00abe2b9      mov   dword fs:[0x0], ecx
            0x00abe2c0      pop   ecx
            0x00abe2c1      mov   esp, ebp
            0x00abe2c3      pop   ebp
            0x00abe2c4      ret
            0x00abe2c5      int3
            0x00abe2c6      int3
            0x00abe2c7      int3
            0x00abe2c8      int3
            0x00abe2c9      int3
            0x00abe2ca      int3
            0x00abe2cb      int3
            0x00abe2cc      int3
            0x00abe2cd      int3
            0x00abe2ce      int3
            0x00abe2cf      int3
        .-> 0x00abe2d0      mov   eax, dword [0x201e2dc]               ; [0x201e2dc:4]=0
        :   0x00abe2d5      push  esi
        :   0x00abe2d6      mov   esi, dword [esp+0x08]
        :   0x00abe2da      mov   edx, dword [eax+0x2b4]
        :   0x00abe2e0      mov   eax, dword [edx+0x0c]
        :   0x00abe2e3      mov   ecx, dword [edx+0x10]
        :   0x00abe2e6      lea   ecx, dword [eax+ecx*4]
        :   0x00abe2e9      cmp   eax, ecx
       ,==< 0x00abe2eb      jz    0xabe30d
       |:   0x00abe2ed      nop   dword [eax], eax
      .---> 0x00abe2f0      cmp   dword [eax], esi
     ,====< 0x00abe2f2      jz    0xabe2fb
     |:|:   0x00abe2f4      add   eax, 0x04
     |:|:   0x00abe2f7      cmp   eax, ecx
     |`===< 0x00abe2f9      jnz   0xabe2f0
     `----> 0x00abe2fb      cmp   eax, ecx
      ,===< 0x00abe2fd      jz    0xabe30d
      ||:   0x00abe2ff      push  eax
      ||:   0x00abe300      lea   eax, dword [esp+0x0c]
      ||:   0x00abe304      push  eax
      ||:   0x00abe305      lea   ecx, dword [edx+0x0c]
      ||:   0x00abe308      call  0x522f00
      ``--> 0x00abe30d      test  esi, esi
       ,==< 0x00abe30f      jz    0xabe31a
       |:   0x00abe311      push  0x01                                 ; 1
       |:   0x00abe313      mov   ecx, esi
       |:   0x00abe315      call  0xabb610
       `--> 0x00abe31a      pop   esi
        :   0x00abe31b      ret
        :   0x00abe31c      int3
        :   0x00abe31d      int3
        :   0x00abe31e      int3
        :   0x00abe31f      int3
        :   0x00abe320      push  esi
        :   0x00abe321      mov   esi, ecx
        :   0x00abe323      mov   ecx, dword [esi+0x14]
        :   0x00abe326      mov   eax, dword [ecx]
        :   0x00abe328      call  dword [eax+0x24]                     ; 36
        :   0x00abe32b      movzx edx, word [esp+0x08]
        :   0x00abe330      lea   edx, dword [edx+edx*2]
        :   0x00abe333      lea   ecx, dword [eax+edx*2]
        :   0x00abe336      mov   eax, dword [esi+0x08]
        :   0x00abe339      add   eax, ecx
        :   0x00abe33b      pop   esi
        :   0x00abe33c      ret   0x04
        :   0x00abe33f      int3
        `=< 0x00abe340      jmp   0xabe2d0
            0x00abe345      int3
            0x00abe346      int3
            0x00abe347      int3
            0x00abe348      int3
            0x00abe349      int3
            0x00abe34a      int3
            0x00abe34b      int3
            0x00abe34c      int3
            0x00abe34d      int3
            0x00abe34e      int3
            0x00abe34f      int3
            0x00abe350      sub   esp, 0x14
            0x00abe353      push  ebx
            0x00abe354      push  ebp
            0x00abe355      mov   ebp, ecx
            0x00abe357      push  esi
            0x00abe358      push  edi
            0x00abe359      mov   edi, 0x0e                            ; 0xe ; 14
            0x00abe35e      mov   esi, dword [ebp]
            0x00abe361      mov   eax, esi
            0x00abe363      shr   eax, 0x1b
            0x00abe366      mov   ebx, dword [ebp+0x04]
            0x00abe369      mov   dword [esp+0x10], ebx
            0x00abe36d      lea   edx, dword [eax-0x01]
            0x00abe370      cmp   edx, edi
            0x00abe372      mov   ecx, edx
            0x00abe374      cmovb ecx, edi
            0x00abe377      mov   edi, 0x01
            0x00abe37c      mov   dword [esp+0x14], ecx
            0x00abe380      and   esi, 0x7ffffff
            0x00abe386      lea   ecx, dword [eax-0x01]
            0x00abe389      mov   dword [esp+0x18], esi
            0x00abe38d      shl   edi, cl
            0x00abe38f      mov   ecx, dword [esp+0x14]
            0x00abe393      add   ecx, 0xffffffe0                      ; 4294967264
            0x00abe396      add   eax, ecx
            0x00abe398      xor   ecx, ecx
            0x00abe39a      test  eax, eax
            0x00abe39c      cmovnle ecx, eax
            0x00abe39f      mov   eax, 0x08
            0x00abe3a4      mov   dword [esp+0x1c], ecx
            0x00abe3a8      mov   ecx, edx
            0x00abe3aa      shl   eax, cl
            0x00abe3ac      mov   ecx, dword [esp+0x28]
            0x00abe3b0      add   eax, ebx
            0x00abe3b2      mov   dword [esp+0x20], eax
            0x00abe3b6      mov   ebx, dword [eax+ecx*4]
            0x00abe3b9      test  ebx, ebx
        ,=< 0x00abe3bb      jnz   0xabe3c9
        |   0x00abe3bd      pop   edi
        |   0x00abe3be      pop   esi
        |   0x00abe3bf      pop   ebp
        |   0x00abe3c0      xor   al, al
        |   0x00abe3c2      pop   ebx
        |   0x00abe3c3      add   esp, 0x14
        |   0x00abe3c6      ret   0x08
        `-> 0x00abe3c9      push  ecx
            0x00abe3ca      push  dword [esp+0x20]
            0x00abe3ce      lea   ecx, dword [edi*2-0x01]
            0x00abe3d5      push  dword [esp+0x1c]
            0x00abe3d9      lea   edx, dword [edi-0x01]
            0x00abe3dc      push  ecx
            0x00abe3dd      push  eax
            0x00abe3de      and   ebx, edx
            0x00abe3e0      call  0x504490
            0x00abe3e5      mov   edx, dword [esp+0x40]
            0x00abe3e9      add   esp, 0x14
            0x00abe3ec      test  edx, edx
        ,=< 0x00abe3ee      jz    0xabe416
        |   0x00abe3f0      mov   eax, dword [esp+0x10]
        |   0x00abe3f4      mov   esi, dword [esp+0x10]
        |   0x00abe3f8      mov   ecx, dword [eax+ebx*8]
        |   0x00abe3fb      mov   eax, dword [edx]
        |   0x00abe3fd      mov   dword [esi+ebx*8], eax
        |   0x00abe400      mov   eax, esi
        |   0x00abe402      mov   dword [edx], ecx
        |   0x00abe404      mov   ecx, dword [eax+ebx*8+0x04]
        |   0x00abe408      mov   eax, dword [edx+0x04]
        |   0x00abe40b      mov   dword [esi+ebx*8+0x04], eax
        |   0x00abe40f      mov   esi, dword [esp+0x18]
        |   0x00abe413      mov   dword [edx+0x04], ecx
        `-> 0x00abe416      lea   eax, dword [esi-0x01]
            0x00abe419      cmp   ebx, eax
        ,=< 0x00abe41b      jz    0xabe46b
        |   0x00abe41d      mov   ecx, dword [esp+0x10]
        |   0x00abe421      lea   esi, dword [ecx+eax*8]
        |   0x00abe424      lea   eax, dword [esi+0x08]
        |   0x00abe427      push  eax
        |   0x00abe428      push  esi
        |   0x00abe429      call  0x520a10
        |   0x00abe42e      add   esp, 0x08
        |   0x00abe431      lea   ecx, dword [esp+0x28]
        |   0x00abe435      push  ecx
        |   0x00abe436      push  eax
        |   0x00abe437      push  esi
        |   0x00abe438      mov   ecx, ebp
        |   0x00abe43a      call  0xab8300
        |   0x00abe43f      mov   ecx, dword [esp+0x20]
        |   0x00abe443      lea   ecx, dword [ecx+eax*4]
        |   0x00abe446      mov   eax, edi
        |   0x00abe448      neg   eax
        |   0x00abe44a      and   eax, dword [ecx]
        |   0x00abe44c      or    eax, ebx
        |   0x00abe44e      mov   dword [ecx], eax
        |   0x00abe450      mov   eax, dword [esi]
        |   0x00abe452      mov   ecx, dword [esp+0x10]
        |   0x00abe456      mov   dword [ecx+ebx*8], eax
        |   0x00abe459      mov   byte [esi], 0xdd                     ; [0xdd:1]=255 ; 221
        |   0x00abe45c      mov   eax, dword [esi+0x04]
        |   0x00abe45f      mov   dword [ecx+ebx*8+0x04], eax
        |   0x00abe463      mov   byte [esi+0x04], 0xdd                ; [0xdd:1]=255 ; 221
        |   0x00abe467      mov   esi, dword [esp+0x18]
        `-> 0x00abe46b      mov   eax, dword [ebp]
            0x00abe46e      lea   ecx, dword [esi-0x01]
            0x00abe471      and   eax, 0xf8000000
            0x00abe476      or    eax, ecx
            0x00abe478      mov   dword [ebp], eax
            0x00abe47b      lea   eax, dword [esi+esi*1]
            0x00abe47e      cmp   eax, edi
        ,=< 0x00abe480      jnbe  0xabe491
        |   0x00abe482      push  0xab8c60
        |   0x00abe487      shr   edi, 0x01
        |   0x00abe489      mov   ecx, ebp
        |   0x00abe48b      push  edi
        |   0x00abe48c      call  0x546430
        `-> 0x00abe491      pop   edi
            0x00abe492      pop   esi
            0x00abe493      pop   ebp
            0x00abe494      mov   al, 0x01
            0x00abe496      pop   ebx
            0x00abe497      add   esp, 0x14
            0x00abe49a      ret   0x08
            0x00abe49d      int3
            0x00abe49e      int3
            0x00abe49f      int3
            0x00abe4a0      push  ebx
            0x00abe4a1      push  ebp
            0x00abe4a2      mov   ebp, ecx
            0x00abe4a4      push  esi
            0x00abe4a5      xor   esi, esi
            0x00abe4a7      push  edi
            0x00abe4a8      mov   ebx, dword [ebp+0x14]
            0x00abe4ab      mov   edx, dword [ebx+0x10]
            0x00abe4ae      lea   ecx, dword [ebx+0x0c]
            0x00abe4b1      mov   edi, dword [esp+0x14]
            0x00abe4b5      test  edx, edx
        ,=< 0x00abe4b7      jz    0xabe4cc
        |   0x00abe4b9      mov   eax, dword [ecx]
        |   0x00abe4bb      nop   dword [eax+eax*1], eax
       .--> 0x00abe4c0      cmp   dword [eax], edi
      ,===< 0x00abe4c2      jz    0xabe4ce
      |:|   0x00abe4c4      inc   esi
      |:|   0x00abe4c5      add   eax, 0x04
      |:|   0x00abe4c8      cmp   esi, edx
      |`==< 0x00abe4ca      jb    0xabe4c0
      | `-> 0x00abe4cc      mov   esi, edx
      `---> 0x00abe4ce      cmp   esi, dword [ebx+0x10]
        ,=< 0x00abe4d1      jz    0xabe4ef
        |   0x00abe4d3      push  esi
        |   0x00abe4d4      lea   eax, dword [esp+0x18]
        |   0x00abe4d8      push  eax
        |   0x00abe4d9      call  0x929ff0
        |   0x00abe4de      push  esi
        |   0x00abe4df      lea   eax, dword [esp+0x18]
        |   0x00abe4e3      push  eax
        |   0x00abe4e4      lea   ecx, dword [ebx+0xd0]
        |   0x00abe4ea      call  0xa699c0
        `-> 0x00abe4ef      mov   eax, dword [ebx+0x20]
            0x00abe4f2      mov   ecx, dword [ebx+0x24]
            0x00abe4f5      lea   ecx, dword [eax+ecx*4]
            0x00abe4f8      cmp   eax, ecx
        ,=< 0x00abe4fa      jz    0xabe520
        |   0x00abe4fc      nop   dword [eax], eax
       .--> 0x00abe500      mov   esi, dword [eax]
       :|   0x00abe502      lea   edx, dword [eax+0x04]
       :|   0x00abe505      cmp   esi, edi
      ,===< 0x00abe507      jz    0xabe511
      |:|   0x00abe509      mov   eax, edx
      |:|   0x00abe50b      cmp   eax, ecx
      |`==< 0x00abe50d      jnz   0xabe500
      | |   0x00abe50f      invalid
        ,=< 0x00c99e02      jbe   0xc99e42
        |   0x00c99e04      mov   edi, dword [esi+0x124]
        |   0x00c99e0a      xor   ecx, ecx
        |   0x00c99e0c      nop   dword [eax], eax
       .--> 0x00c99e10      mov   eax, dword [ebp-0xb4]
       :|   0x00c99e16      lea   ecx, dword [ecx+0x14]
       :|   0x00c99e19      inc   edx
       :|   0x00c99e1a      mov   eax, dword [eax]
       :|   0x00c99e1c      mov   dword [edi+ecx*1-0x0c], eax
       :|   0x00c99e20      mov   eax, dword [ebp-0xb4]
       :|   0x00c99e26      mov   eax, dword [eax+0x04]
       :|   0x00c99e29      mov   dword [edi+ecx*1-0x08], eax
       :|   0x00c99e2d      mov   eax, dword [ebp-0xb4]
       :|   0x00c99e33      mov   eax, dword [eax+0x08]
       :|   0x00c99e36      mov   dword [edi+ecx*1-0x04], eax
       :|   0x00c99e3a      cmp   edx, dword [esi+0x128]
       `==< 0x00c99e40      jb    0xc99e10
        `-> 0x00c99e42      xor   edi, edi
            0x00c99e44      cmp   dword [esi+0x114], edi
        ,=< 0x00c99e4a      jbe   0xc99e77
        |   0x00c99e4c      xor   edx, edx
        |   0x00c99e4e      nop
       .--> 0x00c99e50      mov   ecx, dword [esi+0x110]
       :|   0x00c99e56      cmp   dword [ecx+edx*1+0x04], 0xffffffff
      ,===< 0x00c99e5b      jnz   0xc99e6b
      |:|   0x00c99e5d      mov   eax, dword [ebp-0xc0]
      |:|   0x00c99e63      mov   eax, dword [eax]
      |:|   0x00c99e65      mov   eax, dword [eax]
      |:|   0x00c99e67      mov   dword [ecx+edx*1+0x04], eax
      `---> 0x00c99e6b      inc   edi
       :|   0x00c99e6c      add   edx, 0x14                            ; 20
       :|   0x00c99e6f      cmp   edi, dword [esi+0x114]
       `==< 0x00c99e75      jb    0xc99e50
        `-> 0x00c99e77      xor   edx, edx
            0x00c99e79      cmp   dword [esi+0x150], edx
        ,=< 0x00c99e7f      jbe   0xc99ec2
        |   0x00c99e81      mov   edi, dword [esi+0x14c]
        |   0x00c99e87      xor   ecx, ecx
        |   0x00c99e89      nop   dword [eax], eax
       .--> 0x00c99e90      mov   eax, dword [ebp-0xb4]
       :|   0x00c99e96      lea   ecx, dword [ecx+0x14]
       :|   0x00c99e99      inc   edx
       :|   0x00c99e9a      mov   eax, dword [eax]
       :|   0x00c99e9c      mov   dword [ecx+edi*1-0x0c], eax
       :|   0x00c99ea0      mov   eax, dword [ebp-0xb4]
       :|   0x00c99ea6      mov   eax, dword [eax+0x04]
       :|   0x00c99ea9      mov   dword [ecx+edi*1-0x08], eax
       :|   0x00c99ead      mov   eax, dword [ebp-0xb4]
       :|   0x00c99eb3      mov   eax, dword [eax+0x08]
       :|   0x00c99eb6      mov   dword [ecx+edi*1-0x04], eax
       :|   0x00c99eba      cmp   edx, dword [esi+0x150]
       `==< 0x00c99ec0      jb    0xc99e90
        `-> 0x00c99ec2      mov   eax, dword [ebp-0xc0]
            0x00c99ec8      cmp   dword [eax+0x04], 0x00
        ,=< 0x00c99ecc      jz    0xc99f07
        |   0x00c99ece      xor   edx, edx
        |   0x00c99ed0      cmp   dword [esi+0x1a0], edx
       ,==< 0x00c99ed6      jbe   0xc99f07
       ||   0x00c99ed8      xor   edi, edi
       ||   0x00c99eda      nop   word [eax+eax*1], ax
      .---> 0x00c99ee0      mov   ecx, dword [esi+0x19c]
      :||   0x00c99ee6      cmp   dword [ecx+edi*1+0x04], 0xffffffff
     ,====< 0x00c99eeb      jnz   0xc99efb
     |:||   0x00c99eed      mov   eax, dword [eax]
     |:||   0x00c99eef      mov   eax, dword [eax]
     |:||   0x00c99ef1      mov   dword [ecx+edi*1+0x04], eax
     |:||   0x00c99ef5      mov   eax, dword [ebp-0xc0]
     `----> 0x00c99efb      inc   edx
      :||   0x00c99efc      add   edi, 0x14                            ; 20
      :||   0x00c99eff      cmp   edx, dword [esi+0x1a0]
      `===< 0x00c99f05      jb    0xc99ee0
       ``-> 0x00c99f07      xor   edx, edx
            0x00c99f09      cmp   dword [esi+0x1b4], edx
        ,=< 0x00c99f0f      jbe   0xc99f3a
        |   0x00c99f11      xor   edi, edi
        |   0x00c99f13      mov   ecx, dword [esi+0x1b0]
        |   0x00c99f19      cmp   dword [ecx+edi*1+0x04], 0xffffffff
       ,==< 0x00c99f1e      jnz   0xc99f28
       ||   0x00c99f20      mov   eax, dword [eax]
       ||   0x00c99f22      mov   eax, dword [eax]
       ||   0x00c99f24      mov   dword [ecx+edi*1+0x04], eax
       `--> 0x00c99f28      mov   eax, dword [ebp-0xc0]
        |   0x00c99f2e      inc   edx
        |   0x00c99f2f      add   edi, 0x14                            ; 20
0x01d868b0  0x01d86470 0x02021460 0x0198e3a8 0x01d86488  pd..`........d..
0x01d868c0  0x0202143c 0x0198e3b4 0x01d865b8 0x02021438  <........e..8...
        :   0x00b2e1f7      mov   ecx, dword [edi+0x10]
        :   0x00b2e1fa      mov   dword [ebp-0x2c], ecx
        :   0x00b2e1fd      cmp   ecx, dword [edi+0x04]
       ,==< 0x00b2e200      jnz   0xb2e20c
       |:   0x00b2e202      mov   ecx, edi
       |:   0x00b2e204      call  0x523b20
       |:   0x00b2e209      mov   ecx, dword [ebp-0x2c]
       `--> 0x00b2e20c      mov   eax, dword [edi+0x0c]
        :   0x00b2e20f      push  dword [ebp+0x08]
        :   0x00b2e212      mov   dword [eax+ecx*4], esi
        :   0x00b2e215      lea   eax, dword [ecx+0x01]
        :   0x00b2e218      mov   ecx, esi
        :   0x00b2e21a      mov   dword [edi+0x10], eax
        :   0x00b2e21d      call  0x510980
        :   0x00b2e222      mov   edx, dword [ebp-0x18]
        :   0x00b2e225      inc   ebx
        :   0x00b2e226      mov   eax, dword [ebp-0x34]
        :   0x00b2e229      add   edx, 0x14                            ; 20
        :   0x00b2e22c      mov   dword [ebp-0x18], edx
        :   0x00b2e22f      cmp   ebx, dword [ebp-0x30]
        `=< 0x00b2e232      jnz   0xb2e120
            0x00b2e238      mov   eax, dword [ebp+0x08]
            0x00b2e23b      mov   ecx, dword [ebp-0x0c]
            0x00b2e23e      mov   dword fs:[0x0], ecx
            0x00b2e245      pop   ecx
            0x00b2e246      pop   edi
            0x00b2e247      pop   esi
            0x00b2e248      pop   ebx
            0x00b2e249      mov   esp, ebp
            0x00b2e24b      pop   ebp
            0x00b2e24c      ret
            0x00b2e24d      mov   eax, esi
            0x00b2e24f      mov   ecx, dword [ebp-0x0c]
            0x00b2e252      mov   dword fs:[0x0], ecx
            0x00b2e259      pop   ecx
            0x00b2e25a      pop   edi
            0x00b2e25b      pop   esi
            0x00b2e25c      pop   ebx
            0x00b2e25d      mov   esp, ebp
            0x00b2e25f      pop   ebp
            0x00b2e260      ret
            0x00b2e261      int3
            0x00b2e262      int3
            0x00b2e263      int3
            0x00b2e264      int3
            0x00b2e265      int3
            0x00b2e266      int3
            0x00b2e267      int3
            0x00b2e268      int3
            0x00b2e269      int3
            0x00b2e26a      int3
            0x00b2e26b      int3
            0x00b2e26c      int3
            0x00b2e26d      int3
            0x00b2e26e      int3
            0x00b2e26f      int3
            0x00b2e270      push  ebp
            0x00b2e271      mov   ebp, esp
            0x00b2e273      push  0xffffffff                           ; 255
            0x00b2e275      push  0x1869249
            0x00b2e27a      mov   eax, dword fs:[0x0]
            0x00b2e280      push  eax
            0x00b2e281      sub   esp, 0x08
            0x00b2e284      push  ebx
            0x00b2e285      push  esi
            0x00b2e286      push  edi
            0x00b2e287      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2e28c      xor   eax, ebp
            0x00b2e28e      push  eax
            0x00b2e28f      lea   eax, dword [ebp-0x0c]
            0x00b2e292      mov   dword fs:[0x0], eax
            0x00b2e298      mov   dword [ebp-0x10], 0x00
            0x00b2e29f      mov   ebx, dword [ebp+0x08]
            0x00b2e2a2      mov   dword [ebx], 0x00
            0x00b2e2a8      mov   dword [ebx+0x08], 0x00
            0x00b2e2af      mov   dword [ebx+0x0c], 0x00
            0x00b2e2b6      mov   edi, dword [ebp+0x14]
            0x00b2e2b9      mov   ecx, ebx
            0x00b2e2bb      mov   dword [ebp-0x04], 0x00
            0x00b2e2c2      mov   dword [ebp-0x10], 0x01
            0x00b2e2c9      push  dword [edi+0x0c]
            0x00b2e2cc      call  0x9a15c0
            0x00b2e2d1      mov   esi, dword [edi+0x08]
            0x00b2e2d4      mov   eax, dword [edi+0x0c]
            0x00b2e2d7      lea   edi, dword [esi+eax*4]
            0x00b2e2da      cmp   esi, edi
        ,=< 0x00b2e2dc      jz    0xb2e312
        |   0x00b2e2de      nop
       .--> 0x00b2e2e0      lea   eax, dword [ebp+0x17]
       :|   0x00b2e2e3      push  eax
       :|   0x00b2e2e4      push  dword [esi]
       :|   0x00b2e2e6      lea   ecx, dword [ebp-0x14]
       :|   0x00b2e2e9      call  0x4f7950
       :|   0x00b2e2ee      mov   ecx, dword [ebp+0x10]
       :|   0x00b2e2f1      lea   eax, dword [ebp-0x14]
       :|   0x00b2e2f4      push  eax
       :|   0x00b2e2f5      call  0xae5690
       :|   0x00b2e2fa      mov   edx, dword [ebx+0x0c]
       :|   0x00b2e2fd      add   esi, 0x04
       :|   0x00b2e300      mov   ecx, dword [eax]
       :|   0x00b2e302      mov   eax, dword [ebx+0x08]
       :|   0x00b2e305      mov   dword [eax+edx*4], ecx
       :|   0x00b2e308      lea   ecx, dword [edx+0x01]
       :|   0x00b2e30b      mov   dword [ebx+0x0c], ecx
       :|   0x00b2e30e      cmp   esi, edi
       `==< 0x00b2e310      jnz   0xb2e2e0
        `-> 0x00b2e312      mov   eax, ebx
            0x00b2e314      mov   ecx, dword [ebp-0x0c]
            0x00b2e317      mov   dword fs:[0x0], ecx
            0x00b2e31e      pop   ecx
            0x00b2e31f      pop   edi
            0x00b2e320      pop   esi
            0x00b2e321      pop   ebx
            0x00b2e322      mov   esp, ebp
            0x00b2e324      pop   ebp
            0x00b2e325      ret
            0x00b2e326      int3
            0x00b2e327      int3
            0x00b2e328      int3
            0x00b2e329      int3
            0x00b2e32a      int3
            0x00b2e32b      int3
            0x00b2e32c      int3
            0x00b2e32d      int3
            0x00b2e32e      int3
            0x00b2e32f      int3
            0x00b2e330      push  ebp
            0x00b2e331      mov   ebp, esp
            0x00b2e333      push  0xffffffff                           ; 255
            0x00b2e335      push  0x1869289
            0x00b2e33a      mov   eax, dword fs:[0x0]
            0x00b2e340      push  eax
            0x00b2e341      sub   esp, 0x70
            0x00b2e344      push  ebx
            0x00b2e345      push  esi
            0x00b2e346      push  edi
            0x00b2e347      mov   eax, dword [0x1dd2708]               ; [0x1dd2708:4]=0xbb40e64e ; "N\xe6@\xbbu\x98"
            0x00b2e34c      xor   eax, ebp
            0x00b2e34e      push  eax
            0x00b2e34f      lea   eax, dword [ebp-0x0c]
            0x00b2e352      invalid
            0x00b2e353      invalid
            0x00b2e354      add   byte [eax], al
            0x00b2e356      invalid
