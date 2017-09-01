1. network coding paper which proposed regenerate coding
2. the classic MBR, MSR, rowwise-mds regenerating code designs
   the simple regenerating code designs
3. the papers about regenerate codign implementtation
4. the wiki site and the offline version
5. the coding python implementation
6. how I find solution coding matrix, the technique I used on overlap parities righttwo.

-----
[potential issues for real production use]

1. is bandwidth already cheap enough, so reducing it is of no much use?
2. is network already fast enought, so smaller bandwidth won't make recovery faster much?
3. how much traffic is due to repair/reconstruct read, so how much portition can regenerating code reduce?
4. how many case is node down <= 2, how many case is not. so mow much portition can regenerating code recovery take place?
5. will other implementation improves outperform regenerating code? e.g. inline EC will reduce even more bandwidth traffic?
6. the computational overhead, compared to the optimized implementation of plain EC.

n. brought a new technology -> design the complete solution -> data driven proven it on production env, brings more advantage than overhead, outperforms other alternative approaches. these gaps involves great work and knowledge.

