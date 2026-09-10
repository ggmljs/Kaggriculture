"""Kaggriculture V10: fail-closed opening recovery over the V9 controller.

The deterministic policy keeps V9 by default.  At the first safe route
divergence it may select the frozen V5 low/high controller from one complete,
seat-relative public opening signature; malformed or partial observations
always keep V9.  All V9 execution controls remain active, including same-turn
terminal liquidation and retry-safe per-seat action caching.  See
THIRD_PARTY_NOTICES.md for provenance and modifications.
"""
import base64
import copy
import json
import math
import zlib
from collections import Counter


_ACTIONS_10C4S_3Q = json.loads(zlib.decompress(base64.b85decode('c-rk<U2j`ia{MoP)`Lk=UwPBm+}K#n$dK(2n}IMGAR7b-HV>1$1^eIQSR#3OPjz)wpF`SS_{juC-+R7KcXf63um5}Y@4x@?x4-^z_D{c_{q*VG{hQz3-+lP_>2ZDbbbj_9zyH_2{rBg;eE#^i-~af}zy8nX&%d6%efQ<B+J~P${pGj2U*7$EcYk(%_WEIScD`)B{_u9aen0uchxPi+=dU+!*LNS!&aY=*|Gd6`_~q<;vHSV^$A>qcUVq&GkE^Grzn@P#_Ws@LKYx0^f74>pw_ndT>kl8lwDp&V$B%EneA<0A`*1iAAJ+Hx`?p@q-@1L=<W-;{)7S1l&8Gr2VD`Fj_FxZpE%`Dhi-W$t{EEEm{r%nRbu^x+KimHR-ZpDDdF#u6nT}`EjxXQ+vR@1beSMj!;AiOwukYsX-!G55kL$<zBAS19xO(8yUCtNLhlfw|Mbs|NKmGsCIQVAPJ2sW=;2aL{Y?Su>dwut^G`Bx`-kFoGTXVS|uJ)zdQJDTJoi4Ed(By!f(5ztcmY1;yV>TI%X2#mz=ri^*?sVu5o;%-p`yp(nDOi^a;cx?+Av{|7*>cbYZDi4*lTY5ZrTSRP-{kWMhVbQt0dthin?8uUckDiVK6^i)58lA-$GzvlFTbRdKKA)^!iRKV`+p~I8v5My!&i9h>{hu5tjXjsH7<}bPo1Bw&h|Zd3+DC+`DtTDjA_B^hx_~W>yN+vY5n-|-Tk|NJv<Wz4PN;r#u6#N<4AL`y|pLp3HQ*>5t;osxXLe|3=8m^UjN4Y&ilBkd$+0m*J+ag^R6);Cq_6}xD`JG7$a~`;9k8fZOcsNeVFz(>ti~Az_B+BQs%0_PuT<6SfEeo1DQu4+K(OnXx!wY0~HUdWcw-`i2COF{1Z>7&-GP+r}S~qTQ-~rVBGH?*&2iS=5K)$Vq50zvmTe4ssuMXv0?q=Y2%+J-}}IZT44Zt(Pb1MAXzju*u~a&#W6G|xSdn$pl}UlhCnA&CtVCf3<QKThL=Y1Ze-y4{<!WN74S0W(bQM~Z;9qVy%97UqGX<s;o(+W{%8tN131kB013`TM`XwW4Oi*VlYfq-{o^2KKOXzzu_h)JTQ7F39t6{asC;5+T~^M_iZ5=0BSn|b07Lqshnd|~F;F~6$!R|ciT8S;>`o8H=I!0%zeFAD1&k)$(OrEp1dWDj*O%fDO~;~#AJ7g?8$jGK0lH8SKIprSJ-^j-W`I4i8<got<yZy)M-G<VevNJiWgo7T2YvrUbg4|=H@B~>=<t?cL2oYbhDvz2eQ?Wh`e7jacx*4ibLrSfmtXe$0gdlQ2Yo^#>cv$0@bU3(^V9nA@h^ZKD8-G~B^EXuynXT11BK)<ro)yD2`+8)BiT2i^!QmiZiZnvhp+k}B_oQ#f=-)b8BJ4rV+v7um=O<Vb*+!xhutNeKTd;Tw|DGh8)7c%z{q2lzcC+y;wp&xZGHXR%&LutK0P<I67g*BEy6z&sMF5lDmdTK*l|DNOkXQ%b!FQ$C$dyx^q}2oFR%K%5g#8=x`YX|EB-NczcYNLa<4D|VsZ;^9v<$$q^Uq7>gA6wGxYg@d?Q2x_rAClt}D}r&f%ms+%iT^7{nHt4{CG)$VTjTa^xYeL1)0w0a-tzZ~4(NFp~IExojm=s4IY~J05*Zqc-lF0#_24+I%X*kLyBM5i}8?nEOu^unvKK6aEpf7`wNEF#_$JqZ4g@HdOWk8*B8*92s!_w8-u}_FUsp0oP(?r5?)|x~k-$+CejjxWKU4DmSiRj;L*M9fwks*-ZQ8(olAGz3~nMl;P<{#%jFEc4j~bC^aX8uQPLv!vyLH0=)A)?f1N#5iO_dl3c`$o-)gM^(;k{2Ta#HPwSO21p$8DMWbMQT4O?m9j&{3AIG!UQ>Jy=zPCL##JT7TwOi&kZXLVlbz?ESZi9vxw=&p-?GZrkebA!W--;Qo%qB=blpI9R->_4~4wE^qbkjHL$aGH+J!Gm=j$MG>X0{u%F?X*?0ZWhW*ABt%Y@MepoDYgYf^P1`5#(@p?cHF#%a1Lla{#mA*stsf9#>x}rbWhnM?d-Q7JCtv)XbE}*WNhrXO>4%NQR)s&hC#rl)D-$ZntTtIBsOvZ+|O<Q8OVS(P*T6P;4J;--;<irRcZ^9fG5Ae;mJD%s;=o|MSbri`=31mwC=y59<B0rJvuoSmrx*$*=%>D#7BiVFB*M=rc$tw_wGAtu4sGSbn7$C=!x2k15~;j^;fbb828UFh|SU^jxsoSng(WdSv8G&+{a0R|pU`V|kGyqAlNIBKw7nR^(%~t;7drA5;$J9XJ_mcLC9|_5sDnXv<dxE{lka#C}Z9ef4nU)~aR>oa67+5DYM8U>*w}s`=W~lRQQ1*Z~;xyNh6i(jYhxXd{5TEIU(<KC$gd95hK9P_sL=En&=>g+5d<k~i=ESyn^?^d|yfR3M{lHG1wX!)g5g(aZ2R0G;k6&+aIpL<2YDgT9--if(@LJ53Dg82&r3RWkRTP;b4ErtZz>LAu8D(VY4o_r7ryV9pOVNM%P?{$Xz(BXjfHHM~dS+m$q~C*|zVLq^#OFDhVR0q1BP#=~g<mWGE3Yi&jFiPWv1-lvECFVhQo%ub26(asu{CR580-D>G@sN}VRgNnT?fjtE;d<>U>@}8LFRttN8%}~j6mR#=EhX$4^*^-064Jk?LPVi~L-$WG=owOZ6(k!V+@_&J;2f7&lsxxs}SqrUMsst=sgSAfk<J<h$Ew-0{$X)1l4s!hrAxsGwrhSpcv|SZ7yc0AFm~ca0dCJi`S*yO$!5U5m7$amenlDgmm7MS=LkVS<I;ZJ;y>LC@&s4(ob+t4ZjwprgsflNb;sh(}`l(NuSm};D=tm)pf|b!H7g=>BEA&smc9odpFhYu+(XA~2=^Kep9aHf`52hHrA+J&s@Uq;_Vv1MmPlExPzC?`n_GX8vk7iAQVR@xY*%T1IbqOg@EJ<^TX*ijz!~m(+N$lXo**w!Gg8!Vhx266R17)}wP(mye&&peS(*{B=pY&URah&<OZNCANR%-uM2#GEhhH1f8G2=;qdEvQ%a<>e8&J43Rsx1d47e}qHgNG)aqdao4k#IPKTfU9p(k^5Z7niMET;}VM;li_lxJo8>!wwNZkCtcjN;pI`G#T6`<}BjHL6&PerHf8~3HWrVjj6R1)vr`nY_50;lEK(~Y%~KZ?1AJ^olBS`$rix-rezM2BZbw(3{ByDvGw)KLk^1oD{5p1d~!gtz6uT!lDz#ajWQ@<ds$AZ;Ly#tl3)>46t;Zxqf<5ZxdHugav}R#B5)WICBX9(KpciT$cf@j@dwLgmU$T6DI?x<4|G3fp<=yow6fsr@H$vTX(tL1?3P`^n`P}<Pnb`*p>Lil08$G10XLY0ZaFu-i=ly-%Sslv#v_QxV~JV7jA_7El9CAMif>FIbMfeiLSrN&>4+n*j$#-bjJ&yMxC1|a)wD@mY|(g%p4=(O2<iROM*A?8%$s)=N!Y%sE-T`e@dd54j#0FT3SxNlpBKBdiR%<lfD-_4alcFVThbLOUY0F1(0Yo2D1|kuNkSAL1TR(=Q~Mi7x{j<8@mS<Ca_FxEmx@w1m229?U(@@9el=|6&_EwxQi*VEP34ddErsiIeTd-aLvE?znidimBuGm412`R07$ZTL-Ivq$+$5OI@j)4Y&bYbW>$)P*?p{LqF%FYP##T%oM3M+oBg&9KNE?}~sSEj;PyJfWPOgaVv4E9PQDw=ntBPhC<C-vW0s{$@)r)VRDg-Ht#xT<S{3}5T-bgXfsa)LO7$jH?>}WZeNFi!ji>`$uMCXgSy5b}*D~uN^C@AGIR^|-(V`*()HBSh;*0pJ*LCcJEr6|@^y+;;vWnMb-wOnr4@~PsAX`x|33TVVIQg;KC`%C;@r`8a2mQsICLS_{YPsj)t$}Uk5M*L26>4KH0AxgCEb<Z<g<^C38Ep)tmjqZ1p_Lir4)RGknGYN&w1AKzPM~DX@wa@jVpVOMJr$h+qS+5Y$>U(jvPey@gU28~Y)^eCbgrMMd@7=)NpNheC*|w_Su2N1!CY%OfxK5HknBUzd&Yab%h(U?F&<W18s|1ZI|4t&KJ)b^{ke+&DFxfTvl$;KedJk^?fF;kEz7z@ir3HXgkqg>vkE!1NErUahw4H*+BwVA6D`97o^r$mxYW)0@G}VPUbyk%}@f)J2K=aV3#}NOla}v2wDRXfoE^mcKjj#qfCMi{+vnZIdm&B_jOi=1CWUw{Xr_UE6T@mMA(S{vzpD_QP#Uf+66~YH*|IJ4Lv@ma8tQIedsCy#<>6^8xZsLlgR1`WpTLXwzezRKFxL4kUW(;JB93#^jln)bjt5Q-~Yh*1dejE7im#y!<_<FuO&sIP?b)a9qUz$j*EkqT%>X!mPs|_Q<l+`TO-0NExGY85cR%M2|RVFsY5%bs!%pEI_k5a8nFA<U=HFEIzrlx*KovSU$`XJ%))$`E4e3O|NlPb)eer&e-5bHZWEOc>qiA~RPku*-hKy4Kg_RZ$4PfJ7O)E9<abiJwCe#Kh@gAQ*2g|o{#tk!=~Ge|<G$E*Q?7Z~>FqzXKFIvuf~jY6(NP&F1xRww|)BIVTcTEm@8UTjDIE{uS`G3VpPfZ`5>iXJ-NMH_8us7@z?XXm&%Ad1IZ(159Ns|Ry|F9M<c?;>L9xIrfkSfX8#xJ`r7wT}?XluDZAX1huvCLglF7A{Mp)Qi9?27#wKPaEE6m3;b6igCMg4vYOgi(?q$Ke5&|&Tm@z56Qs1GSVq~`QX!e$3{RN6{>iYl1~B_B@3Wo_MPbBrKZfa!?DayD9QJ!lxY_+`kN<%Crtxw)FDi*TVJv4RjJ}VY=xGIE|J3v?e_EqJxfsQW!~rm1+^Far9#&B;<BM%C|-b?zN5zCW-A^x$I7oQEE^IBP6(1(B5NXIAj%~Qo}Z#Cnf(!;`Q*qM+;WZOog6-t7f_d{T$G$|Ev+Mw5AGlgqn=zy1+8phMq=8e;)Y}T(Ov=K)|9X+#_Okn)oORNI6tGq63B&|{lgS#m;FK$a^WN;)rM!h)EDAqJ^kUi#O3~977(X&`0WECj>J(r)>YGSc|&>hQ|Uj@#M^H*7GI;ykBQ3HorE#*_{@*i1LnsG((A<xx>%upd_HZ(VBANU-&SmDkeFj<EFZZ4Y3Rksbk?HuddM5y*z}q$1mIa@yPBJ#6seaY@v2-Ssz4@3g%qMOc){VqkxY%_2+x_)giL9m8}<~$l9m6gEFe}7k~mdKi48|ONr3^VA|!EtDgl1UjJ0DT1<hOy6@wNBWkGjRQMF`pMeK~i!qrf)7A4m-6^7{;Fh;f{(ytNZ(?tf_!6#uY$cDzz^%3JlWJ+D&Emv$TOe3XS4bgHtCign>_f}uexdX)JuSzih<XM?xKrW&YlmZ%u)5W(t$q^Or5Z+q)mpmv};Bd+gWA=B!!N#b6e;)RDiMz~B1qZMk$X6qGaklmCQ^9vl&F9D=$vOs?<lKT)u)vZxOhfG=qh9jHvV~U%-4!?cuzkAs#FIz|&zQ!Jr_o8ZK2T3c+~Km2FcNnOH4(USlf8U!u|x&>50u_LCaOtb0#ytkV6HHbV@O=nIHTEdCQ?Jx$P{{9Pd&lwhC{M2s4z4SBY?vwd7#~jlmDD|@VaZxlBlj!Y9%{>$IRMQHRdj<3L?d9#bLFkN(xzP<PI%WBV2`aZ;d!W>hWssCon7%vkJcOYo{*pRqD`Xoo$|$@myFvf{oJIwR)_OVa)ru>YXNu4??;Zu`TkZUs+==CDK@3=%J={>?0y408|WGxrX)|K%a<j0kLn#gT0okxOOSouisD(&hp!l=qI&lM9nn;(;Jd-V}Ub90GF0}EN0!vY6|E2fA3eDKZUmcMy*pYSV_T3#VMrT%gS=JU!A1@G93o$Z>0cjQuB0Ri2(E|La$0YSrUYtp2)YQQUc7&z$0r+f_U3nIW!`xM6A0xl$x(pCBRu(iFKS$#PqY}+m&h;@Hz@odJwIWuEJW^Mh=a*AP$u4nwAMW!d^yd#dJG83-uV8K?GARq-Q~};Jmxq0^iv<WksF8m}qq@Y(xbPg?g2y=s`!nR`qG5s0Ypcq4_4zwyb4jDBw@)nro$D8R|V)fxpKoZ%=-j0@G3bV0Z@|o(%0ulT2~qnaVptV~RpS&kWY@sRmN*)6kkF-@;a6buVcBO5Rrl3qOm$(T7&f{Pq>ewAx76!5da`MUAhR_OriYzKv=b$R^^%Xq9PoF&qrbC~GoO0Nqa+u?R2#B|F^kfDOl4ruCGFFH2)tS*oUW_F2~9Fu<IjU$@4>tQ5<X=L#9=#u7yn`3ms?3~PY_Y=Ynjt2CZ~ZmxGBY)-O@Sq*woo>GG#%}##dYb=+-EV9$IP}r4I&or<p?`u4H%NkQaVn?dn4{l${oxJK>hm`cCnt)EOp4bbr;Aq_xbvw~#$RL@{wM8dW%9z*OLtkY{Ii#hGx9GTzz#ls7)l;k|!EvLIGu4_VzH=j-vpg4z=+e-ty0lnrVY>nshUS21iHdnyq(1P_O5-bLK9Y%H_uLSwa*{c`wz)&cn~DxNULj;l3r|?5<A7UoJh7FQP{kxNk}Wb*JElNInz%-dLZ?EtWCkc5)p?d$6)CM2PTKAA(z_VM54(63L2*k~tmb>KOfy&&2OE8Qxti4A8^96E@PQO-GJHZqo0-91ltwY6oNISA-CQ-@t5%z~({R;vPSp4uOJI#3dJSfRTS{W&cDlyL(t==iAzDXAyt_sVQe`GQnaGvXI43nx7{CqV;82p*k+oG(hhbO|Lo}m&CXJoy1Dcn{MJ4$p>JFtYwC>?tRgiNh7mzkDQFirPPrxCX01I0|6XzH~M|II&)gU6K7Aq|oye&&m_p;v;qo_NFfOs-lAv|&MRA4r9O^9eaP}C9~V}*1mVBM<+AZ1bnhika6Rp;u`g1j=Vb5RMHk!XtfLvu;hJWDOfNJXEb`@j&GIyH(!urD?XTlULyEN$gXX&ja)${Ww!{8?jlU@$$rp|*3w0=h}rqMiAoI+!CVqPYw-MF65F-|v;!7g0!!(I7*PZp&m1p{{~a(Z|o?O3l+cVUUIL1DjIHg;DKR2wSa=r|orsF_8=q5f>U)7feZ_loh><x)(k5!B9qgw~m)n+^nM{wxWv!7mJ^^s=#M@>Zq1$#?*0J-(;Q02Fr>tg(&30NK}OPjtXlgdb{$vD`cOs6rgC|0?DN{FR~0q2Lcz0t0Jq|u%t%CQazUm3VMm)3W;q|;;_M^BB|Rf*V1MY^Nv9IGMwBSBWrTwiIQc7oQW1!Wi~H`*(6z&Ty%}mOZ54!94yvsTBY#hLY!dRI=V(f9Mx7b?7}F6#wS<Jwa%c7Q;~)l5WytT@P=fkGple{oJK=re3}S}MWhawp+Z1P;y-;Neu*sAb*X5SPy!^c7+>eBMtiYOW6UI5Nwo@w2ryndo6Rfntb7PpI_Xlh>W1#c5UTSe(9XU3Z)tyTjQ(CY)ejXlvTcg3yfN*~cj@WoYvWEMA&U54f$BR#U95%i{&8xiji-qn$VcQvu`t8(<UFxdA>Dz^PD>f9)MWd%d0|J8tN$7tv9vZhx`C*EolF9gND-6;rYZy{EN>e~sHNQME1%L)sN~X^4B`RAu?kXEq`8>{vb8dzLNQs(<68|PkI}EvA$4g>m!l|S0Xl-IgbC-+!ERT5tg(dUlFCm>h2s5i2IG#oiZOlxK3_5Ys-HQQskc*oDV=Czq<mHd-NcIbq;*z>k-=G@n#>s`nT7RVlsa^!#Pyq+t^$WfXCicS){;a25enZOSIJ0WHtk$`(pVN9kZ!P^DOJg80L$Tmg4FJ9f4&_kV8pd`;QJVA8lQ<WD>W@Ux<W&BzR!o><3q1{zCP1R$CE3qUF1~suTV<3*u|Hjl=*l-oD3YVZ7yreOPl6~29(4&`;zIfRl&;3v8=aCh4r@hp4e@mmls{_?`OSnD%p`MSSG|Jm+y9@vXw`pydAHO<=0}ojV)uT39T!hFDERefT3Qo-Bw1qE&0I`WacmwnX0dmfRs~p#0qfDvX#p|a5@AZoiPrJ=q$rE8Dt;mRKWv#u(1l3r7Ao*yN(sT6xnqu38Y7bDB?XV0Z}KPXF>oC=UJ!XI)yF9(0PnqtYi{W2h;vE4qli~^~yko63V1)x){|{x{Glx1jvZ+>{8`QG;2YQ;+U>p13G1q&`jqN%qmU%4iDZw#BW(r#LuX$G3=i_Vy4<&BoL-6vh7hqHxgyOLfQdA<cD4}I=zl&WQ!F`8MHU9gDaVLx2*8))H)+nRhD{Zy@gq8Y)LLf-y&b}`kvr=w)UB|YRiCbPR>hsT?FP-t7)BJME0m)YBcf{sloIHU#{Nm%lbl4dabJ5h=nG=Q@X8;19<Z2#Yk^~b@$D}ohPq5>I;x;1c(h!_4QX!nbUEO-tr4KPhJWzt2bIznoBgSOro7qr&O#Bprl9{;9G?PN$QYht0j%-bJ4EOYNN8{Dv4!Fqen2A*0(iP?pZ+>8aFnaQl$N^-IN-;(pq@Tw@9h84A>L%3-q)=#(flYl8&(KsQM#SCs!pM(sgE*<IF(T3e7GbIjOEDr(ALM^w9H7t-*_O${2`cio6B2>Wf;qrm<Jhww<<ImlWkwk(GgPrPM81HMG@IY+k&!#>MrbhQPoOAwQuhQC#PO5+56MsfFw|Rb<qgCl$ruMrdbgDuQYSpb!tSKsiAaomEdrb510>8CBKtb?lAyGm79^DHgj0+j6d9nTfpgPKI3FRfEWH#JKCYe%XMCRu1zz5F+?)s#3O;wiDH<^kvT!5V@^YdO|*!fT%E|skiLprciTIE%jDldmV-{jz#zq^X59`&!aY}?5%`G((B)~q%4Miuw+5CcmdpesS=At!1C4sIAK(E^$IwD)knPojRb##C!?GutajysL{j?5R#{UG1Tz+NjV4oZD7t7>c}cD`^^6?JBG0irZ)9=GOD)kwQsmG}rBh3)bDks_F}an(s-jw;I(s*jWf^7>si`c*Z6#`tRb#d7GG$uVLER@IJIR)8vCh#})Zlp{(1LBJ2%I?Wk5J~}#LVy2BYS?-Wu0V0(g~UDK1s)tHf>##XVtZ3DSXrJRjsZFq2qMdseYc|g*?HX_#8W~*kAyB2O$p6&Y%n{EX~baryybUEfMdZj2BC%>@9VA9%qRSC)QCeV7$XwDyBlwo_6dyBEKxXop0r2E=psh#J<?yc;wqyB(IL5ZpidAeO(_rUa}go`v*gi(_Ob+Qqj8n&QefcZW^=c9r+<FU2~ec0KZJ?Ff8)NDhhE0x<UIP&F=&RHdZi2k2SLoRY5nI!d76H6gguhvRogTu0~(b`D2;Vx?12M2a$o63YcRa#?%G3W1)YBWiEP-nY7|haSAkYn;IId!6_(DR?z#ifP78xB~2K-H8?V9j#!#brsTP>eq4u@lk`K(V7{o@x0!7?P)%Pgb)X^rc8q^j%A{dj$q9Xdh~EhVQ432{t#S3FM+CEVtd^$$-C;_e=0Nl070SnhK1JHl3zN0Zpl2l=QiVLF^TyGE$^`aI$F$XOo1hnZ(cJQ)hts50c2MrCUd5*iC%3Cx#LZ4^^k$Zla-GnLR2YJ!BPW_8oL)+acHLQRdV1r^61L}aK*^g_F(cl;gW*Me6^m2F;UqFLC8}qOr5|SR4d3Qq{R2TazSJWfO1ciZvm2E&td`t(8Ns{Y0$C!s?czJc)(+O$1zwV;QGAm!Zgj#QY><LTr2=R)(<Q}EpsOl+M+~X7lzS}YHzHu`mS$yg_GaD4zOoK{Q$z;~L!_{LTY}V-7&N^CbwjH8wdtL1V3uc0v3nv9xhxD^K~D~JV8ujF+vQBQ44Iq$gs+4UEZRpRL)fUtw<tlU)UcyjFVmLKXa?S#ET1X~gL!!X8JqKjzw>>xbc&a1DMm8?PmDI3wxL!Vh9-ka2bTwAT^p7Y%z`JlVKS(#fTh(?!j1=m3j_(I!gTXWELIb>VgtJ3owG-CBjY+H`UTf%qANzlWfGls1rv8maVo$P5sCEkxH-%=;w(`?Buda^U}Aib7Md@Rt-zWfoXMs-BRo^$li%7EWcg&m5*{##xE~>3u$FQ*PM?hFZsf(V)M_c4>h0?k1Z~NDo0?9Nx6F=;D8+JFOKi_)pv;gu0_`LmHG{ODv9;{WB#rEAQK-L$bjZ9Wu%?+oN)ZJCRJt%!OuJRRima(2RRvTaPFE*mj&Lo1lvm~xm0~yvM%z%D%tDG3X81=EdN%6QZQ>Hjd9_}#WSgE5m##H-JZ%WsG9RRNbx~KFYIn7a4W1TIOi0&N#xs?tN~K|y9xf_dLB$cPLAigf7v!WH&{KKi^<J!?0rLwi{GFP>+^Kgf;0kV{#ulj+*<mG4jO4ATrC`1_BRff)j5m$dJa!#zjJ+ZjP#rUVi9niE0650t{WfCm5+)iW!p5xl8Z68<tMk@5$$N*pdC>vUsHG>g|6%^O-Z&q7SI>w3DIMFMF>^_M?rT~qZ|Wwa`X?>zqED45VPf*z54l}+x(7uyglN2y+L9ErOmC~O+@A9CWUMJ+G|`#QUd^tQB>t4KTXRJoYPV#Hh@8fr8l1UNBFbgzx)15l!(&}cIZf(<>hA^@TtIA9>X8a$E^<e)J9cny@sN|(R*n?%I6ksQXE)AG2(%poW5xp{lsA!ARvg&&O;VM$-kuU|N>aF{tEV6wl}MHPbxA=_>EWjo={ap*bxK};U*lGi*S>jtcz^iTmv1H?cwfQKp1)%0;s%Fa&`)Z2UE7J>hux27-=y(D(6+;nVPgbu4d|!8Km8w;Fh$h')).decode('utf-8'))
_ACTIONS_8C6S_3Q = json.loads(zlib.decompress(base64.b85decode('c-rk<U2j`ia{MoP)`Lk=UwPBm+}K#n$dK(2n}IMGAR7b-HV>1$1^eIQSR#3OPjz)wpF`SS_{juC-+R7KcXf63um5}Y@4x@?x4-^z_D{c_{q*VG{hQz3-+lP_>2ZDbbbj_9zyH_2{rBg;eE#^i-~af}zy8nX&%d6%efQ<B+J~P${pGj2U*7$EcYk(%_WEIScD`)B{_u9aen0uchxPi+=dU+!*LNS!&aY=*|Gd6`_~q<;vHSV^$A>qcUVq&GkE^Grzn@P#_Ws@LKYx0^f74>pw_ndT>kl8lwDp&V$B%EneA<0A`*1iAAJ+Hx`?p@q-@1L=<W-;{)7S1l&8Gr2VD`Fj_FxZpE%`Dhi-W$t{EEEm{r%nRbu^x+KimHR-ZpDDdF#u6nT}`EjxXQ+vR@1beSMj!;AiOwukYsX-!G55kL$<zBAS19xO(8yUCtNLhlfw|Mbs|NKmGsCIQVAPJ2sW=;2aL{Y?Su>dwut^G`Bx`-kFoGTXVS|uJ)zdQJDTJoi4Ed(By!f(5ztcmY1;yV>TI%X2#mz=ri^*?sVu5o;%-p`yp(nDOi^a;cx?+Av{|7*>cbYZDi4*lTY5ZrTSRP-{kWMhVbQt0dthin?8uUckDiVK6^i)58lA-$GzvlFTbRdKKA)^!iRKV`+p~I8v5My!&i9h>{hu5tjXjsH7<}bPo1Bw&h|Zd3+DC+`DtTDjA_B^hx_~W>yN+vY5n-|-Tk|NJv<Wz4PN;r#u6#N<4AL`y|pLp3HQ*>5t;osxXLe|3=8m^UjN4Y&ilBkd$+0m*J+ag^R6);Cq_6}xD`JG7$a~`;9k8fZOcsNeVFz(>ti~Az_B+BQs%0_PuT<6SfEeo1DQu4+K(OnXx!wY0~HUdWcw-`i2COF{1Z>7&-GP+r}S~qTQ-~rVBGH?*&2iS=5K)$Vq50zvmTe4ssuMXv0?q=Y2%+J-}}IZT44Zt(Pb1MAXzju*u~a&#W6G|xSdn$pl}UlhCnA&CtVCf3<QKThL=Y1Ze-y4{<!WN74S0W(bQM~Z;9qVy%97UqGX<s;o(+W{%8tN131kB013`TM`XwW4Oi*VlYfq-{o^2KKOXzzu_h)JTQ7F39t6{asC;5+T~^M_iZ5=0BSn|b07Lqshnd|~F;F~6$!R|ciT8S;>`o8H=I!0%zeFAD1&k)$(OrEp1dWDj*O%fDO~;~#AJ7g?8$jGK0lH8SKIprSJ-^j-W`I4i8<got<yZy)M-G<VevNJiWgo7T2YvrUbg4|=H@B~>=<t?cL2oYbhDvz2eQ?Wh`e7jacx*4ibLrSfmtXe$0gdlQ2Yo^#>cv$0@bU3(^V9nA@h^ZKD8-G~B^EXuynXT11BK)<ro)yD2`+8)BiT2i^!QmiZiZnvhp+k}B_oQ#f=-)b8BJ4rV+v7um=O<Vb*+!xhutNeKTd;Tw|DGh8)7c%z{q2lzcC+y;wp&xZGHXR%&LutK0P<I67g*BEy6z&sMF5lDmdTK*l|DNOkXQ%b!FQ$C$dyx^q}2oFR%K%5g#8=x`YX|EB-NczcYNLa<4D|VsZ;^9v<$$q^Uq7>gA6wGxYg@d?Q2x_rAClt}D}r&f%ms+%iT^7{nHt4{CG)$VTjTa^xYeL1)0w0a-tzZ~4(NFp~IExojm=s4IY~J05*Zqc-lF0#_24+I%X*kLyBM5i}8?nEOu^unvKK6aEpf7`wNEF#_$JqZ4g@HdOWk8*B8*92s!_w8-u}_FUsp0oP(?r5?)|x~k-$+CejjxWKU4DmSiRj;L*M9fwks*-ZQ8(olAGz3~nMl;P<{#%jFEc4j~bC^aX8uQPLv!vyLH0=)A)?f1N#5iO_dl3c`$o-)gM^(;k{2Ta#HPwSO21p$8DMWbMQT4O?m9j&{3AIG!UQ>Jy=zPCL##JT7TwOi&kZXLVlbz?ESZi9vxw=&p-?GZrkebA!W--;Qo%qB=blpI9R->_4~4wE^qbkjHL$aGH+J!Gm=j$MG>X0{u%F?X*?0ZWhW*ABt%Y@MepoDYgYf^P1`5#(@p?cHF#%a1Lla{#mA*stsf9#>x}rbWhnM?d-Q7JCtv)XbE}*WNhrXO>4%NQR)s&hC#rl)D-$ZntTtIBsOvZ+|O<Q8OVS(P*T6P;4J;--;<irRcZ^9fG5Ae;mJD%s;=o|MSbri`=31mwC=y59<B0rJvuoSmrx*$*=%>D#7BiVFB*M=rc$tw_wGAtu4sGSbn7$C=!x2k15~;j^;fbb828UFh|SU^jxsoSng(WdSv8G&+{a0R|pU`V|kGyqAlNIBKw7nR^(%~t;7drA5;$J9XJ_mcLC9|_5sDnXv<dxE{lka#C}Z9ef4nU)~aR>oa67+5DYM8U>*w}s`=W~lRQQ1*Z~;xyNh6i(jYhxXd{5TEIU(<KC$gd95hK9P_sL=En&=>g+5d<k~i=ESyn^?^d|yfR3M{lHG1wX!)g5g(aZ2R0G;k6&+aIpL<2YDgT9--if(@LJ53Dg82&r3RWkRTP;b4ErtZz>LAu8D(VY4o_r7ryV9pOVNM%P?{$Xz(BXjfHHM~dS+m$q~C*|zVLq^#OFDhVR0q1BP#=~g<mWGE3Yi&jFiPWv1-lvECFVhQo%ub26(asu{CR580-D>G@sN}VRgNnT?fjtE;d<>U>@}8LFRttN8%}~j6mR#=EhX$4^*^-064Jk?LPVi~L-$WG=owOZ6(k!V+@_&J;2f7&lsxxs}SqrUMsst=sgSAfk<J<h$Ew-0{$X)1l4s!hrAxsGwrhSpcv|SZ7yc0AFm~ca0dCJi`S*yO$!5U5m7$amenlDgmm7MS=LkVS<I;ZJ;y>LC@&s4(ob+t4ZjwprgsflNb;sh(}`l(NuSm};D=tm)pf|b!H7g=>BEA&smc9odpFhYu+(XA~2=^Kep9aHf`52hHrA+J&s@Uq;_Vv1MmPlExPzC?`n_GX8vk7iAQVR@xY*%T1IbqOg@EJ<^TX*ijz!~m(+N$lXo**w!Gg8!Vhx266R17)}wP(mye&&peS(*{B=pY&URah&<OZNCANR%-uM2#GEhhH1f8G2=;qdEvQ%a<>e8&J43Rsx1d47e}qHgNG)aqdao4k#IPKTfU9p(k^5Z7niMET;}VM;li_lxJo8>!wwNZkCtcjN;pI`G#T6`<}BjHL6&PerHf8~3HWrVjj6R1)vr`nY_50;lEK(~Y%~KZ?1AJ^olBS`$rix-rezM2BZbw(3{ByDvGw)KLk^1oD{5p1d~!gtz6uT!S}FKh9A!|-_OhH-!NHqvCB-7DDQtP?M<;9SvjZsMU5u3r8Q2nu!;mQf-lqWMFyui_7N3q(MZQR8V{|8uc+Wjh|7dvfdI4!=+1X)su#nPj6e8Iz%Y-+}+Pj`WpKw#(JXL_C6#4`1FbUyuj(QhU12LGDY;KKD5Ru3d^MD!EfVU(i6VMgkm_+8{(UFD5SU$KEPPIOY0dX+)=Ca|g{P=a#rgO1n<7s<x_aLLD_lq3u16DGF-qj{yJFB{^h=ax#w9-08)*^a{;o*N??9wK#SU{mp0L8`qF5PfRSE!6xw$MQ9DH@`b*r=upQK%5SSXoT%ZyXUjvP#5bkqgS9zYbg~N(EJ}ZWn(|?-Tmfu$4nYet=UY0<$%}Lprn+xX+a$f}an$rG~3pNU)F~F5M61bckY%1Y>qzPTO;nU^mAHX8=m$W__>g+C;m131!MSoEjNnF&Pm_N=%J1LqZ~LjIyRP<mW*3t2R4XBf7@|Rz^jiB}1?(>S>I1!ej~zJW$p#zJ01tr6?Z5==1Zh1WkA&*+3_CaerfwbTzP}<+LJ&vSls07LX8~FXrlslenyKU#PU8l+jq3Gvtq@ResfsA?#Y$rjdp(Gy0XHT~qZQS@e~8>CD%1Sz^nliYulCi3L%h5yME`4N&+m@q3-BL(Ex9{W%GnRXjW)H(V&dL_rwwJJF>JR-%R|(YDt;&v2FdTZpyL@$xm|-%;9Ip5{?YRw&UVlsFIY2?ie_MugNp*N=WqaK4^WBB*D*LX@lT#o0a?6{2;mA+1@<W)2a8g4?}!19yKa2H0iWs)D;p*%6t98i3(C>Hc7TcbhnKR;zLbCH_JuIMc2YG^+eNiI(<!`Yb}C>W#r^*MwAZQcUVSxS0f&P-FU1B<+`$0#fBJXtO=edi%Ew4lxpV3Tl&ZjWV``ombMM)2Qk4^H0)L7v|JiRUXxEh_V9BNTVJ@{IkwU<dUV##gSOO6+$(_8t9m$RE5s+V9H(+ua+=XslTMb)>xlDUx;)??0ZEecF29g{CgIQj0sl=ADI0&9|6$9ym{GLyeOjXjR>S~)~e2lE0a>u>g;R{AX@p&YF*=Ap%a=rkfn5tOmI*>O!%!zab>NMwW#=Q;JaV8zWd_q`R+Vx0qxX*e))cBBHgwSRp_c@3jC}#j0lrgvsiPlZ(YnED2G^;8S2)X*c3<1V=pjwtUNwS-7>vcNQ%_R!RMQr4kC4~wlwR5)W=uPL;LbgW@1e0F?ag0+3G{A@A$CLW!@z|J<CYaI0XY$R!G=4o3}ny4Utn{7;@3|rn>tTZw(AOyag1_F6*#b2}aE!37sCZ8U$Wo*rStb@#IN$#DX?Tx(-3rSSVSc02IrWQ_pJ+cQSdg9sRp70{+IFj~fGuI}j>*=y(@xw5g#woeZ9x<K}=U9&bSnrpB!v%muy(B=^6Ih^6BOoit#Hc17Yg4NBWSLM&4%ZkC(vDv6kU$Oc=uERCWs0<RbZp6Wbpc%N0W>N_dM?aDbU`}Zu9VT}L8TGu$gX$?Rm2=mHFr|ji}Pv;#Q0eMuY;!#RI30RaYfQH$3qKlWBGS?2rGC!dt-=|WrUBu{bo(!He4YW~*Ftu)d?J{9|B(9cLltHW$FH4oZ>Qfr@EJ3Z8d7}@s)L!tH3R&BW%Z7fTcmZlkj~a`ct$5fRE5Ej|Y)Bk9AxLV8tci$$D4ZyGeu~0m_D6i?lOtzv%QcpFa`;eQKwYSEQF6Yuw2nkbxPvf^dU7F^wz4G}iD{F{9FFNndj*JFQ^Kkkub&21tKHG!{EQAuAQy7>57VYy_6tqOC6ts@8=mn}Ux=6W^oQqSm-~NNK%COyw-1Oo5=ZS=S9Qnb4du~KB>+JaZ@<-8e2q3gCMsWd62`>iGe24nm>(xdua`CGVukwg`Lq>-aUW%VTd}D@l8&9ReBl14p%)|5S&P!^A#ZeJ(`&X6fM=2IYHo^Bu3n17tAdTF7MUCsQi#Uj1&0eqGBu7PJZFj%GNplT*i(>AR{pcHfLLWn;#4KYHXP|B1qPs+ki`9|1o$O0){co3lyfyy3|btN1>H$S)so2-u`>z_S3|*Clw8wP7^Y*u7}=6szebQx7a3>=pM<p_8yZK~M~oAZDRqIjT(Pk*jg)dVM9b}%-0R5STYWv}4iKBaD#ZYhXJw87xrjzk3TPZom*4IrM^wB+cx&lj@}OLS!znwA+1~{R8>9aHdD!D6?lL<S9KdoQUya<w+19sD1>ZF_pCgAP>lj>;a|>3%0!!X74YiAmddVBh7G526SKREw_UYaePa+*WV;Vc2Mkm!uK|LXHhs#33NZcjVMBvIz_VU5SA{FRAP<r>6s3w64R55^nxxzq>A#qLPjAqA~NDWaVQ|NI$l?AUG4#~ox!q7a701l(%fp#lS{&U{J>#jLVqPkMCmFxf>Giz7Xn7gDZh!nFGht--YDP*mYJG4}da23+MHR1rN$E&%Yz_3irDtIoYGI5EoQim?<Z1c2?=fdg{Y?RKf)nkPWW8TMA?=(q#5YoMfZIL(q${KSik;dvm4>hf09}zhLpkmO<HMHLV`b2ySh<!UA?6q9QRZPi#{f2UImfwy<KdDV4YOV>G-jIYF3!E_mxU}SBG3!QFQ#jZEd%xQJDYX4JYMp|?N(xpgP9gPPR+gjv>MRA2=`c`#D+Oqi+NT3c1fWk5dR5xVk|5;tM7}MR5@22i9$8}&#M{=&p%GanV&%=D)O@8X0nW-wtmAwlrk^d}u2j2#*HMttgJ`{U71p{oa%jW_aiCn+v`p9$_A*jyr`zdSsK>|*BA99+Jqv;b=iSv7_|C>DE9(5kM5|+ABPwtx)T=Z_4?6m_s!t<DJ!tL^%{PIzWi2B^0e@Q8Tq_OBQ18JC{5?*2d-Bs1n2zcP!#n8kWN25KWQr5dRNfI9Qxpn%X0U!wHIQnbhSn_k7Pb<rdqL}0^1dQi_*wjoKD2V?x35U1)keY&-msD@YJA1CpZyi{ZB)xZHW4RAt4ynl;b2%sS(A|h=zhwGMSuY)+2Mu<Y&gy`t*1nMSsKgAQZ=o!&$14O0p|Stx-}MNrC6psSI9^=mMEIYSBMW_SPKkb69h+CrSSxGbG-{;bCOleYS4@Flo|wScJd2fW4RP&k)5W6!mgZprh!d)U*pMJ)|dhkJ5uF-aQjN`<W=7~q@*v^1axxs#9ojEN9(4j+lf9y2FY};EjpP}#=Pbp`YKDxAuVORMaOjn{?K8so?<--jvIxXsn#^{og3kt<+)fymxfl=rNwFs+ZDJlGzUaWRLsjF^?`?08ecK<kxUG`=Y~*~lg#0@%^f=4RCK`c3L#rsc)~gz2i%h5iLJDRDkhPUY>}DTF$F5p#5HOZIu)uVGeGI6&a>32NNKfj(r%ZR-o+q(*u|>|id(W`HQ#$>n!&0#*yz*C)uaaB0FGFO52RR=;S(C#%nbgbG>ReRT)V63=Bnvlwc50uhO4G?qQ>V~0&D!xYcLbsQW7J#(=|Sp76h{k(K<Tf-8EW}Dl_59M6R61IjM=l0B#ruhmy38tgVVV48w{Tq8a5gY3x)V(7ZG*D#<5NcPMqCbr0vNf}A_KfV6puva8>E0uIpxSl9}hIL8P&s*Coj1`#o}SZT@NZCQf4m;Ig?Mcp|B#FNPi;faf<0<)QGLPXnvqL%0wE2KjK>s~zoDU%{NT*G~>I#-t#<dtcii%P(ZL{rQknoFwYS!zi}D*6=N2Zq4ZsZk_?eX&{CvR|HKX)9++<FG_g-gxfj&l;-(gX!T7wVfLl&`rt~?aUX|!5m2u&1Ik|0uVj<ey_y7h(c<N1{rd6TPAA=brp<?K7JNgYM#~!gDjLE*pyN(jB2++*lKk=ZLb52iDZC?xX`$|U`i6DtmtLbz38bAhBD&2b-bM7W*sH56<s8_Sp2kA1wPYLN3~otrjFbCChJ5tSXP87L?IVOq9VL^R9G|7+m+W{A^VJ_07d&2NG`2;k!3JC5V%lW6<NiGB{eFR>bXo%&`ShYNNkG|hYcPTN!@0-mNtu+cLd6p;pE;JS(6)2lq@UcOtiQvvw11ZCdsPgqHBy^qR)5bV6kS?DupK(;so2)(KQ<4sJ4<}7e*O0KDlbHbp~aeiZslC2quY!HzYfqS%tgeG#Vn~(?m!tB6YY76#`Nc|LGI)OJu38OGTrE5+HfS_&Q%T+KYV}V<y>3s#P#VfbrVdY+i|H<wLmANtdEkH*_zCP@N}%cJ9@GOZ$6c^!LK4eyFICZBuOJjcISbOHVgn8+RHBQN;fWRNoQmVl9mKk5e;kJWcFCJ|ZWIg&CG7=ZU2X=?-jmTFO|ZCfm2o3p;{b{ny}#rM1b?4Mg?pWD=M}il8hoRUtTGdD}ojE#+2U`IL@AC6~rz5Dy@ZRgkJ8&CMi`t(6fKipg3Y-)azfjDD34sY_eB97P!m&=E`}OgM)QcDw3hjU_CXRDMb-6z_*K7<bH7jPVQb`HJaR{mijUy`Aby=|meN<+Cd2CRV&Bt+OhO49)`8WX>qbEUf>c)S)XSuHV#j6*x3H6QP^4mK^$zQ26e+N=6E^Y3I_D#<J*ubc6LwsY+G@SPmByq;_xn^X)(ZBd)Cj-^WnX_)L^pscG5K6&kAZeLnmiA9~gE^_f;Wo?L0|BB!E%g;K)BF1`$<%*O-bWZ-yhb6Hzn+B7#bpd`lGmrRGP3RYf@WxZW0thdGY#BKw<yy$9wKkJQC$&OsXG9fOxe77T&tvnj#?Ra%8zZT<dY#B>UXkGDqIbkUU4E2ibwld0X$q$wwGl!wbRDF#Eq@1cFR)A}ktz7nj(;@iijB!{*XBn=^Ap1b43Le;lja9HLRpH6mb*$*6$gWdKAU!HX5$|CMh&uT^69Q;B&pH*?DQq!@&SUIiC6kaknD(b}@WOnmR|YbaP$q5D#i*XrU5s-fKt_aTmnv7HSqpL$$8_}?&?$?AW;&N(R%zmQc<}Zie#?>~enxGLVgKY2Gu8GYfiPW>ZI2SVktp*O(hdkBKlGZ>>2)+CTdY{hpuKS&T*<t<WrcUA))}FyveY~4EzDYDOL8gt7Ws<T_XO9owa=_oTLyG<a$dsgA~2^~P3r_BvPT6|qmi#j4W>8va`kRs))#`(YgOe&EHnY0(rslNz>`NWMtTdZyKffmJbB$wUw~vIKx}xbufKxIoQ`w!mS4De@=}0Vz0s=DT%uuR677^arDAOWB}K{r-zpSHQin8KEonrbi*|KZ8<j0rNi16$J%Y)!zOAWp&kDNGxUu1sBJFqWrqtM#*1}`HMM|Azz@C_2pr-{g?xUcSbcAI`)gP%kxhm<9t~0Y7X9luXXm<I?Np&?j<%+APhn{b04PKN}#y~7n<SnRGU(~`ijlF`l?X=~(q$r<?tPF%JrEbZpp{<r;^WwENF0L0f1O|o(`3X&l;yM?U_}HLJEo8T;BBS0ssVD|FLOV-S5mYMxg?NYs$_b+Ata?J4b0X2rsH&E)V{f#dQ3TgYvDhuxmU9iuOys3^GUV#68bp30#$Ctt%LYWWa+ueF5W#m-m9nL@ov2QwFMFnd$Zf6C6Y{|XM1>hmy=5mig_@IUskZ{#>oAmYEW($VH`ghD9<@njZzVL6UjMEoWikANB@3#>3*hEUl~^nSmbVVT38Sj3SHStJKI#={B={RV8Rax#wJR4SlF~=E%9?5*n6aR1G?|J+(M7AuOLC>DXXHp0d5-0IBa2gBYKbnAB8Ofoomx_z^CZcL$*mMt71aXO*}JJM%P@;bO=T%=D^Yu_8mn!WDbu<R>OKkCNw#E*b&j^82G0|L7Hm63;KXTvgfb5&W`3_8+4G|=>m(bJPRL~UNjjFaY3rIitFA3e;hT1^YIQ{j9jCia_45QT<O%M?=h$(@1_R(b2yu9J24z@bX>R5^1qq{XiFp5HyjVJAZ>iJsI7@6ev5s;9;~maYF%^pTv}4y1`DN+td@Cn&Q5qv9_Qn3jBj3g%d36+ZL#ChU>-yO7lGTXaKNy0X?z-)giq_?KmV)|n)0j=~$PZ!Zn$y$;_+?UuVUa&pQHU$h4cZTBekUNXv4SajteJhN3cAS@wgS7P$Qdh<<@(5UHTr_iAIp^1)dB}Ohzzt;z#Q{1rY^W03;i=JbJ26mq!oXPQ=pOC)X-oJPC<FHg5IA6<ZFU2X~N*G!I4RG#L{#!CC`QR<2tOIq#t4i^F`IZ&1}PgYWixa0}bi7WBjX9CJp0CPUs6n{7x8%T3DiLjjJa;BABgXwLAsr4pZ_p2bw3ZP(B{?Dbj{sn5=aMJuB&uD&#4hH;xWeCa`BZrmcqC1ijFU=9U*doF=WZgK}T>Dn4B}xn12NZgy&;H?x$K>x53E!Vn}KInf;9^ioQ+>&|M^(;HWousxpxO5UW38S(xd3@_@dSez;jCy|jUQ9WBM{V;oP_%;XY9|*efr5@=}(sj_C-Kd;lwdBUj2;K!3$P&SA7vCYacCgMa@RB@@;+vFlqZ9sMgA_z66+okzE-8KjT~*OLVo0T>++!)f5dmAbG%J&{H|s|Bm382oB05+YB8BDK5~QZYpy?H;8&b`$P49FAvpi#p-4l7pWnth7dUBuxD<*o{E@!f3$lUZNd?kcn(LNFx!bUy5MF~2kh8@j%nYMgJGw|kQ`BX_5%*zAF*qkT)o$sTiQ@m75F_QUzVzk+`4Yk@ZG#N}fxI7^1+OV8p7CgZXlR<3-EUktTc03SVAV?q;rkht{v6`qA8_*T+oIRQw8P_S%FSt$<T`?*yljyW7n7CVtQvsHUNTi>~&0)3?XNd|TQGzA|6XS!l(0qYx1=a-NOg7aS;h7Sj{MN1@%O?|-@PJ9g{RsJjwUo1Q`eaOZBQJ)fR!iAbZ(pY%XiMhX)O3=(Wp-3VDVEDxVtYOVWroxdXeZ&Q8KnJ;tz};(X=GoELj5(QL*_MsHO&lCiYN%6(uJX7+O6tUWK9jJDxd;!x;hziglqYuyfUAt6vIg{+J@3(7E+`z!#|SHvr(UJ6PHlVtM!T{+w_dMbgi-DX+y}C`5?8ci@MrWyQ^hv@U(zpLb|Rpo~b-lDh;dja8cO`DvnqU%KdY_ASc~`p2{1q_hJPNm|tMw@6-h5PQ6<JS8x+Gwn(kW4l8kDByUA61@o;L*-7GLylJfFvFm7K>=m(q>X`9M1k$7ez%dr@w-IxfFwqzhHfF`wU}3gdowv?O-aFjQiw=lJEj^+A5A(nE#`)O0dOq||>Dcy+nM>+(U(-@~Q#TpaKWS+feX2wW6O-S5$nC1rJt(RnMB|mzmZX?vdRv9%_LP?=V@(O8iOziXYIdb0@u!U4nk({9yCqXZ<TUow;LME@Q7%*0eMpBM9_wPtX;K$de>b?`0%EIDk5nLYkvodrv4eYyhn&2&a-@*Q@sTw;yK!zppzRnKGaewJyotQB;=s0VlB%rr_LOK-lEO7zJq6*YM5@%UOA2~Q4?m?y&uROrQ}X)z8n=?X_RZtN`@^@sd^7pL`wD*c{1r<VH#qcyep0*Z+D_~~?0!7^CXEk*wjG8H8zXpYKtKKc>Hh$n7D$l')).decode('utf-8'))
_ACTIONS_6C8S_3Q = json.loads(zlib.decompress(base64.b85decode('c-rk<U2j`ia{MoP)`Lk=UwPBm+}K#n$dK(2n}IMGAR7b-HV>1$1^eIQSR#3OPjz)wpF`SS_{juC-+R7KcXf63um5}Y@4x@?x4-^z_D{c_{q*VG{hQz3-+lP_>2ZDbbbj_9zyH_2{rBg;eE#^i-~af}zy8nX&%d6%efQ<B+J~P${pGj2U*7$EcYk(%_WEIScD`)B{_u9aen0uchxPi+=dU+!*LNS!&aY=*|Gd6`_~q<;vHSV^$A>qcUVq&GkE^Grzn@P#_Ws@LKYx0^f74>pw_ndT>kl8lwDp&V$B%EneA<0A`*1iAAJ+Hx`?p@q-@1L=<W-;{)7S1l&8Gr2VD`Fj_FxZpE%`Dhi-W$t{EEEm{r%nRbu^x+KimHR-ZpDDdF#u6nT}`EjxXQ+vR@1beSMj!;AiOwukYsX-!G55kL$<zBAS19xO(8yUCtNLhlfw|Mbs|NKmGsCIQVAPJ2sW=;2aL{Y?Su>dwut^G`Bx`-kFoGTXVS|uJ)zdQJDTJoi4Ed(By!f(5ztcmY1;yV>TI%X2#mz=ri^*?sVu5o;%-p`yp(nDOi^a;cx?+Av{|7*>cbYZDi4*lTY5ZrTSRP-{kWMhVbQt0dthin?8uUckDiVK6^i)58lA-$GzvlFTbRdKKA)^!iRKV`+p~I8v5My!&i9h>{hu5tjXjsH7<}bPo1Bw&h|Zd3+DC+`DtTDjA_B^hx_~W>yN+vY5n-|-Tk|NJv<Wz4PN;r#u6#N<4AL`y|pLp3HQ*>5t;osxXLe|3=8m^UjN4Y&ilBkd$+0m*J+ag^R6);Cq_6}xD`JG7$a~`;9k8fZOcsNeVFz(>ti~Az_B+BQs%0_PuT<6SfEeo1DQu4+K(OnXx!wY0~HUdWcw-`i2COF{1Z>7&-GP+r}S~qTQ-~rVBGH?*&2iS=5K)$Vq50zvmTe4ssuMXv0?q=Y2%+J-}}IZT44Zt(Pb1MAXzju*u~a&#W6G|xSdn$pl}UlhCnA&CtVCf3<QKThL=Y1Ze-y4{<!WN74S0W(bQM~Z;9qVy%97UqGX<s;o(+W{%8tN131kB013`TM`XwW4Oi*VlYfq-{o^2KKOXzzu_h)JTQ7F39t6{asC;5+T~^M_iZ5=0BSn|b07Lqshnd|~F;F~6$!R|ciT8S;>`o8H=I!0%zeFAD1&k)$(OrEp1dWDj*O%fDO~;~#AJ7g?8$jGK0lH8SKIprSJ-^j-W`I4i8<got<yZy)M-G<VevNJiWgo7T2YvrUbg4|=H@B~>=<t?cL2oYbhDvz2eQ?Wh`e7jacx*4ibLrSfmtXe$0gdlQ2Yo^#>cv$0@bU3(^V9nA@h^ZKD8-G~B^EXuynXT11BK)<ro)yD2`+8)BiT2i^!QmiZiZnvhp+k}B_oQ#f=-)b8BJ4rV+v7um=O<Vb*+!xhutNeKTd;Tw|DGh8)7c%z{q2lzcC+y;wp&xZGHXR%&LutK0P<I67g*BEy6z&sMF5lDmdTK*l|DNOkXQ%b!FQ$C$dyx^q}2oFR%K%5g#8=x`YX|EB-NczcYNLa<4D|VsZ;^9v<$$q^Uq7>gA6wGxYg@d?Q2x_rAClt}D}r&f%ms+%iT^7{nHt4{CG)$VTjTa^xYeL1)0w0a-tzZ~4(NFp~IExojm=s4IY~J05*Zqc-lF0#_24+I%X*kLyBM5i}8?nEOu^unvKK6aEpf7`wNEF#_$JqZ4g@HdOWk8*B8*92s!_w8-u}_FUsp0oP(?r5?)|x~k-$+CejjxWKU4DmSiRj;L*M9fwks*-ZQ8(olAGz3~nMl;P<{#%jFEc4j~bC^aX8uQPLv!vyLH0=)A)?f1N#5iO_dl3c`$o-)gM^(;k{2Ta#HPwSO21p$8DMWbMQT4O?m9j&{3AIG!UQ>Jy=zPCL##JT7TwOi&kZXLVlbz?ESZi9vxw=&p-?GZrkebA!W--;Qo%qB=blpI9R->_4~4wE^qbkjHL$aGH+J!Gm=j$MG>X0{u%F?X*?0ZWhW*ABt%Y@MepoDYgYf^P1`5#(@p?cHF#%a1Lla{#mA*stsf9#>x}rbWhnM?d-Q7JCtv)XbE}*WNhrXO>4%NQR)s&hC#rl)D-$ZntTtIBsOvZ+|O<Q8OVS(P*T6P;4J;--;<irRcZ^9fG5Ae;mJD%s;=o|MSbri`=31mwC=y59<B0rJvuoSmrx*$*=%>D#7BiVFB*M=rc$tw_wGAtu4sGSbn7$C=!x2k15~;j^;fbb828UFh|SU^jxsoSng(WdSv8G&+{a0R|pU`V|kGyqAlNIBKw7nR^(%~t;7drA5;$J9XJ_mcLC9|_5sDnXv<dxE{lka#C}Z9ef4nU)~aR>oa67+5DYM8U>*w}s`=W~lRQQ1*Z~;xyNh6i(jYhxXd{5TEIU(<KC$gd95hK9P_sL=En&=>g+5d<k~i=ESyn^?^d|yfR3M{lHG1wX!)g5g(aZ2R0G;k6&+aH;Mgy-!2z^I=72W;hcbXj3F+6x+tz-^7A>VpIP2Hc*!*q@Dqq+4x4u0b*z^or^lFF{G{KMW%M&{_ZYnb~v<N8w006k=tt?;q}Ru*uO)_F`kG5byK+KQkQsdGQQRS!p?Ofuw=J0<2uJ8RgREfo_BaZ~qNIwC6ht>Cy~?@HiL!5bgLDWLo(CcVYsk1k0T$@y-*X<)OGZ8-?$kkX~@1n(C7P1F<7>Dv)F&C-h`PZ$_|po{UZI#ZaHwa^-<O6amRUF!ruzR{1}VtWaQEQVe;Ay?860+x_#+81L?+f~uUJ3+I6DL3SmryQ-5wdxxktl_kPF_Jc;nFF;}$*F%bs8DvTbHdKo3)~YXO(k$&*G-dQiBbTcns}x>PO!4BpZYY4mF~!ceiZ5`SQ&l7kyUrHLIef8SBXOoW2NXB-6{i+$dUNfF)2UvV2WWJ@+vhIFU#^QCVRCWH5j1jOT@TuZ=RU?Xx0=MpjQf(O@ZNCmzn})lQfr@2A0W63^040&JJFj%`<Hx_|Iv3TM|$)WQLmo#l%7xt-Q52ZAj$uNxuac+nKN1_8Ty1rS@Niu;^l8m=<gmGsXm%7oH_3cgsNN%z%5N-*QlVan$-ccxci&$|x5b35P?t<=a>;?LszjaRJN4WxgI6GCUiIt7LLF><|G&X?aGkghNEblfi9b&LUnMWVxnOy6E(mfKP|om|9CwB};Y1=GvzqEsV{_Ml+zo9!L(=xr9lQyaBv#S`HyOQdo7&&=k%WTVKCC<gf^^qDFSWCkJ%vtKcA^HG`jJQU)b&FUtuQ9K88fk}aa@!j^Y_bkfE?Phdp6T*$?i$Q*`X3GhAzAcr9ja@zQGq$)y2GAE-ug~WUAfeuI$GS*8;E6dIfw1b6|cB2r<Zn-ABS=Qe5r22%L`sS$uB&E<FaED0<m$TKoxEhGdtmJiTe1eEfmY4_3s0QpMDXoC6_{JnM7mtoCG{*A5rEseCQ4ENKu{W0ucjd>gn>MkFEgMhele-5QNxfh0XdkeWx%93|3ENrKWknn`zMz%XF}fB}Mhp-C^J14aaqR*Mbpj|Z?sw^iOS(b@&9a3CT2IjsrPxL_afm{N;Kj;fYJcO%*^yNu9*bOB4*hlDQc-HDa-F;QYkHs1uZFE08uA02DiN5iDIe0IrNDiz84>(^$SpNo=R$&o1exi6D5panV<Z@}`*PZzn*_T#J~#tV8aMxYT~{gE-AgEA#^Kb+2#d*xNK#{Jlo=8dX=9W%#UVczs$aj^$sEx=7O*lZN-Y_JRnbvntP>_!VBmqWqVerhg(^ky7)GC;e<i5H8_5Pbsf+s?gG8)>9WAF8DU>a1(Y1ht=zK9(SDeIUh5JH92Bpl#%A6s8EUove<_uxix;Bk8e3{X&6cwAQ_sF8J%u8p!mdg@bK2=;XEl4cL1C1C)>TZA%fQjGh)E{EbQtHo1*sS8=2|40IDJBZSh~J4WU9b{0M2WV&?s<l*+}}d1g^ri65&w?T-tsh$TCzg1CZX7QfKM>^2r(k0_PKuabCUD*loCNb>lLD0eJ{@T$*2&mYYl15T0V1#5ER_*y&JguQ!&6U+g26aRmzUY#MA%`*GcyW^Sj%`nX_7zG$`>GI>DKCm7r1O-$}Hz=hJ5q5>;;uPP-<kl9OUm@4?L^up}GPmm-nBv?!1&c|n`)an{?vWpId*z*Eqjglm+sCG5PC9>qpYp`U+}rn)ev&Z_dLenXTMXhs_K7~-FGP9hgCWiF1y>a7r}5!OJ*B&8~J77A1Ll6bX*sY?CD4YtPm^!Y-hD`MX(da*<96XxHuSY%ANLioV!zxfD&7Us<h*y2SIb#Fu<eX~||PF$IkifU(PYXH&8Z&vFX_X?fR+<`2mV`PGZ@?pYnRmv=DjjTn*Zv)@`vi02;U(a{vSqo^V4)n|SOA~3gg{VSTO;g}!wP8e<yqd+DdwuI-{y;gzs?1Qg-o&OjVjg>exnt$=Q7V|}WkXV=Mh-sT)U*((bG4;eAEZ9MdLG)BZ!!~OQkl8akIhyeVtvPlg)aCm@#$GclEx_*sIo%BzS+F>scMLv`ofTlt~XWSuXt-<(BUnhaCTXT)tWGB4oT?rm~|oW0>d7iRFx-Bsv{P(QQUP1s>VXe3I(88xSV=kYq*oii|y#&g%R*K=6u{3P~3q~(L=|(XroOH)#+sL>>M`-MDchFYA`i!^<XaWMIgTaT|_J$H|V4ROSCHzw`ow?_7P&4Qkk>dY*$Id<U=;t!ewcce-U`aAn;V@X~X-hl2zYHF>Y7RVFAErnG9q6C)T>g`Aw?<B0-o}Mml9LAACCR*a*m@LKTlv@=3s=WC1kHz7t)%)Reh)IF|VdCHX#;((NKffAeJUq-mgyI)tfp>uZ+@+aqzcw6Y9h#duk&>{XxApl1ncz04bZpr!VLzf{QDUR*Zx3&jgiQ+m``+-$|e=2-c)g=ItHzzIQ8OJq$%3`F5X!ShoTCbK`{GoKtegIlh#ypzL+@&f8Ym5Y+|t)+D&Lc$${Vbqfgsl=5n(MU|2ROWC@KiVrm+?o<r#d!TRuv+bo7UySlSOU3_vwxU2?Xq8JLN21Dq}uR|m-<4ytfxObm%ZHo%L3w*4!?as#F02^$GYk~E^jE0ekuV7nt1!I#^P(V`7u%Xx|1*_9-sNqdcgcRL3+KcK^H63kI$#A7>xTU^V^C|4U%;1jO7FOKMlPYna*02UJrSr8=GFUg#bK@Y*%wrl*08=BwiJ4M77A|sE|T51}`{VIFhMx9N{@roRBFEbi<y4Y_js7l?B8qLlUPdDYoHACn+!h)r2JOPbI)FnXz_Eq@bLup<>YDpe*Q4Dyo)Du85scShyMr)}rK^rou2C1IEaf<oY#&e7eX$JNP851=-Lzx;|o@h)k&qyyc3Gg=wUet07u$$K+l|{@&{AId_2A{8cFifIKU649G<^f>J=^aJu|<Cpn_x9l~2n|B?sg3LH+^Va)z6IM^8V@6W>?FL9UIso(&X1Nmy?F3z^TeJc2_srei^Bw5GclAK$x3Km%MhH0o>WYkOEShn!$pu6H`AGS~To_G@J;2G1{@iaQARto9~i91{t5=P=Kp(X-XZnBpTE*7ak|AErG$3!&=OrVMZ1k4o%atw)U8fP>+&O~a68ks_m>!~bw-Ec@21{H?pVFYj(B@eV)aq^$@4qkW7SrXNiimhY^@R(V<s>a+URY9bftvIaKR7oLgjohK7YJ{th?yV6ANIhQ7{RD<(VphR(F_no+e3d$MS!bK4Wjq&Fk6@#8cC8*OWEk^4u6n0Q;)9UxMQn?_=~vd6ONlgA7ka2^9s7vL2>=y?R<5D_2GA$sTR`mF@nEmzDz0Km_Ukv4gR}g0B>G8h8c}mi!1RVB+*sg@5x}J-AB$NxvYNuV{@?r6=1-yRzftQH3|3OGQgI5Y_p-7a?N?_hfJ}#h`dcYLo76rXSRw#@iqNalPL>2Arzi4lsgwZoGVsV6lOW!<Rt}BGDiJGh4yEQRRS9rbR$?9J6EXd4`F5q+1-y=elpaLurK_;kwUI+3E{Fr=x~65qj<A=JT07lN&q6&$W)Q(t3+Y)9EI9A3w!n8bPFYdsFD6<Y3mZ{^L!n-!DSFV+uT^~-De6IUe`vl5v@L5H84CE*y5?GGScZBJR^ab(%G;BlroePmKN#LYhbKe3(j-%yc&74>(3ql7&@+Sed#Zs{`!uv>$+xhTSltU+zmoSA!NSktZ}g#+GrxUBGOacecJPLkTv6jIrv2=%m~W$62C|7bF<NC>T?_}qGRm5a6hQY=Ml1phK*<g_JYd6dmT5gD;>*%lR+g%1oqd*dI1Di7=hv;VFe}9}<+(yey0JvjM7~0N0K-~f0Gl8<!YYj?pquMm2%D3vVpfA*l&91nNVAh)_!`TlFpKOoEfjX;)H4li%KI8m-m=CNkl2wb_k-J4awo6))*&T*sV1P4t0(q?EI3*>Mcq#H88S$wb8XSdlrrWu_s~~aQVwY;<1IR_Bk+d~d-W9SNpRdK<V>}uiSOJ9=Pb{~BDyrRsxB>7TiC9^g`qhhTB2fJ7O4+Bw9@#BnU7>**gZFds+?pFuWjzo@us2!j#miT(!vwg={Vq)98YYeB~&qqjAV<<)Q%}oktVKDqtK~PEtvsIM|Ga1Rz*syg_Cx>y!0*x@xv}&MNr(56|4E)E7J^C#lc3OUalrJ_y%yqGJGJ#nhc-N&}L@v7o|}QDd*Z<O*dCf_o~&V?KE69of9=a#}ZiMhhBr3;FgjYxt*@@v9utVU5M7v5$~?if>fCaPbPBZG|ov)6b5j^I5?D~b!2T-)L|G_#1PFWpGjk<`he!8aZyP=iMm6n3$1%NR~6*k$pxg%OO##x))R1uCcwg0(8M`L&{18qS2c);sl`f525-v})V=KY#3<^{At0ViRtQgAJQbMDToWSN4ivRS$5<g93Rw5*0Z5q?!QmS2Yt^~Bv>>lc>s(X<W+a+o{?J@fHP2E@GE&i}=sqw6rcR9_5$uc2!j}E=97|g{QyPaQit@&DH-FYx9T-dxZ>a6uuz+q-wrFR*s1D{xifAqaO%Z_T$@hCD_C*v@V>HN+quVlBL#V4@RP^z)xKi`9P8ejN{J^G^a$!`v6~b1l<7s;xU`!+fM8t*0)df?MC}l-2qwYmdeK3>}->u{26gTTAiLK}&!NuaItt#-Do;s@KnlW|U);C!vvca+<Od$%nFcKBvy`#dKiQcZf?h4swECndqw?J}f&5JC9(Sg8);;P6hHY}-8u~g4xf`VQmxI$uElsIhgs7UHI%eAyw#JnR=z6>Y##>kr7c%o!kA!nk+Rhi98VKzxtB^O;|^b&o(D+h};n^q}2xezDVwvMjR5J$C@47)JOpz+C7bFDKd<5Z+!21GDPG`u0%>C7tJ6{pb<8J{LXViBpsWvCF4lK4-bh+iU0bzLeNC6oZkE5_IPs?lET(-<?!R#L5kAp(ro&SvvUJS!i<l}@@8t-7ImF@)+o3AA&s{#)AL8>7D$PW3}Yjcl7@D{oAD^Idwn`P#VCNQff-SD^ZiP#0@qynmdUY2#^P2l5d)Q7p``JULG+RY-SWv(r+>DmB@@ZC=<B<m$f$M=Y&Pj&2~TUni5mBvJ%rfvF0?3Cr6C5^5>8`pTzt6e_tiCWCkYajb$=6=`lJfo!des8CGS^7vMR$Yb=YbVyy=(&Z@1Sb&aTDq+Gobg<i1A8RaOxuo(_QlWT1oWZzbu40T|fX`P<zv^d>W$NuzUrHz17%87sK{v7DJ!zd)VPtR?s3vnpNoHaF7o`qeDRKR#rmMiA(U}O{oVDc8e}uw!$5k>?m`yvEo-~$42c#RUXG&GF8o+Y6pdht-+n;X-3K(&19r!+mn#O0M%t}qmj;_#9o$vGE_xRAOp0Cfe((&X<YZo~c{VS9bE_U%{C}ln#5GMo2Yn#j3^3tZcp#dc^&c0+iY*n!GaxClZQenL<z9)7Y=;cLM`}<jMoJw}&3YH0R$>qBpschxZC~wEBWBIihZ)3|?YC`LZ=gSF8DPX8qY`2wBZcBc!1erMuMW*U&Bp~Hf9kBvjvux$E51bCcM`w(~B09@(O$ONqI#uw%9&D_FWvL2J&aPucFGY5pN&@LoA&PhpOF-1g=a~>d!+F-JxK3e<F?1ed7b}^B)WNhrje{5FQ@t{fp@cGNn=VH6l<s1j3js1BJiAo663tqWqd2Ck*MLr0Bs9~x1hYyLzr%yK5Aj=;6!9}^YYh7*kC>^p7YT&vifnt7(2YcyuaI^?5c#3kj83nk8QEgRQU>jf>)=Y}-7PD;JGIUTRh6aQS#M$18e5V}(YMG~yuK&6o~?amt=cl6o0IbrUKfEm)oNNN7?C|Hm>P|IMQSj;!I!Id`?9_elwPYUH)5d)@RV*V;{cvKdNI;lVBLMQaOcVEj`{*58v$a&Q+@pvROWP?qqqFR&6Ae`%<7F+mF5x+E0bua)F~Bf11Kp{2KZK?K$1G7*=k86`dqZDv)ZU^xk_T$(&!OPruA)2m3vmug~p8yrxa<wYd59FuCx{&^DR>9ECcq$`~p2KkZ~UcounfyJF5Oj)yY*!hjg8p<v25twL-JYM^37%$thP{Jw5b%Q)}>|oH7PtnIdmNt@@%Cu4(KQv~8y?*Cj>yRAgl!Tq$)+Rt;^n6q^^Xt#NU^s39;gM95EQN)*?*pv1=pU1}k_O%)mS=1D~{xDnb}nu?%W0Vu>nEKp7mMQ7C$(wq~CZbntLd>wnE{fr{GR*J=L!M2=hSY{$Gy^|qVchw;B8!_%Wu3t7FqLstE4ulB4o2ry8rR_v@Dt*~A1w?LZm7b6fCLk)zXzDFHxhd3~R7<@T*j|UBjAIeL#Jssq`SYkvDtjxTk@Wg^Eh&rPA1ql=EnWaOU#i4n5wN^<08SWHUA+R%U-eP1KqJB5;K?Yb39DVXAd!?lvQ^ep1Hp_1U8BiV9EvVlRbG-SO+6z=vdD8R&l_2s@={B5krX-fQt8x^>YOJ@Moey{u&SsQsLtL^Wm$$<L~1Haaa)PnW7Sw~yG)tZbx`+7$WF2)TdZ@m6*YLC2()0^DFP=>`y-TjI5G2k^~jzdby+9bkaR*OyHC=wq)l7b<XLrXSqk5@dsV9|Lg+Z%b*i5ycp*=4CqBoHD>fJa-$97Ovok2e3QKb{*C|LCeM`jqC*#G^DSJzup2t~Y!-;j23mETkmWruRw5J`rj>s=dZ|7S%nTygGDX}m1Hy-&m7Rjrls2ei<OkdZ>j+d-P?Eb+J<aF0<msGSazq1t7mz&0HdPjZ;OV^yHF2FC7It+{av5G=mfo{-#Nb@@ZfsGYR(PPc*LsigCrmz**B}L9yi7eMgrmN8xbpBYTw5}F7$U$VFr2^)dhcR`*?O5oaVVR4bV<xTmQ=9^g+@^*GYj6t6lNI#-EFfPKd`S}qZw-!2nj@B`lPP&FtRL55<s|(OGng-`_HAYx4ph@uOC4xPza8UWl`?4<S8_sMAmVqzK-9t#Rcl;5=@G$f9joOjKzEpur#a9(d4=-vpihxD^ulDVGw4}Khg2a?>AZ1tpfZ6y(=lx|+$QLSUNpD7=;1VJl^vA(s#o#p!pZIG7ICvv8@-vOq+BO-A{B-p>Bx!Z2&b1)qFr}Zo1WgdvV`sV98mHmRm_O@?_hXQU&Z27aX5*LOo{5*V(Ew3d&9RmSpPuKjW6{`hmx*??(9b8467wKUPkaPxImT&ZoBvnv9*JBc7d1VX%ye2j2oTs2OFdyQmFtM&2&le6X>dn-VsA8E#)3d`HcwJx}{l}oV{5$vahTI-xSfo!VoDe-<BXXB?e8eK;4jPer<ZE8<^!8Q|z9|LoN#gSJ0CK9au5Z({?$NEkov}KjAAO1dH~O$PhN_@hwWwDK+e9*2}czGn#=nC(EZw!eCw=K*r`g;qQDOEuG?}T8fd({}ZFlrfsOzhM~z|(!u2cS=WZ;1he1?ZkP;eD`06gl(6H0-~vGcsW9EV5{uPDt=NFBc<1cV+{n02iGIO#n&^sAahXJ?UBSfNQk)8~L_{L}JZ=uNjW|nG5Q!2r8JHL!q=n`SWGk>H2xqdX&Ir$x_~f^C1zA3su!ILpBJM}X7p$e6jngM%x*K^hEVWw7rh5B21wmUf-=?OM<SnzKB1*Ab))L$E87MQPjzBvJN6jGZXKXF|GD#!*S`_N9AssTW39M;mkWxfJ0F^Eb71M52uOe$|NL2w9h||@{m?K=vALW(#M5P!`g3&gVCbN(tg&F>lgr1H1bep(@a$c=hEZL@K#HDME9ZwrVw#)~qU0u}GrrKRCV}qv!6cf^QmGMmFsZwcJrH6~kR#0)oYEbT<>jgRK2J}?kc)b@ZXu$je3xB63Fn8+R3b=xssIf(AMRr(;6C-&mYAKj+&B#s?C*w_HHIH3K8)L7C1ysk3Um}nu6#$O0c)yL9yM&3xh_Ep$z6J}k&FZ{$PV(O2ZeDaiG-~My?SGj6tvAlc-qrJ=e@e%;XUtqupZl7Y%A2~$sQyVyyXaFTN|>1Z_Cs!0o$f(V4Ivt@q_!l*EYsU6EVrk;JQ-_B7)^BMvsbe#C5b;}?ABb7huSTfA|j`;rv_(kl!$Vfy6!_d^zc|0Q%;k*p!&PP1s4!om3pKCnTy;}?2aAWTRi0CwUr}<JdTg7(b<i269R3=z?ks>3FS@Xl@$lJeUnsWt+%H{o01f+>FOy6M<r6FeqB<~Q+oI*MS4!#SDljA-`BX6<h5@eAKo9n_2rw%2i{lkv*)i^y12oi7xa_bUDtME_hI+r**9r?5VY+uWY`$NTLb#(?@#{+fyYZt')).decode('utf-8'))
_ACTIONS_6C12S_4Q_FIRST_YARN = json.loads(zlib.decompress(base64.b85decode('c-rk<%Wfn|a{L#bd0;(QBz5C-*J>Ke88%3^3ade3Fo0GNAgm4}-Gu#j^^*0-%CImu^N3`#N4yn^#msnzyScgfFaLY?@4x;2x4-^=_D{c@{qW_}-N#=)-#$Kld03xq&(HqjxBvRL|Ni=yuOI*R+wcGR*Z=wY`IoaFKRy3d`|!h;zx;ap^QWI~@6OK8KHP84&gaF~k3X*0p9g<<T(3WV{d)7``u6GU{A%>|PwTt;pU=)`ho66bxc~U&!_)CUR@?30&xalR{OQA=zkEKvX*THFFK3(e<I{6nf4+Zs`tkYG;j7Vy(}8$g-`ySGx){H8|G2@cKtqPFJ$@Qb1!}<Pb=BE}Jv_AJc}`|0eck<vyzBGb?T2-3JW+r4{{Y@LYBzc7?q7!ES+wK%yPuDX;iRv-nX3FO9O3ot`2EM_ar?A>7%!sncc-fdF5UTf5k202884!8asKHaJLBY=QSaDPmV<LTz@t$*_V2^(ZfWj+^s+MtUAN})I9%mR_oFcURXAN>|DnkNJE2&?<So0g2V*uEj$+2j-{>>88+ST%C(j-4yyFm-(^OfPGvROpo1uEN^0Vcn3);w{LnofReM|MRl)s7R5e(t(gaLCD&6_@mhj$!4d_8*~(Fbqfj^p0);N36jr1yP3o$xLl*#Ga~O<kWGe)tBD9o;I6iZvM=rp5)*=c(hf)!DwU-h#0`LVjA95q(<l;r{M!{o(1?Kdm30KHYu#*V8kh)8M6FVl0vLJ0_Zg{jEJ{PjwF+9FftFD_8mD*02EI^!hjEcihKi-n$L$zebw`n0JNwI55J&!p-;@z!-sh0{3dSv@J84_hH!EsE^?Q0>|DkNSUhwKSd8@V}U+}4`d#JXg@aiqxB{y9jN-CO17`Efv9gD&p+{W+FV}+cnTi}y=B9B0LK0Ck)<&hZ~hWEA+}}QKI?IzsY-COS2nEQpVt3r^1Tmis3iulXH7-{0+K~jgI#QGR~$ogDz|fJ9VD*7$Pj3R>ZFUIi-CY}#_FY!yc-#~emt(*Mg_dgc{DW^z*}nbAKnO>4UsZW$nbEhEq*iwr~#a20e}SOq9fAffQGBI>&ZXH(*8Ke+52PPA8TS#b?e2B)q`MqB`P0ST9=tKGvkY!;7HQtGr*9x=wW1cWegM#QgYf)LgKAnD7(`uWAo$f!@txz)(RL6x}&@LVh9=y)uAuRAsUWF3qPP7oHBrTU;;FuAbijd9ea7J>C6Co<S;11k&3Yl0FIn2yW<+&56UrIDG&PbiRe-pzHe+_S<&G=!Ghjg;0>AZaQWbp<MeJIyg#-T;kk5dq|4_$e?sHC)<K`D5w$aw9-kg=H$SW&9{vJ=bSZAcF0pFEmA6|^NE~B2ZAq8l(ndd$eIrVbpM~RQ7=~l`svS}?q8Kdbw3*6i8rmB}h|0r^crdGJeH=a<F6sDj8VtL?V+Y$1b5T1+9-I7)@dzYWL9O4`*DuY?+IZ;GOG7ge&+^_P{4;?%?L01n^G(K%dyg}HtEkn=wrLtHmBlu3d{WHd<W*lc;=}!uXOf`vRq>Ch`yJscnR|r+5QAHAbANyLoTdVesNElTGxYU<{3t{MkG{ASu1nL0&f%mMnKz7_(1|TF9@N?eARDp!$&rUV2b}>!2W0*9zU6zzz)0dt=CYMgp{4+;?s&8@jmo%h2wX{EYVj!zKduvDMbJcmVje$bz&Zr_4fsdEVr<?D#t4*ij!v}k*^t=_Y^>2Ib7a8zQzE<L*mI6Y1zd}fl{%F%w94e5+Cej5MJ;jIY#AF@Fh|t3xTc{LMK;rMxfGP0LvOsp0A+Z(k+B@FvYZ(Z0t(H^%GZ&(#$f{W1OeW8oc4R3&WM)NbxAH_L{Ayzyn2=*$^)kBou~E6n8GZcm_sxQwx={ERM^qF%a3t9i#=spr{#OgV?&&awotoeZsXRmdtNsdtJiI%A;zr?Heq=Lkb57rX!N&ahAXoP!Vf725%jm(sbq)A9A~=e8+By5hlifj7;afA!y%cN^x=tyS)+3}cInQG7p*r4N96=10*c3{7Cra2h8%&#>C2g5iS<s<icmkGA<mr4Z&5QS>n=(=Pw$2}BQr;uX2|<1Zz%XP%L7RyPf+9N@W&R4UXDd~*vCWMx8?}!e=CGtEi;?bM6ubhe>i3mrGn-jq6iMf!#wWq>z_W|{du>*YF<+L%Q%&;1q|P9-<S8z=JBpvkX?C&A%Y_Q5=}5zSvH2iJsy2t2|pLCL$I#}?HF%&cu^%GvvW$dCvYwwxtl|)r@%x?il^tV<;L<blf#1~riGpdIle+P5$v?k%`C|o1C6l23Z<>Y$7ma_4(1&gq-=Kqg|qSj$uMe3ZUrud2&2?pf|w}lfzGAP%)C9vIn2QwV9dZgCO%}7yBnOcE{!AGpiTu(;ucDK;4q+VQ2LP*jG#BG<uP1ok~E$%V$hhdFSR0aioru%h(KYkN6j!4zbsx5a@#C_UHM={=6ZYD-;6W0Qh4CG5TWmRFKhQX`JJW*HHAwKERe_}C+u4<s;N8Zah$F&XsG?{LJ6t^026<(p((qyR<2)5)+BT4%T>(17d^(S6MA%A;};It60aq26#`F(NDj3{j|pjQS;Zj)qSf%mJRO8IyHJT;VJ+Sgx1ilN+~|^xiM6;zr&;+2kDpc^S>oGxh6pf?8h{Fo1x1k?$*s*~JDa{V!$*<q3E0PEB_-Wz0K6CWSw#wF3~Uesy8&G(7cO&QB`cNLt1RM;K-8H*-(|w%MtrEzex-0#&ZJK^Od3y?dY)-OFE>DmH@-%*@+8l0j$F$y0#j~k-!8XF-a@P1=wLO5`@i7^eaq-U+J}y*Io~eiPKYry_sVkAMB1JVL0Hjuxs}Wa%*3Uxwr%pnN!JTlW0O!u!8&OZjP$(8HUcQ%yRwB4ME=l2I!agLS24J%nuF9_N2kPVGzu$CnJdAqevUKNMH1t-QzV5+p<LYR+QJMm;G3<!or6qPw#HB-n5?!6Ag|B27H@_f0u2P)ENt!U!of$#!NQgW$UZrK1;hBbt=DC&qh2iHYHLt>DMrFqFzc=w;y^uH8Mp<R7dCldUN~BjZ8}LBLE?04A(nd}&<$%U+RN+Yzq7p~*(kh~G)LBtK$XGlxKD9O%9+q#c8&qBKpPa4LQA@snaay;CUcHrtclb^I39qyEq8U*n6y=biO5!iU~;wOV$1_svt3lBgP~PoC&t0SuG}h+`6@{7089+E7%m2d{s&7=uH&PjH~|9qv=?<kL(i)-6OF&isn`$0#qe-ElCx>m-xr~iPU+Y4MK<MugEBf6b2=jPspuDR$zaR%o}7qrWcgEy`V{y_OXf1DdTYU9ED|c`f)7V3qfR8VESeKQyyuqo=&+}HeQ0IbsY2uovIx782vO4o#wiGtMH~wf2K>m%6@I<VphO|E=O&+q<nks82Jo*KKU<}{tQ({zOUh9xjYA3l64sDhD=}7pspiF=f87NkS!|5lR#!d>)=6Dd-aAiNj&UgdZmV-roF^i{H|sYIocnSM_zFq1JUj7~IxtY=qygqW(}c%z8;P#K%z$Tt(O(OIS$zg3x~()Av!$gP6EwV?v}32K4UtBYbW>54gD6?UTrKRzOAEzmWi)AP^d(`OP5rK`k%U6L$rufe-(l6utRdGb3x3ojBq~HO>3|6a-%KLv^g$4dw(*>2?B=qHkWPT<^n`6(fQKdfPX*urBqs<}7Fg79POh7!T@S~$o;;H$;4rW|ZamDEsY%5NNDFn_qE7m!M4fbX%%D0<Mpwk8^huiNGZeBgWLcv5=~Me#Pfyc$D<~|WS)m%8ie#pNQd|j=S4BqNNLMI#81=?ELnMLNl&FY^1~3W0lCh9OYDgqrVw=?hiQyE^T_qU}B=YjMy7<mgN)LnD6q1KXO>$ggUhEJ36`^5@nom-Nk2z4>|Dj^I3HlzGP|eR{@*a|8d=kBp_-9gFSrhimx_#iVRp+=IP?fEj_ECvFs6_24Ju9A-4z)Hpslr{X+A>%=^h0;clR>VdA^s^UEd~ah41T2mMPznto&>AYMInBwGN$s`qUJ7|X&o<V*4Gsn;Ibfl%)Xg+Mh`6D)zmCYt69YW1`8Y62JtF!X&a@b-%JJo)?)!=h<X5-A~G<0D3o+#>;W^^!^4Ey%Q`7DkwFm%Xtr!xVP;_hX>$lVIq|*3R+A(RNkemu<}+HEK_o-WTMC&kjnte7m(jHPz~!GTa#m(_kOEERI+k)91QxrW)+4PB>d$i{cJHH(QedKZkBCtyB2Fylf`Uu+TosD_8}uz8gGC3ORQB@H^jM=nReC<fY6U$nHI7!aS_=pbn@4iU<!Y|k)28A%#)uI;Wj=w}B^`cCae+)#11))txRaW{$D~)aBZg>S@mw}ZBep)SwqHrn9I;jnt-U57Dj7IlId7vCDAeJw$CH5cd_N0&rJji*N*U7~Rjo8_3;#4jj7juhRm&**9w33x)47=n5eWQH!)LI3FCoy6Zy3`F_FQ!t>@brl5=EuTDHAj2I%-4s^ViSQZ}XDH5t1Y8H;px9!l?P-4_(wchv(lilRPE5aV-kn<)q2}d8$yIG-F@^4T^~jr^qQtD7l=fx@LNRYyKNiUeUNIhD%1rox43LUy!CiXp*LhlN@y<a&;*UIJ4kt7pscgHB!noF$HcJrxBm@N{|Q&-aufL5;sa0znax+@S@seHTYn+MuH!nM#D4Lo{ub<y0Swg@e7?d)7jBkmdY8+KZNhInw%P~#z)byBuk2?Q`#l-Og1DWy%U!ct;Ro<&w&bFDj=O;M(Y|sBCA;Au``Do;~VpBf=G=j<M|Q;VISm02D@fSTLNRUM9BvyXlU27>zV6SMd!3mK4m*zUv@02oi4_~=-Sl1Vd89IEQm!SQXyBu^)3nhl9#T@V=4ffxZfEWuT1m+3tW$fOHOJ+&X8rH5*{qq*bwt8W%)m))nMg|#UZr1;QnCWY;ztey1u2Ncf@zIge0#86G@l*;6?>Sxd@XbUNo0h%uS_FNb0C+K@L%dPl+B1us(0H1`nV<S_-9|G8mYWrGY8%IBr%Y5%{$n<ibr?KQ$atc(t8Rl8`{y+)A>)DsI>^lR~9o%1#%LFfn3YeO1qCT_l+a8W&3}w?yk|wf1msZBJI3g{ljb5)4ILzGZ2)D>&BQ@a#0rhA381%>Fw>x2SgG3;XYCa#$;bT1fIgq&80wI_{qOpCP~5<NzbYYn4RL5(4_B@xKb^Lv}+AErB#$U<3v+IpUXo^&`>8Fb=r(Xtmi!zPwtERt(o?Xcpj*CcJ@K+(;l%vY`r++JX89@}0TQpXJ36J#JJcF;+vVSV`ex2Qvi_0g8n<c_PL7&W8F}`frImu~cj)Ko5f`c(rgIgrY6$GcZRZ5s)`xZo%nxWDtxO(q>e83ZR@e$gRz=5PegyC*o17G>tnfDy}nEtY9Y%KF~3u`2v3YM}#!2;Z*7L$bVU=z8;}Hw0r_Xoj@d|9FPdt3Nk+okJ>>30&sAxD{l6|-1@o0L*I8<xXFO)as8chJ-T$m@`_<CG8U)&7F3Un^qERuitQB7L*A@yyaA=J!N5#LKaRP~9pDJqv-X7fZtiwry@qb%DNSNm@(CsA5-5Z)BC4g3uAKx}>JprW?S*K)4xOZmHL|J&glM4iwWwBln%tpOLu5x(1PO4_nwDCafF5%jiFN6uxu!~4G|U_1VZpOTt4G<$gVU>>ia~Uqev@Mnm&c$~UAKbvaZa)xXkKg$R<=r2P>G&ieKAT<W7v+K5eAofjo{7QU405xj+7RtIKY4fn=~Sh|BW;Lt#Zgw(4PVjwtH7}4J#~51gP?FHPly%dB^VAQiOe&@e;3hz6YcM$wL8U(;b}$S}2P0+Y-bHfkxXZ_K14Me#ItdF!5&X*XJNH2!GEkbS&N*C0qLC)eD6$R28^TXqD%Z<|Ioi1F8jDm6f9-N~%A+d=>YkUCLmH`pjy2h$q!At9a1tyJbhbGWx?bP2L9dQv)3$BY-OgB%@Sns!twQiMqw$x<+S5B*!$D3he_2DTzJ+@d~5PYUxV<*1mQ!dO$%1pnHxsMuz3mS$5&7tri1L&BswxNmXAhJ3lYQc1hLwi&PN@Bh$=Dos;*eI2PC2L|q7Ut<Y#aPk+z&yk3S-*@aO1;v^ljWKBdsfFHJ=&9@m`Rg|El5Gs#p^m7{7#$mOlrN7yR0Pc$tkEh;{CM_sdZcR?el~E=MA@q<=pchpk36Oml*#sN~VK7lYPs}&4xd<z9cR)*2L->il?7(-@w116dc8Pto+BJIKO3b3^cP#CcK_WcQC(oO>c7So9O;q;h<EMXS5~(p{WA!E{t%-dcrkBeAEUFo6ck3#jZlxMEJgQ>Jw)#oa*ZKZwt+lc9hKeDb*X2gbSM<T^3V!->rw@>>>usJJrS>~1wo`rYY*s<%Zr*XX&Lv1F9`p(tI}vOU@wQRI9;!%kIZe$GOc!-J<-sX>x`(31kr3t)njX~7$dq_!tUW+VUAC$0<o~YTJ(t^F*;kqs4v7S|?{S@ybk!X}BL1Q#0Ew})kyu(wWfVhzhi@UmSL!O@$RvjtPfGhLH7N^YVNs|`%N%3>sUkbeOf|{~g#}(VHxg_3wx+sL20~BQ)OkY{9>V>>!6-!*L)YW-&oZS8l&ztt$nZ`j!sSevC{ZvyE-VWs!p~R{O1XM^ZfXe*Y~;zqzi{NNj#==OK^CV1Dl{?=X<IlhE;A=Y@g;0e_khLJSON0|<Q+p~_&N$L#o{(pE!r!>O84`0({>r3WBg#<u*5m9{#cv1%XzX?wR+5w=tvs4Z3+D_rY4E)(5^XE1Sb_3nuvUMRRlIx-)rXK>i}MIrPsQqz;qNdFU!r!H`FpdnqaP22c=cYI91T*6`-$RQR$Mv)pgj_X_Qx<nX^}cV>-;5f=jridl^V9gUIdaQy$P2x%m|!O!5)+PFyy@S{yN~QsW7J)CU=|fGvQhR5RH`ePLBUf@3R-#`?fw5db<duC&O^SWn?;!X<iQSgW3L>i2^nKUmjEUpF*B5}65IdqQ(`H7Hehgnt7v083Ful96-;Pw8=i1ICRv;Fi9*pUqjW5w2Sv54V<dCzY|)E;6M60nM0`70p|8%&*ee04ECvzzBf?SQRU`U<XZ6HP0bh;z27i=a(i}5Y~R6v>Zy&@v5+g)|U)C9t25HcP;yyAco3*rlhlS%HSp6Mc_=<&bLZi>&k_dgIHT!Z5Y%|0X5Z7sZ|9gOCvmBX?@SA)CO4|RQ-yU7!#VEaMuQCP7!Rzjl|!I;777lDr1U4TTReI6qpiC*<=ph*DhdXf`+*SM=g0y7v*kaTlKKD*}R3cBX;7m_1T5o1rqy+HgiHK-Qg<=JvwgyWpzD!BEJ^OQ?qj~6*N+Uc!Zc&A+QhdsB6hE>Nks^cEq)lBxs1|>#}Ba8>Xgm?&JwV|BrL7<jddpNm8C}MnaBa&h^aIHXehpp(=t`#RAmB0W4_PkVCkLS)`@C0YVcXE*DBy;LE8#Yra}jdCbqVxLss<;{S?4Cp$|YOyZ4`^sU11GNQzeo>X^MDPTJy$H6TLR&toVn<NV9mIoDcBCBg1A(Ua+^1fy1ZhF*lizZl$*+t2(MPAx!8)6i-BELB6^*mdpf=8G%opVjY42{E0;4c)v?O0JV6kNuRv{o0hK3)p#H=j|eL94WfCEQw*7Bt+3uIOD!6szh#&#vE-COZ{ytDD8IO(M%fLu&Dx&AKa_%uv|R=}&R^Wr|eDY-S*x038bJlKx2f`D<F_=X97l2bh@K6OnE3w*Uc*CD8j+nTtFdmkTuwjgZoag8a~OS=31iJ=EO@7OD#ZQaWLknBzBJT13aqs-GHo3Zi2Pp@)8_$U>q}7rRR}he=&VRv~h*g6n>uk@sH5TE=T2A@3N}PJ|~E(?G0Y=!{{&4%1p%by61_9z9}WALSPqVC99A<pLr8fHoy1EhqesD|hv9Y7yvA4T+-(J$p|ph2O7)9ln1-#Z(|ZZO!E?c~f8az{CAhx+WWjjC0;E!PdC2P%L3Cn^<k|-LB8OF*QY`SSW2MxK22q0k&D?Kqa->8YKEO%qgC1dhNCqnQQ?qOaHRm%WMc@K&yTnWi`S8RI|vB02gKq<5_f9L@6<>hO;*SrRec8KO{+|v1<c3Jz>V3fNtM;5y%oioD^S+NYoo4S^hOd$-??i2JjS?xnl$&F`la7ZeH#wC(K!*U{pq?5}Ht!(`GUboiKsn2v}5qJGRUhE%U8qFn~~<HPTn*JTDjYG6w`I$_#PBMw6<UcgJT?pxUy;ztD?ns)Q^r86uwRi#GgG%TH7ewKf>FYQ~D@P6E%2FymCoh86%})wanMowifb<0@PMMD(3jRL}4qS9}HR@`5fhT5kc-Cn%uJ(h$_iy|LzY-X@5~xdPEz4(m3xxu%_Z7NjE3Z1dW-HP7Z+=`u30mnqFSy4B9Z6lp=xWh%-Z^I6y-Q+ACCWU32t(cO$H?M4w1XRDFG@O>tV#cANnF}*BgIM8%oo02%QW=|-TVrGT&Av&yZED_&+OV)UM`fhZYuj(@0tQ*$rtnFr`t_?|$l>~gM%bu!UrloG`YW*qihv&c0pb-yEF><a?Mz}F=&}=5ZUXMJe!YZkEv`)E>;LfK;aBDkM$2P08IeSZ7NDv}?6B2to0KYcS=xPre@i7wu6yYVK62p9(t^FD~Lut%22z&}Fu*yZ>CQ8E^S%5OTQm%Td2{PChT)8NtzD4t@uaGvls}av-mmB4V3Ca9%;fKzbnl23xQMQ3|rPsOOt9^3VmL<k=J&Bk#LN(B=5^MGrC0+x;7Gs4>8^7>ynw67{$S-uE2rZhQ*5!CzK&Ll3V1U<iF9{<w-B&zzy*kf*yhc{8mQ!CSyQliqYkPxYO%Ixkr$;@F@)I7YllA@>dtIAA319C6>Fi=1soT<9$6~d|@az(})xDutk(Z3CG1Lp_R@36mD>94@_|((V5DFX)LpwDmE#cj&i;PLnQo^+oQ*nZPGB#`22!5qetqi)l{Z{6EnXblK&Jqisf}N<&Wd>_rY8y0Mr30^_OrG<~en_DPL7Ll{-dP6>HN%YI1*_6EZ5FRic0D=i6~Dd%RC@6Sq0(38yEYWzb)@gpkf<TbWysYW?krSv_i93hYg`S@p~^K^;Y}=<?y3EeShX!7-@;JsB>s3VDSEKhuX@F6sX-Soek_i$US+ov?R29R*(CKNnky76+aME90ykB{rZ%1Cs*G{J1Y5L4QzGQ{sJ*%BO*R7s5+ox%VuRCNo2bzur9LIj(qx>^sC!gpeoc*-D8x!y8_*$tr{tPqbh8BqV-y|vQt?@F^T|RfffuP13}CKln*`#j4G1!sqgtVssIFfMvVB>SSI%*i#!?u$bR)`=h9N_F6dFS=Y(WRf!(2&`^R`|~l9XC=1@c?~|FZ6RALLReWJ$`o`zRo-i!0i;KDOzxWHn%jun-v1#{&=q@bkH%^B#z<BHqcw@a6ND(b{^*JgD;uKr>e9Qfz*)r)L*f<Z>c5$zm$F^Q3<0r5xVceYIB@`F~K$rV{{iOd=RHaZ&veEKT^kYGf(J9bHzZi=3RL+XVxeFslL^b7}ODSzGY^5ydbnqak39GKJD${<E}KCCjrZEx%S)%d_^K>Obg;5>p_p9!PAxa_z)|r$CF-A`lI?XF3SKVTztI#u``mwOM?<k`Tdx8%_<geiCH8UGuM+OmPwuU@jvo=`Bk31r+s#tA&>+rDEmhv&gezf5y`#RLAzN4zM(VlPOhOmCeqs9utJe%LA?in)gLq<Z8%0!#ThM;zX42<e==HI?-_IfKC|$c1tpBTuHQ^T=S^bXz?MG<n!W?T^5^2pu!EWN=q`Q{P<6M@AT!I>7uJNZaZ9CY6<yT;d!O}?aMLKc?VtOF_euYNlx}vC-U(kk57{zDNi&$oyXd&Dry$F`83w3R)1w3repfO2vh!=N-ssBS#7e2hG$CgoO1tdYa@`&-w2|JXf<}3zFsNXvz1;z`j4cgSq9*$49xkPVIc-80_z&w7@BDWY2d81sJvW9E?z(<jP>|Jju($ni)STF6K7x)Y?i}i0%xWP_ep``Bn1+t81Up$;aFT|@<d5ACeC=x@OrEs5R^#^d74%q@tmq8naeh?qF73LF>Jlkoi7`ZA<U4hB3g?n%O2^H(qCRU*#gh;$s5k7)LR22mx`7u1SUm2t+my*#G+r-X`?}{f}h6rfiId!hBvswMV4oqdRZA^2a`Y+4Y8N3MMJdZ;42hOErBbfUD8$+ST})6L43s2a|Q{Q<O(ZaOzo|laXuHkZk2jB?88A%fhXG#L4vUV4LQjYWGv-BDjPs3R+cz0y()>B!XIV%qDVI)-I+ydKkgS9xYv|RxO~v*1A9ygjlu*4psSp`61UnoB8RGEmvUOL{JU!W4xjkrNk9uRJu%B($W;~DoY(RI0O&LC4Re+A@CGX{*Y2j}BsG~?YBuvn6=X$AnbqrywrjJ&fn7A~C1+bsC|S*<Fo0%B*1gvQmgdxyQAlg%vgn{LBWWGeh+q@QRDf1eP3YJ&4G>B_odS$0v?z4}7q-e+mDZq=q_v*-1xiHbH4?iwS5eYn5Vzv>h*GO(BUZu)REE&tO4y6yU&O4Yf84sakB?e?h;dV`=E;*fFh}<-qfI>g(Nu_)s0UODt7zWQLo5Dt_#p5aOQ7K8pV8E^(Mo)1Y!)nV`UcvC4~n<YvMz0SZ`FIN-e9Z7aWVGKm!-#A<7<@FudbW?*g)<)P%Cv(pA6RTMvmpzYmj*cO(>=m41{HF!ZCM67^@*-@?yZmW5y8`LZreCu@@Z6LPcyWW{?SW$%%Owfw<OW6U#J{fN#t;c{As$fwnMtUI!JAhL$dQ#jj+6hK~>TpX*jLg-U4@yC{NUC^d*CnWz?H4a@)*7p}mhpU(g=;2#u2QHf#|_i@-;gk6BQglhBNy~3(IF_e^&M-8C`PCotyeMS4aS7#+rqRIM7&(B<EcL!D=p|L;J2IPkQSG5n~IaZpY`;+Y=Ho`%>4*RV<i8qx)keSV>soTGA{||QnE?W')).decode('utf-8'))
_ACTIONS_6C12S_4Q_SECOND_YARN = json.loads(zlib.decompress(base64.b85decode('c-rk<U2j`ia{MoP)`Lk=5|uZN&D}9pGcsg*h0Q=143G^11e=FR-h%x1IFd+S-cwy&)#p(5IC{ILDc<vax~r?JfBEl|fBo(EfBgOTlYjc<<cH7iZ{Gd-;ripJ&v%=XhtrdP`|Use<v+jt&zHx4{Pz35|NXzdJpXd?<NL?|)gFHM{I_4Pe}4bd_07rY$=loelhbAM@y8!Gn-7!!__*1;`||PqkDKdHC#RRQkAK?S-2QxWy4ZdF!`<z>&u>5N|Kj4|;eSr29sBV9?O#5B*uQBp>Dw<S_nVKO9^3l!?cJvzAD?y~%^nU1;^XG#X8+c+`CGR?H+dCk$n>@Qr}<Q%2FzX;&K~UHt|gCivN-7L^S8*mKHOZt-9+Pw`m_B5@U~gI$y=ZQWICQrJ03s#dA}GA`uaRm!Pn9e-dxY$zh55LpEh^%MKu5HaP`2YyPPkgkGG%ai>O_kfBL_jaq!8kcWf%#!8sh@*(mM%_xAdEX>Pytv@<7Nx8`y`T<uG@qcHteI$dD@p~(R|p;^J?Eze^Q#%wYi&5X6*(P!*=-09FA{O)|`?T4_PreIwzgu@MNhVW?RXUjnsw2?)JPCj|tmg-|Ef0EB57{cch2Fy`5Z~7qa-m!c5a`t{i58lA-$Gzu=pT9{beeCbk2_Mpd?cYw`H1v1Vhp+Invs>jXuqKnk)VM&#{ObH{b++$|w_t9Mkgqmo#F!Smy}h~Fy#4g+pEh@&-rv0c=fg8$(BPF{Vl0vJJB~C5+gp3mo^TKC9Ff_VgRA`f!LR_o>Gf~S@4Szzx_6t}f1Nf7Fz*`kabkpng<J76fH4C11n$-I(zeWG-iK*#vp%K+2poIEAZ4x!e9C^1jRks2e~@_uqW#$6kH$?dI#BVTO17`Efv9hu&p+{W`dnWHcuIc`ddr6M0F3+nPqxNjzWH0=gxHpO`>dZ!O;v)My|7{Z`fKBVO}_Vm4Yg81?z&+R+Y0UBd<dg2X0Z5|Q}6B;AvMx*$gW!HkgV7bySGjbEdTBl+uqYTYX}jt-gPI?`?bs1pcidrShyV%LXnQsl(pY5o2cbMOooCzMi>1a^-Hl)f?g$qkwb>g!8?btz8~P~^=Dsy_7C{8I)F98)QKbSFod5%PUkj&5`^U2cQ+m^bLTXCrRX&pcuHRYGP8&(Ac%)bIqfG=^<GDoUGTx!{CIu$*QjITZhQkR5Tn>=sCIoR4$*WhdMF0%;IuKw9hsmDNa2IN>)6v<y+KDt)oxIxBbCD;0AD#+cKbED9h7~<Qy%pFFQThv`o4*Qu46EBjt0HYz#A$N=JtnMn$)Y=@cOg8AkledIX!=G{kYv*W9l3e9~X{k^=!m^{B(DH|HJ0)?r*@7DIrX0hr+i*8s>61+{79fG-B~^1T^XeK`86)G|b336ji-TV`QNUJRQr#np!7QtjR-|IH=OKK6VegD?R@?4QJcl$dgTr$*%)Lon79^d<2TCAnLdE@l!La79o0iYG@_I+TL=6@FsAzou8|~gh!*}y#}_vR+#L<!H&*5?V7WP!tp7@%Mu%b7%J#^Rh((+t7l+L<yv8A#pDvazrDSAOpAf0)$@NoPtce1@!d(;*4z8@xVOf~($T4zgN!0Eh_f;u>gZOG4c^09vDfl$B1BLQ#*!}u_7BKZ8f_?)ril3=T6|2suO%3&iyo%?E`98%Hu{+&WfFSZJeBdzO_U$uH4(t3^Kh)!M1(R<I8%p-1>L*A=zKff=;)iD7L{$lh8aESg91*S7C@e-&eRxRz$clRx5u)gF3fD%MJZwj%&!HG*{yP`3}&<1rkY5n(wty9^flvLcwh<2>;;*qK^wr;%&s~e$xwXlY=DA~+gm>PB8MB)vxH4H%;wEgw>|4Yy3=X4UQ7d1;06Ys?V?Tw5(wu1I?1+Xr1D*0iex({xu-pr1=~S1`Bcv}XZfx63WR^qX&lc6G9`e4G1G5g;$O6ZVK5bO8;f9M7%s*=W%f<Q*Z|f+6QXUh;jIyGJ0Ds)r{e#W$d>FK?L%qA+r>@BlDwQH3Io))JD(=ELEHbc&O0`&v}^27ijGnX@&ed5fZW;t*U~&dItsvz+ZOiamdNShUmo7Q|Fem~0{dD|9IwH?fFq*$Dg8{r#T)E)G+^-7hWP3I&0h{(D(G+_D*=9ug~NC6I<o6^mP1Lq>lImbx+Umx^a3Xgl8S&a7&#Zst*tOTIUZGqCv<4O;%Vx?o}SBW3xM?zyf0fUt+jgK)|1Q#Wh)5;jq3(K23kYN;gFqMMRQ7aQ7PeCT|AmsSpvW{Mn~(|?+top^I!sDA2Qjx62RalVJ@x$7CS{|TH7^=a{zCMIYF5AY1&D|RcHqiwVt@nFizG(4pq?S(<D~Y=ni;u3Yeu}Y64@H3@zFQU^8`F!6;_I_2)nnrz@|e8CUFN&{auls+H?&K575Fl2)+StBc<qGL^IQkhKiixr++xhrKr^TOa(Alsh9dayRQ<LnM!;kPZpvc!(1<K7(?|!)s&y@Qvw?86GmE&#Ag@S<HZG+3uwkum~Xeo+e{8P=cYg&vb8^aCp5CXHM}R;!%^}pG694e4#T57QnWKnps(tg&Lg12>|ikDnS7i<T+Qcne=buHwm!96V+^mS0J*mD<BAe;{1~XO5DoG=WTkJxMPVj292*3T5hEYIQSUNh-k?golZJ;#QEqF|B?%1s7KR%3|E2$5NGHH(e#Kh*GHuy5iu5vWD!`}vp(1+p=L~CHDcUc^SE?g7V%a2szbDn*w#a9xzIL{^t*inakeC_7N*)#$I+R?NBps|b~I^LZPbRe3YpEv85-WK`oVK-*GSSfxweJ*zV3?qimd_`>$lLX*M&7;cj{QdG5!4RAp0@g`AT$L3_|PCapK4y!0o;(uX*sYmAo#cumr&ai$`4Xbt?=qJuI%f=TVmgp++ykp9R7t=MRS!%Nhh!gE4!Tgh$1`cx~1}+%ucJR2hmUg?7#~9j@t1#ISp(fHZdzNrDHCYy(gNW!nMxcd;<;0Q}0f-SB%zjg!~!0?oZNZUl|mAaP8=7R*QX@<HdHveBe|Gf4rAQmS!l*C^7VcL2Q|?_$QeC9qYg2Ny9ra`9l$0MJqbP1W!&35v~orb94Pxh~l#J7(OpCS)xA=Jn;^N0a`6oZU%vJkmzcJN^gc+DGKb!@ew6fn?Ppt{1a7H?qys)~UH#G-Vif;mw1dLBz>K6jFtJEihqZ$)T0SyV4=@$tIvmy6w^YLc<&t<4kQzT@R6mi9#CCG|wWO<Y**SodL8g1SMOq)Eq0}(SuuLlp&YkfHp@$$X_<%B_r7R%d;vv!XcAy1u2PY3|mg|(J2sn^qyv$gB|NR{Q31%<XQtKPry$kKR?UCo{m&SUa0k_s~}2|%MpCs+Dg-&>Pf!JvQtx47}+-MhK$@@S!pd4USQb;)KoB(^}NuSyxgeIN$A58)5BBdY1RvKsc1u}lU<|hGJUR=;KNcTD9IgYX$)B+0Cz;PER=L|<OL#417nd<r-LmVPUz@dIH1LBrN<n8O??v%_U1T?s@=o;el!*BXRnfr?SySdd#k#v2sbN93{jew)<23|^C04MD)mXB!{qCo6XALnRCNbos7FgO3X4T`EHdMiO7{b6G0!xMv0{773D=L~p@L#v0$dEg=<L<X@~7+$I_n0uOHNl)YQ6e1;}->D)h6)3OL)r5t|Jc+>U^-)hz$bm0Ut>#ZvYT966<kMq2t3o0RMsF!9*8tIs@x&HP+qHtS7tFX(tTf%^MHXTiOG<%?wFlktCR_$s*ggV!J5zlQ9&h2}2JxA3JNMKJE+z<(NZ-U8RIasDamt3MLq+8oNDzs8Ho=X-<gfkABDz8esAaEKy5U6)@xqNzMkqS~$=ki*UAa@|uVrPvKEAwg^{6Nb=N~93muzM!Fq7N)V`oRHVe9JeOx2T@Vb?1ny8TOJ|&z<BPe1_*1?^=19j-OpXaqBo2F2s1J)7iTmT+KuJU)5H36eI<DR*YV4XV6TYE!<wH#alb3KymJve}x%Zl_`k1@sua~%J5?Y=bK?C5=vO}&=C&jW{!eJ$Mi5<g1qsxn(!uKXPQylQq-g3zrO-lc^zeon-3X8>*>i3wm4akj`Url0T1mN&uL=$FzbLatN3_CIhKF6f>8TwTyTA!`KPlz|yD@_j*k1|CLN_8-EMm#90zgm<s6BY2H6VqZe5=pX!?S*Q}PP<A}xeIEZ6bc*B{5=MV=p-A?z3C(er74E$xVD#Mu_T(sf^OF<8(?;U`}W7`VUUBZineT#jTzB8EA5I61><s2v^0}s&p5%u%1@_BvK+*qCZ|!`j5P{XcVK7_vW-*et_q|m0xRlfFAbdLFH887%AwkfsT(2Q9(2`>8Zt2uu6W^6)<UgVlh`EMHnDJZk!Zw<+#ydKwM&8&i~)6pa@EfQn5jjRDePV2Aozq75m(TQg1mrQrqP(1zkk)Z^$`NF`rbGL1-C3f=CkbmPEW}RD#G;8v89DuJKEI9=<ZJ;;wbwiy1IoP4KK`jF;ypyNA`QfZl&F<I0+1q^!deMeUImVW+@*-y&GLL*H+r7)dobBLaY>?+K!{<>*3VY>SHTX6529N<RZFcAymQF$`ph5?x|PV0QU*Yh;E7?jZ)KE1;l>QORsoIGT|zLkqv&JG~~eHk-YC>d29}LvP7I5T-2Nu7_MhNe&xk9X@sT};N7QUXo~-%RjW}#(F16cN=ixMif@kN-$dTbIre+Lb^iw0QQt&_5@C;G5U(Qxo<%3sq-3yvsKMs4q16zi@|*|`j*z}rIMF(&tc%PE40fIrUerjF)>7JG-Cq*NPA944iSSI998mAtxX|Q)q_&kLEvKjzwP&+_SJR_F=fSfObl=Qb6(6<gj&xSit>=q@T^O?bZ4!v3@xc@^Thl^cWr85#{%6~45bABH4v4LyxHxmjx^n7@T8M%cR!|X?rIS%lb7tL<XDLO6c9S)4<!gC$<cVHm-iLE%(NEim+)B~m=E)-^`N2Xym(E(_+1U~=xlg@w>D&*{{S64z8!xH5a6EzDtla9r34$S!XKB=O&@^2LbYLDX!W)cIpN44hqTZ~9MaM2)hK68u((vnyfZsP|YXMgg0Umz5X$z61&>4M#WOYTLPoq$Xn@IpANA^$2S{jzl-&9{hq@cb|jzPN)etRm|xQ=N3tH#$l{Ae->Wt<63%{N2eFDU&1zkt&LSTb)X%@!y$)g=PB&*(7&0kBXB-BMz{3&kO8P>t56Ev3+c1-OwsZ7qa5?`N@QT>(K2d8(a=WBZW6qKU~+QC4Uk_?;f*%+}J-(^biB`55N&DUY)Ko<g16>o|;^>Es_KpJ_C1rfPkW=36uKd-o#_^j8#q)gd)!leU&J0V#AL;loMJt}a`NMzdY{p%x{s3&LMp*8v`{JcLb)19b}|QpX1!8?;tI=;_(*VqT{_UP(@W8flIvPfN4jy*4<(`U<|R9x7Wi)09ZQNS1y~78Z!zQtcL&%|Q|kY-NL|z>^}}-@8JR6s>4_#`OU0e?`_5@>yi2kJaYosB#Gr1>`F5b7z&wUs)l96#~t17QFi!oDjwa6`W<5rG8eW^LaVy_c9{{+%D{%>?F^l(5PjuM*Ts^T7Rzls8n^}e#?HuGrG1Ek$rfgO@BiP%hM7FYOPhH{G*fW-IaIBY6@_OAahM<&B0DA0XU8AaLa;`eQ5)50j-TP3BZdK3bCbBgnEU#wPRc|?nqK`Akk{}2~SrJsiR%yVR^iZd9NgAyR2E2m|KgBl2#jI+^F(~sy=_Hdn8t()RgT@#geI?5ZmEnLiQ{Lfo>_`@;_XYne<zs_Mt)?A^9a-dW@aQjJv}sB-ZL8*6Kx2%!lGY3SnVLVaky#uM{13aSo6ROVAieVK1XyiDWAo^f(hCg9KoeN+j`m>{LR8<+B<azglZWCG7dRN`t$o@+D}<mcVNSaN8Yak6eT^S3s2sUzp{ITWN!U8V`0W4+dzOPiFDck!yK1tjeguC7FO^FkAXn^^u`xNs=h79CT#J%tLLeQgc8PqLG3uay=NTRuoqtS`>A(O<_OOilUB@h?G3|BV}Symrsu|ODFnRPf(-P7#fMbx+6=B9^)1&Nm%Wk3!<ae8rL$2>phb)vUHtWt<oT1ry0|wC#ST*n@s)Inwv1%B2JB{Ipn2l0n;`Tg^_{S(lpJD)RkbQl6?k_O4WX)>5-f;fjbvxq%N$KmUew&PhMp0jGeEgFkgfo0B$sx%0u(&1%C;w=sqVyxbuK7CD;98E|gpwal}<{)y()=xf%fB@k)g#+4T>}=(_{$_;VdgfHakYwHzO|ln;+;_RV+i|J-foT-7s9#FFLgxZ<Z;+jk=)>XJ>c2qwfwn=++}PRzcu+sR~Q-+ICTR~=+2jpilPAubn^c^sWmzt6;!v38U5l-~^xb13<Nxp;1u6}c39&a2W;FmTM%5za3q@7_%jrVCW~sJMK45zZ-^`4s;+fHRk2knOCo4ouakE(`fPLqBcq;Ovv*^98M(G*Pt3Q#~uP1u>~5v%N)*;dttxhi`)8_Zwsg77Ov-Z(K*Iq8CbYfnxF&3&rEG^)QL)DhH5tVk4R8v2hJtMpMj~U>@>9QtN{DPs+kz2cjg&jj)W2oIwr3*Fm-P)u`U{0l9a@a@(|eHnb~Eu(ja1XX%?PM>-WO(Q49Y>OYapio$C$0tixozM#8gi21N;UZ?>{*f`_R34`t|D0VWVA;pV`0b5-DMit%5aa$NiCLkUKbi~``ShGTpHx@Jyojd7CC~sbz6$(V)4Imie^{H9*;pFLEM{=#z!>TUJqwF1~37yrRODaVL8A4OlW;fK`R=SxNu<c}fo7QFw50Z$1G>`pIr^N-N`_e5d6~0I@R+r_lO-IE~z85EE<4#&i#QDx-m~S-}9lHqN<3C~{s6(l&<*|^v*3AP(+Pu+c;fIAk2}RlZATt-sW0K62+LhO8Ai-82laY&hSZd{!nmGZoNEreun^dhBRV%~7&%4Z_)@9<wj&<s7aS3?Jx!L5fObGx(D#_|{p7aZIo&eLv#%7rLap|0qt;r-M&?cU+UhKL9{z?;Z^~wo)5Q4in<KRnT;xkHNBpDJ_sM=UHe8Sjv%@HHn&3wS~GF!k%bhpu35xj<yLps4&cSU(bJQ9Es3@FOCkYJcxPL5;cC62p7<z)I+sG^gI-ZRml&@wQNzBg9(Sd#hX0x?*0Pv^Rw)$+hHJc$aB6COo)(eY!gB9xXu!f2P^Z^l&pY$A;I>-o9?huaJ_<)eOS)uGlXPTH}>r%)X93ri4#SHsLS?Xndnv60ObR=R0{^pr%FRsc7mjHl1eRaj>`N2n<IS0==Z*tiNWMhTz--_FLUfDqDlmHc7r_yPE>uP?{0@AqQasH!A&Vr7(pnwP8V7kweCSyC?4UP?ACa+m7A3?^2PgUZc5FA0^)Rp;5-84xz)wiuInn$2)<S|oW|Pi?D#5qf5zm6m!h7Ej6!83$epb2EJBk<|&Trs5|zL0}bz3wTyUt+FXKT1>JyS;oT52haO)fr;Qjgsy}o0-kJ|FHYyk)O2teHVfsz)yfsNYZ>tDcxTaB9eA<D%?U+NM1+f#Jfx-E>BVD3tp;UF7WS@Dk2ENAyw!-Ei_#?eO2y(~2k~%gmoJ@NUN9RHDqSYIaNju?mwmbGGS!{IBAV=2rQYYd)H|6gOHV2>jlJ{u!i#n_LO@K)Wt0TskO@{k$k#P1E2FWBvkF&lbCO*SkO)h6>FLNSAv7Z7)o-qp3$M`=`L@g1b~1ap;=5KCs)*>dhYGT<c=6KC;*L=&!w8}xZ?DKfVz<xW6URnB4?N>VTfy-%vR<OI;5*moBX?cFex0}QJp2$YME%eC7VBs4wb^o#UNb4B78l|h&gC--8SsOQ=GPV3ds&m5tX!SSN7%<TQXgZnONeGdcOR3VON{U=cam2m^@ZM;ZEghc5l-8#W}dl5H>FEFS{U#v6N}etjvx+#>Nk1?wp|(=(~2h*f@$79Bb6j|Z;ebON3u#=f?OP*Mxjd-tMeL_$CL*U8KsH>zAA$_z4pa@27{8!kYy(^7xpo8;*uh3SEX`#h^(wtiV!O}aHHNPZM3V9vqpBSZmW6~;qp1MZ61JWs$W$zpOLS&1MsEWcel})hy-;fP>y`G^O2oSq7hm9QwjmsFHIRGml0FvO+E<Eb0t?%&`Jy>>OTaD5fiahDXsHrGBT@@D-}@iYsrRa|51hT$U!Z!T*PA<9s1i-aR~HFq+CU1JXSVB;~8qYf5G$%R8x}rxQ@<%j-^4tNc6OwP>nUq%}co8`r;zV0^sMqm>9;_z9PRcNaA*>?th!6`8<5*4Mw?UM4#`3z4>&f9+keCh000LrI76sOCA>3ovP}eRo;Ns>|L8Vn1a8ogL4)Qv{<0TL0y&AHMW#U?$GoCgRMI~eqH8ZR%d+`1*&qCsI}@;a2b+^0^c#0SUES2z^v&$?935^TG<;VHcb|#O4Co)Y+iloIsDstgrZk**~flt&8Ze7r4>-Kxjl?;uY;u$S9%wR;YuM2u8mb51n4h>G(Sq*b>YcKFNvVd7sfgd1xw_@2m+Eh1pOx{7wZIu^YM)EGGl!qfU~~-#5!CnCz;5cqnJS+vq+4flv<vX5y<mdl{89Eg9PTD;67hYqN=;@Vb60o+ckLUu%Qz^r34rnhG!RuW~@1$cEXTwohChuOQ(SYjN2@71!Fp-$o2Q@3oI?eWnB&nXgqK2(#vv@_<T#zfOTKk4&W2GsYLy;ss1u#zSqSFa!~~qgt^eR-S)Mk>WP<`a8a)j0)(&%*yjZP#km}D?5|FRUXPD)b#XVtNjoM0x<as~`Qfqnn3hi17)~jpW?uN3(`|&Mo!5djmlVxN@*EjFVChY9h3tazVg^h&$%`d~=CYJLpyvL|3?iayP&`F?v>?P7L06`Kr`VR1Fl~uUw8Makb?P-?%W>&dX-THod0W3YkasF%Yz~~l(;h`k8W&>%IDxtntJs_x*UPIu1&YIVD5PxUCC(~hj;zT8wpY4Pnr#=4JkFkAuJOjc&?F6aR@<7()S1O;6%EUBZBioEN%Mon9KMktE0tLT{)b%)sofMtSoo}>szWMMQCvGOk1#}+lDWJf52EGkYn3#(Vw9Y7u&nQb!kr$~URA5Ej}fShFMOeBY7p)s)T_3KD(R)|%&PBF=g^r}ewLuaQV-42s=Q+GMwe2wD6XzN*jarWQC(B7P)J<mxsHbQW*x}>k6qhFF&7FeP+_Q2@g!j8GWz~@(h@b{-V=Q}NGNg%?!b%x2Z_%|6ohoWWYmQ*nvm79wy{LQu!6jKfZu6+2DX%(IFDso$9wQ{iuD#WZB$i;wr8d3G^*a3zPSwKsz&_-o{}gRkE#}=Dvm3I`Xy2Pcxg^>Wbt^p8ZEpW#NLD1<sMBm!SY*$hEhcng@*@H@ieqet9U}9Dyu%6o0Phy@;B+6=_h+u*0(Gp$Cz|{o>B>Y$7jFlqnG6;sg@@ru$9UiqFC3RWcG0`P)wa6J7pO%$@)r^WbB>L+i{dvY_6HASVzQts9Xsx>L@XiiaGyhW$G1!tf@AiR5+lPZ&!<JStU_L`4a|J7?rawZGO$dsXl6hT$HL>%#nQ4kt9o8r3UmN>7ZhggS6+;^?2HW`WqE&_0>zskx$bjGG6=0kp4o}5KFfjiLE<$K7tsxl9(_pD#l<nO1KV#)nk|ueYCYVl!L#e&@H>kZTe>X`c;Ley!V#@=)^o<w9JHLg!P!xEl&1s4%9`)HOkw%tmY>y`uJZKSXPmiQ>9*(%R#)bq5Y8AMQ*b1g%M>`mT-R|4MV7IqcTgeK~@6=b>T_P?dAhgWW2080YjZ)s+4Z7a^0>5A&DthL5mJE>V_136hJC3r<WD@NaB@R4cqj%)CGb<%ZJ7s6l7A>h5@RWG3#MaZR-|D$lwrKJe^ki?5t|Zn4U@UCMyoqz{NA8*eWHev^v?ZXnciA?mTt4k~n)W5I8||fXUR_g;q37Nu|i@dud>&lSbi`4cR@2KuDzg$lZmy9Ihk#m{;M}Fc7Ab+eLz`CUeruhld`y(`IV@9;r}nlny{t7jg;1A=<vwuqBRemWiqA7(W6$BW8q<&(dNu>`0aM0wWOJ>D)e7vTwc7Vt&*-A3#1oT8ZLBRu_~*Ily0It+hXr99|QA{AP<8b2kV!$tqltu%3$bMP)3=NvusGE|!v=7QR-%bw*38jG2-`YgVF=giMO1cWF$)s5VumWdW_N){UnQ7q+|y!GBk^LdarqjQk`CKN>}pQ_30x?~jyjiI)GdW<;sBP0MaGci}z{4R<adozW)b|49OVeQJuUvVTLUN#ws2ij!K2Q}>*cZAn>XQk6n!@l**&#LL$}tVG7Fcf8wOz}bW}J^(oo0jGgz8j8Bh!>d@pDrjJGq>{9Snibu8TyDu(tqQH8iZW76-q1ZED=!yhtZf)Eb(vFkC_gPToIEXx?(Lyf7dNU#*@e5!+)S1l-x7EjZAamBmEl)sT`^IFHqo+8evb>-4b6%bYeX>VYD5hiR7`nL&14%VdXDQylx-k*x;%^Oy8@K^vI}(qeBAFV%h6ELmLldg!7O_ERf#B><pjNkm2+H<$Og=AF(~}u!7>tKgqhn$2GIPMt-`BR>pZdVX|TOggf{_GGptps_$cMvf_sCBm(eRFtE2}_jRKC5+p87@+FC~H%!$s3e1n$iz)?_M3jTnGTFqlbev!nUMCv>TZ(-JwOaUcZ|GGHO5>J-qin3{L&cuOhFbmX+vQj46;!bpS@N?l9?l)WQ{BZs8W9W-K{ohQ`eET6Y<ab}1xWA7db+!#Qq<!ErTt{jfY0rMl_Q+Dy3h=ELXc(U1wzac|7id}G;k8vqYSkPvqS1^sW<bD*wpvoKk3*4Ed@a<I5MNAbXEf%Xad2~QfQMO9bCHTkm0V_q1ZmlJd8d)gnU)RCm~n#Z#c%zLTb&Gi?p`G;{GJ@~l37k(-JV!T{0-eVaIw$K4C}>cHi2!>S~BEp%zF#{2J(*ZcC}s$H!$lgF`=v%@BX%ZYi>6Tf2C*`_Pi7rYPD<Du)y1nwhz&Fim#Nq8Ll+zrTbXT-R+0$1<@x&hi8q7+*SM^RGNxxv3x8DMAx1eOrDPnM*2$HQC>{U=<4&_PE+ff+1`CZ9%f%w<1gEJf0Ng4Jd(|QI5rRe3!QmfDg')).decode('utf-8'))
_LEGACY_ACTIONS_10C4S_3Q = json.loads(zlib.decompress(base64.b85decode('c-rk<O>ZMva{Mnk>mX93K77-3bKQ;Aj2cq+66=957{F^7FxH2$Z-)Q7dnK}1RWC9!GV@W=jCEsE?5g+uG9x1+fBv77fBW^fzyIyGlYjd8<cDvcZ$JL><>uk*xBJb><LSx2|N5W*`d{Dw^8MrAfBo%0{`TMBKmUC4>GRWHwGTgh`|B?^KYjl3=Jw?D<ip+e<aF75{qSkC`7-*$!)EjG``6n~o13pEr<b#@f85;O{d97=7=Hfc{_f+q4_^=e<Kpr0e^199`||n2pTB)MylFA&+s`N4&BNEHw*GW?|Mk<;r{SyFhv`5(Y;JE4Z#|#Cb^o~0t3X4>uRVO4PX%hg>~-es!5$7Rd76{Oq_4YQk#~K$z4@@Q#uN2t{~y5HX6+_#-TjyGcsA{L`tGO0Vwm)GH&e#X+!5Z~%-?@l9yeb%_wz+G|8BZ^;L=^r7tzDrxA`J!7w4b;u`?#$%zDSBvK^f10MAD0(7z8iyQR7R(eut6bv-nfhv8~px*vt{uiWVZ`wvYH*a^)FCU4n|Js7jma5OX4{zjj%-MG`Cn>=^E^A1DUPLr`N7sBBNHiLPz^0Q^q1#M)}q2o{9zNPwD%HR0&2!?QX!hkvQ=1m{O;T^+=?`Q7=`Vbqq!?;%-y!$1c^uEuh6W*l*`~N$7Q`hIZA70_Hvs>lduqK_uG;o3RdFuRZjcnf+Z^7IiAwO-*h(0a&aCdvV`SA6ZKW*;6e!l(uFVi!j)8M6F5?CVXcN}RB_P6$^J?0)79Ff_NjjMe97_b1}^!g9X@4Szzym#x`e?^-Fn0Jl&I5NV)!p-;@z!-sh0{3dSv_obx@58vaULV~71de^cAZ4x!{Nz25jRpGTK9G3?qWxI#N9`sj9VmNHCEHioK-4$)=bv~wHP=@Gp4`VlZ#m#R0OS7f$krJ2H-8J95ZlskU+8hJsY-CO7dEWlpVt3r^1TmisFezG=M4kfR%j3BDU80D!Q$Ufz56?a)JVr6yK1FFGGjjsZyg<2@w-!Od!=)sAw<Y}=}w^cYsuK47j0%(xE*6ckrAiKYk$COqLv3S84~swUGxXk&&5UwdgTm;4;e-d-Z_-@#{sV1AN&5;-{E6*0IP?oV@KX$2;YUA)?om}2+6naZai4#&T05c(rXOhDYXEkXAxyUkQgczX+MdoR~=b)!5d@q>E`|~R>%6?_yM#)jAEmq8v2qPqVZT%C<g7|v@ytmOi%(+_@ECRdwy$d(2-F!49a+<d^iN)E0bk+Sfl$vIYd0=K|eeZT{YwPjSO@hgPC(Q=zRv>kclw24{m8v?`FgMW2+$1+OwQ?zq@+c?yWJk#>B@(#I)KOF%MtwZ?->d?(hE!ESVI-<aWq>JEUPQyTeVafkq=1k4HeGUJ!%|-JJn5at=jh?@}9C$O2EtGO@<i$rx*jAxs=pDXov;!*HehkJE6r{f#`@w3z(bG1OV|PUa(!Tm@FYLtj5PGiwo|PtOg_gjm~Kju74iu6E>c8JO^BbiDV#)@y~yE+W{`x@gy&KPHY(AztR#2*gl9$E)H@Q(xT!V=~tYLn}s?;P&qB_9-m}npV3%?k4E_`S|f9ZR;KUdEDE;*V56cnS+cX(TTG%A8PAXkPY7Htc2I{FcBgs2V=>X0{aJKD)lxLQd7kI5G_8Y-q#WgRicOKzDtcA)kZ&Eq)b9@n@?%Hb7SR4#F_|T(|I^H)<lFdjyO}(#DelJ2z0)kZglj`Pm9bpV8e_)>4O4Jofbfzr_SUUU%)4snYYKXqAr5jvWry2ZW<d~`IZ;VSPh$FB4tW*bmj2Yj8_o@L{RoF$Tl_F0Ipwlo#|+W;!k@6WPIJ;<i-y<q+pyE=aI>V8M}UZcFaPM?roZpXH&ftNPz)lLu4s{_JR4oaWbkIaeN3qk&I?1zqDdKupLAbO!a(nmctref$%>R4PcX9e(J;{TU5}$Wr+{L_FKDNdf8@e$a%i9;0J%CnLRP|0vG_Mtq~gMw#)3fX8&R)4+XhN2b;h%$imGmZRM40G!TrNJm-`afH6;;ZIN*{U~4e^nL`!~sLu6_4?j!k-#=1mNd~W`JOVl4`xSD*`yjcCun$sa0bXNoBP5VBCKR?d0sL9W^GKv`fZMfZuyxAy8?LM|8f=;Vz^Eh69F;%PghDtmmD{hFrIgL{2)G8|x*R5WZ}9&3`S#Ddm1p@$?JxaIzY0jc+tSbPTZqtsgshL_HLK_pgGCpH6*zcXar(f^hLs4mydZ89%FhXgp@h`aW6Dv1Bl}>ckB#95C~2*E4vl0IdWZ`%K1zJjshArT8q0GZFm2s7B!MNaMSOVHoHH=jEo#)B<478)m0xR((qzoFrOmQShVK>ILiZ`SF`OB^Q~S#NTh2L=9N)x;Y{I$c8kxRXuhx-mKxZ%J(dzACD;``}tz*@9c;K{9XvLjK;uLmXX6*}FNN4Vf$2{eNv#0@2ard#N!*)2a$zfh;Rh2gek^0{4ky6d-0YQVG4Pu08M_2H|SJsI_ey1r^9m72bW{2mU6MAkevZ*`kuDi;t7%@ZA&z1BoewasutxVaI4W$lNk}#Pc->%|A2&?^(o=T~cb#$HOXExXhuOyIGD8W3`d#GX%LyPk)s`2$Q9R&sKp}uf9s!P<rca4fT%5t&@+WML<NFX)@_-2h?3>tzQQb$^(wR$r=KIg?!<er2!i5f?q3I$G`CT@;~7VJ!03!6Q)>OpJ63iY*H>o`F-6G-AL?-VA?gkmufDHV{ULVN|tsz?OE6uUVgo%RymhBBE)`cRz47id-f)Oibo2u!fI(5&~tdf%SMK_+CMKkfU1Iw)@@Y~HqwhRubLb<EdA-O%k_C4w%ulEpzX0i?^vn$U4FHw&2lD#sxQs;8XL7(<-;P#HcOAV1QW6A#y+hm>^#AgjW*$xoHUpmIT;)+c6IH*GD$q;hk~{o3(c#8_)JQ;R>Eoj17I*1~kL+v|YG>*T01axap|B+Jc!(R~|>xVva8IvWU&HB2xB?OmKbCfKtK-D`gY@P)%yFzAk(dew#~R{kYLqo?qcVkpE$5s{FazcvBO#lm0nY#q6>uXtV<jwko(;xQBcC(szktlD$k#?=}7t**&qozAuUWs-?Wnn_bv31N?fplJ`hd0W`4aUIxa(ml>chD#21?)G_Lr;%9!Q`ZKnJ#!uo3&>)YJG_4EC?-X-r64+NR&zvi*oL@s>hiXT(ka(6LhLYFbw+A4AP;QZ>%>|MO)>#$vz>G8uc1_ja^Qx9^QK2VN`^o?X+)(axzdA%Nj5)vB7B$5Ti~e7>*g@Dv`yW8b{%xnm+Zuy01;ZDo^c4vhz9-z{N^em9MT5zAeFiM3{`b-4rvmw=rZ~;Q~qmmrs~(Ex$1KXH;i)R4LnOSOjYBMvRd0XbewO)ZHpOOGDANA4&u-OZ&)?TG`p)S8CcdJYy?JpeL<M#j%Gz@g~WIs0_Ycdh^tyzS~i3YL9=Gw;)-E5G2O!^VkTEkSOic5rh3E;;=rQtwNCBS45@>RF4*=9FIf-Qf)p9HxGZ5ZhkHzLZMOr8zKZb>eq>~QhnQ%YqCn=OA*6R@`7&+&T8oNx&(EvM3Zl4+Mr$f9%n)8F%ScikmwnSPKQ`v!JB$Uy+{e@Q${j4JTI(l@ILxu0Bw3?{R?R_>z&stPtichvf^op+0M69KC3<2m!<XasTsaWU@i7>{cu<3-CIp<bLiMbaJVQprUKEXqvtW`6wU6VDI*9g%6bIS`kmMTGMV6~NPHY9~SO|!Ta^{X7JWMGhQ*8;g(xx1Kj(8uT(!qw8p3b6T)9z;9Fd~KP=haB}ipX~$X(eDtlRYmE4ci+nHKLf^!&qGvzgNfs4TumD4dIcuL%IU%*;Ug2F-OIYRN@@TSstG|XlhiD5uLOED;x6JDv)%TwKc%XKQL+)=9wsspB=M3;R)uM$DIg6a5Kq-W0g?3Td%JR+mF)~u?x6$+|d_MjKoMYfs;HKp~y{@mx4H4R2vez&M4I>$>5B8_l)!~?`W3^M=>*tTp<<DER0}h*Z#XhhP5hw7w-OxaV}bG9$FGo;((1&B)tCC7RmAoqJj@qd3H6U0-0hmp&}QB1QvhN-*=s?%w!aSA|^FK{jPWsP(2E%sa@zkt1SqZ1oholxBQH)<X|vbq3#eOh^|d+ay!Afofgp)$OspuASmxksx2Q;JegiL2}KA;P(hMyk?5sCIx<@xJdPjJig4SydQ23SrzgJ{y=1#z^J&?kKtUJE@t`SFY5!Z&191ZCY%!RrCIa#ynAut$9$gH4p=a9~q*t|Gg6fLLUG1gdVzup|ZdLoC)mrS(Q0iF|QAbItu!n273}hc98To8rMGrBbX~3plsp;S^oi0O6#!*_l`nu`S+-i<SOo+6$B63i|_1j|!@XQQ!^LK;<Fmeq9^BYW~R1+0AcAlLNgB}GJdK(Pf*9$?E@*0vpyk4E6Ec8H}b;>B$N6Uz3pUQj<ma7o1<DtM#Ds5nqDg(pNhCK(p#Y=~8Lc@IVSjkU`d1;|t3z9W7wtb+$1DOq}>VUCMrZbVD8ni=x7>?=Fh3t+T_+{7M%Q)Z}Zi=LHQ!9k6rU8j^nVG3(8X<5YIb?)P<{&NS=ZVo!AW;N3mbnvMN_z@Ryqt%kZ@N~GNIllrT}r7_N1LZWv{^+QeCjRRjGGu-_N<${SQ&o6Wd!Qs9KArgL^$0*qEG<9i@9tsmtfxnb>C?0_Ogpt_M)NNSWU1(F8mRKxXFruF;2F^X7Pp=JI&NKC=#_nq%O~hcXY&ff_sss-L95twZdoBjeys!r|UD}lhM120U&v82MP#Cb+9XhQe=-%{Zvns&KreNu_<4eq18j9eh8(>R`&pi_~>~DF6b4mxTwo_Q5#;<f^s5FStC+Wz!Rgc()e`=#Y%FDv4M7Y;B`tgSsf9vOeYFUIn`ZPhoou{@__iG)PcV&QlxpV7?XaqBfvtVPs_fF<`C29Kl2Qu9{qK(?bMQ_NJyGeeVt~j$9h5nk%$d7?)b;g{~YPjV%fXxm@WQXDtM&0c41v!))Mo(vL0EK&8vi2gU*bkt9Wqm+o^2+G<<{CYv-jnZ?;oSaoi@rPDiwhjYmv~#Fy6U4r`I3?rHRJEMgM9$3S!@5bXl%Ce9>g7sk$5zSTf{j;>z{$#X4p)9~&WiTBcNH(_bOD)HW}Gal5iJx(w_UWhVT_pl_jKs~*q)Y@q6Pp=4Rh?1OS$Ft~==WBN=-{CDNU;#_%<H@{rje5=NMQ(bOH)n1m2CW=!gFYp+pEF733*Wvccl7X(T2ea8-_pcJlF9;7&=)PBF#iGdf+`HKt<AmqQk)#2mjSq!#)Q48B%#Gvq=fB4qEAUU;yRZr??JFk3^nXdU}^(`N_z<4T(ig=ehsAlEk??GQh<Ujo-jS`JmNu0fB=il1L&*|6(lAd$(1BbW<)nHoz;Y7$O`8@gnibfh%#nn{x7Jv+BW6QFcttu`&AhVz^{-g3bgihouUBJN;BI0f*xMgy@igx9|YX!QN*H%lk5U}e^)ASiscCN?sHbdtzBX*9X8Gg@Oi8~3gl6N^ldCy5nqi;9lFywS?@BE*6QePc>+$3FInLED2ix^%pL&Qs3YU8NnIGpcYvr4ZYXxcfd}%}WF0;orQoZF>L-OW|8>iLah1ueM|g%=fa>Ci6Xe!yizsXYCxis+Ii}-9rZig1?%8X7CrJx1NFWjFJ%&mqUW1B>qL)F)8lo5hPi$fPQ9dYEf_Eo^Uo`y*{GQQe5)FrtkH(<T3QTKzBa+Y{6cP1{BM&XLE_L{0hCa*fhjmf2n}e1rB-qQe+n$+FnlI4b%hse*g6D4O8;?Q5maIttp}wfs;pS;-nco5`LqlZDv{FkdWdJdA8RYuN6C6T$LyR;dl|O3i1QlMIu}WMu2BSi0W2A@#*OpBZq_;X<GM4bFQ@+r0W$ZIhuX*{#5{ceW%?A!OL0T2+(YYIS=$Tp66+#N&e1#&La%qT;WhRAj$}tzD6eX4OqUDAN2-;B!3ouAVFHb2~`OwtphGVUiB`yIk^6W_T(7_wjy;=}Z$izlNdm+&SnxMoa5vT{KR#Z%ssk9y7X?iIhV3~K+TraugBUZOU^N!<!s+!^eK`cOYiRTijI-+4E_+=pbh&N0VlTi69@rIK%qNehJ9%#A0=|+<^G7U=L%_gfxcTHAUN9ZcC3MlR0R2f{^-#klWDq2kvwdIWcFoI+Lv4s0|N<;+=MIeoj!shUKb@$6vA`6cnp0thuE3BB_HCKYFqLMmAJ$9}QqiT7;)@SuMsYWT2h};kWZrxe((t_sJ>27C*F_ny@Xz$J&SasF0Uzw_&%7^1t{%lf-W@$&S2Misq&bLtv#Nlgk`fQUaH9HbJBS90Sr$XUU5~-3LF8*k2wM9r=qOYD~bHR3Ypl~IzAg9u)80=K!621H*4^N=s2p2laF{Boc8FfbD6bJIZf;f>fYo~>*3Xn3?DrHG|TgWtNZE?<?#67%3k+1+a%q_Pgsoii+ga$*-<9M~wDZJ7faoTaHnkrd`EJbUQ7!^ly`$UJappV&Yt)YHc+zGLIW2W%RslN8EQp7N|iU^I6)s`NrVt1K5`xxB`8z>s&r}kxCnla$_i%Zj?(lc3$lqA*SJU3^ahM)nh+6-~2fS;IU<8((>x1|gVm#W2(%tBq9DIw*_Tb4Q<QD5Q7>h}NhlFaAlRwokHMOwg#$2T-79u|e_L$fOgRH35r5}>%%!~z`lSy$58WhAqYk%U-^pHvG`o=nAzAvvJ2-e{U`LjGExe#K;jv;spEQl9@l*^OhRX+A-G=Vt=>t0^Ni!~QP+2sM7*Sk)ibNbEoZi&O?mND@&yU!Z=qWoER}LV7)!&Lw|5=mwkvrSijWJCQ~25vN{3If+>_Q{T8)A<B`h4wS%v8+j3&9$$5u3`Hf!SSq(|ktiIWPY3<U(qLxotX+yiMoz++7WkBM52sC?|Encp<=9?qqS>?CEf2C}DH>JM#iIb7S%OD#e4Lc7S|&GTt{77+QPh&vn*0nTeu6lWzm^`A<NtEcR?FG5x?0j{l%%VjGtc`SpNg2e9@TLs>@jQbv|>(ML$WI@jw}`vr-y@0^)nL-!!4&H?<=jajcKEgv4e{y%Tn2TJ0m~^3~LIJRDqnU@UuomOT(4bhiQgF+dh+IA1a~|uOk&9CGjgyDOx=TKwhKnm4#%yzPi*K11xy?E6P=}D|;PBYzlIfXbZKpUEgSMQqGigIa!AaAHXDNRn!*U9-oxdyTG&}_X`(Gw4_y*X%tC<@o{Tb6U#<W0zioFYl*$81*;|fVo0Y;<~4>YZ5g)b(E{7>_}dcBCNng7s+t<2U!}M(4sjw=$=vXPX=&J4X%T%-s`sbIv7!R)iOIUG5l1#=zLi#<Oh0KAX`Boh;VQT9)LLMSsb;9e&}Faa_M~E+Wa1=8)Yzk(bWxFv6DT8al7tFG47RrJz}CSF=tYHC1!)CoCaXljivUxq$Pd!jE6)&Qtif2aU2+z6E-M8)Y$(fj1eD*u<|OUQlW}q#O+b9PS@KG-?$5dJ$LRf?H~t!bNvfb5?i!)*c&Fr*dk@0{*HH$@P_o9qHA~7X)U@4nNwA)na>5k&8Bpr$V;xoet6lQ4q64itAZcaBDyh9F1Im=Yn$%nKZ0hCNAFI4te-e~fYK`-RUV!w}p(L9x68N(0rz~+vS23akacsVm?qdeT%(x5No$#bp2MSgf4)B@4;q5L8iJHa4Fxn#_w^W$?jB3Ovi95Mjr*UrLgC}x3l4Pb(&_W$h2Jw`Lkeb7w!Bg?#M7z`ZJaG5WcKR`4Jo+Z?lw&%1uq5h(lOkn{wI$0*vVcD@KDe?PWeF0`Bm>>UVgwM^=fx#vGDpqop%trY)!%$>&?zqwha?=W6S50OL(nHCJ#Z~orCMiS(h)B~AZ5rgXH+XAF&uyC3@|sTQuju=Vq(4<i%`O8#KRW}wUpQpx|Z^F2|RRwBR=LhJb{8e=7c2|N^R1%jFND=#{_fXesL$Ux`$E_RjS)qhzl<xXx!;>m|zp!@S0X295?Zu3YIDbkBmN7c&9HBjO+SJH4<Z*TOF_(0YP%j54RqR3yNgayir0!ofDS-pV$|X#h*X|e^4@)6VC#K2yrVJ4vv~&9MXNcehlD8tU`DoOOzAR6Y90g6j#Y9>L9Dpi_$kb)~HJ?S+lx`RN-W&Wwai+S#}vIf@O$4ixh>#-I<<-2zNq=ZzG^g*2#1pm|kUdYd5A)_lxC8^`S^A355(V2WO32`yd>r)k<|O>{&buC=oKlM`f|$NzO^Or*u-Z+KZG*qnU!7NaF0fMQPtb1J-0mppLnPckwhUb7-;B!h&k;2Bmx~umtzKp<%rCUx+YWUo)uPi?ocInjOmPrTQfR!qPvh+{P5=Y|A1P>_i1OMyM>RV(@4Pi`aRdsI#>*l(sJQsz%#$a^6Cd4RikpYN(W`aPAnbN_Lvb4uMb(oKXeGD2%(^1Y~=23@;|!rIh?6=7Uy#JHysI%Mnkb^_ZJ01O_=bA<W%(G+&9hwlWH&{y!+(D1#ZTc?L3DhZ$pNt?*Z;=HpVV`IxElMa@O+iq^{kHdQl}L%0QaJw0yk@7s--#*)zhA|AaXEo-D%syw|Sjn2qx@lxv|l&UH#j*wg6k9e}GkELlR1<2^IZ%mrLC)(0Jk%z{k%^7t>#se7UR!f&H#}+&;B26Q7L%GT2DmNt}_W>zFu^}Z#mC+>1&Y@<JljG-m8anyVLn58g)LR)JKkh4dEW?0=4jn)zt4tp&T(HAplw~$FrK>rCAfKA$7uZnClSv^Fu__4C#c6ZNLS^#CHMdesnIN^Bf~{ixMwOcwrHIh0kh3Ux>as7&QkIr_c1k(RQsTIY-ODU87YY|aiD9j~RSw*>=L6ngq+H(FGEc-}dDna3fyXJpanZ~pWtm0OA9*&QE41hZCxo7L=|+hlwmhQ*vHeSzZ;CYbcB>sa$1dX`2C5yt2wyCshn{pZ^OP}{1C}d;7)T_OY`s1VuOlUChEh8U<qk7!D6Js*Ti|-p3s+NHL9wu9q?^}zjoJwDE2UsW*+CK3CtIEueW+dN26qu4+SP(Y%(6(`($NI&PI@w3M+#PkNL$>Hq=pyx3W2B@^4+RP-SRy~&+l<O0e$MON(Uz)YO#=jF(F{qO@OXb@iNu1(@0#-ebA;udYGF&kJlx>0HJS5vaDW;smc3N#5N_eR!+x|z*W5LAjrk#3A?<QiHbw4Q+Z)}o;5n6HmQVRQcue`T8>jiP%QJw!<(vNm2$HKe|V3YNbIAA+rj>q9oFbl16a(rq*)E}mUEIdG0)6BP_E3K7P=Qj?u!Hus)aV1mEbS|Wb)+V$cdXRO313AZWIBGi~|*g-x!6^5m%u{@m9lvb369*m_-OoQr5MGEUu1?EUpoDxTX}Qbv+$bCs#*!S?30~YW(L=?M3(mr3_<+nbopgT$GQZt}bl16{uG&k;U_<vt+GqieW6<M--hSE?Qari*WLE>W#<Jst)qZ2Nd*DWArUnVNO-L(EM*Cp<=H9ca?iHpu}lItC>SNS|YoH#%HRekyY#+5Waq&?_yO?HRihova~6eCR?eC%WZLvk+2>(A13F%hzSvXEl~mwk>MnX4!Ta6?oiPT;4V@&gi;{pLq?e{+i1?!dES&}hzu{;wvm`ROfj>NWWCJK9>>S{HkbAFN*TFX&1kVkCixleA6?v(JEpGHfKI=x3+mBeOnKE(38m?zod+TiG@pyY)r@E+qbO&od0}{Zf|^u>6r@f_7nD=p5}x8uc-}M8aP9-~DR^u2^mtkxz^~{66O~wV+An7>i2h83$H0lZw8Au(c<6sGiey&k`!$uy809Qhw37EO;fT1@RZTE5l9AT|cN3^9NvfK8+(oN#GG(%$-dYbiGPe@|Id_U!=3uyOLW@i%%sqicIi^(~<uH+M=7(q30f?HQBO%<tQx8+U2*DF=X&%c=sXwOt$fO@=kUdFuTb4^s%5<Ww2O$^fq~P#kpte+PC_Us6>^EJ<fT}OV^8*4LCB3dAbQ1z$_{2~vRSz_AGq1>>!hJ~a_!?iOr8jZthXsSx!jf)*#XuArU7H-}@C1UQbtD6=9^<XMWz#Yus7MWWPQ`37VPkSNo?$sT#2GO?FQ&$$^N*<nP$&&g16*|Jy6g-vJrEVOlzOMavMKsoYq!{yD7TU*qFpSJ9P+LnS7D+6fFe|MPziC?W&R@jWowJXj_?s0cOtDN=+<$?nid8xXt7YLTkaV{QhDq14DQlSmkt}*44sSDNkvql6;7dt4G|@byqKe(bfcMS&^KB=CRB`4tz>E;N6;|xT9N!aq45_bjg)#WZfp=8XK>!zqGYJQ4hcb&8Sq2p!TE39%t%2|%>@dO<%riyoma0_MwUTrtXS>$mIcJw(_XHk&%gn#fvI^7zR5!Vwk4e7Eji_kylLA?1Q6Xc6*Kk{t0{_{gM-N-9<ay+cUEczZAB$AdqBCEPNWu_ua};#;3D8gnvcLkV(jK-p0nhHE*=xwT3>D+9;P4s^3l1nZwiHH0`fF18$OKuFVt%IWu}F@2O+eCv@Y}^v+&wxfdT3Ap*mUzXYwsIt8Zg+t(sdpDSpGnCDqa~6ONkX@kwq>)JuftphOY~x~Z<QsKxP3Ie*E#a8G?-+Mw0|iL1qPq-mv~v?)W?!5xFgH8R;`%NkhL=^Z1Hw|A#*(dsXDcGd78XJD1XD!?2DT{b&cd@1Y&B&v3Ot!@xi-uv<X?#mG_C4z;5jML={U6m}UKzL)uxCy-yyr4ZZkN!&Jz4v`-d;F0*@g=)SUh2zolYTN082gnjO2zu=z>6FE>d5qTcZ_HshIh{XL=FukXEH68f=dp($U*Y>f8tM+hX')).decode('utf-8'))
_LEGACY_ACTIONS_8C6S_3Q = json.loads(zlib.decompress(base64.b85decode('c-rk<%WfRW5&RdPc~H-TL;A**dM(0SQJ^Rf*1}-1fY&f!tPgA74F9`javt4Xk&%&EHRN!ilLn(<cfBh!GBWbZf6o5)^KZZY^4r-TzMOsc`R4ZBPam&8J$%0J&o<|0fB*TPfBo0j|M~jy*Pnm;$1nf>`uWS*`<uuA)joXp`NyBGKivFqeS3C(_V#Xlc0Mb<{`9`@KMwxmQ{TV)`t|yKfBkTFzM6dfLw|es;q1KI|NP_q-Mi0k9}a(UvDy6heAuy%H*f#+`QzbD-Jow@&er{>hsU;lxVwLN|M+SD)#Sr?AU^fCw}-dRr*GXoZtyD5kl||&pQclR8ZddCIeV~&`<6V;NjK{2_E+RxA8)VU_SSf!{_Oq$ylv8M^49I249Bx*$K!V&4vS&b*X>LhKXXU8zn;GTusp6G`upi3ntnH4J#gvHri<v)-RJ2dDi`PX|KAy-ZzjECQ&|qqcz`FPbm-sP>+RCq{pe|D4!Rzi%foP$FWrs8@K^41f&GUj2keAm1(UaI#~zH?U^t2yD}STU*mm6M(2bru-Fb&0ET_p>mz{99fz4nZt^8~mbwL|hbm;h#w`-|Bmhw0LJc1$Io-kmJym`|HasQ6}hp%VvC-fmUaEEcPdGPj^bkf^CpH6s_4($GR@TR8Ebw9koV<)%D+^{B{!!&S#w0Y|EY>jN+XK%sO9w9$1%!oEEczbty+rNGI>HGfv;pX<{FXJ<z(cq<D5?CVXcN}RBcDMGRJ?0+TJ0g=G8&~;q6R-eJdi@9HciP8A-n(_}ze<|~n0JNwI55J&!p-;@z!-sh0{3dWv_obx@58XSULV~71de^cAZ4x!{Nz25jRpGTK9G3?qWxImkJ?R6I#BkYO17`Efv9ip&p+{W>Rew1cyb>Hz2$)O0F3*?BTHk@-~1(TLTpRFeWAy>rYgbBp4qVe_O$j-lka_CLoHO0J8u}+wnBM0k74v~0*ik=_3rNwQX?IQ?5dRx$&CH5f9v4Dir<}L+iN-(8bXAuSKSHpeyuV#=tY|u7H-FwP-Mhu^4cFTo2cbMOooI#Mi>17^>eXNf?hd;;X{UzgLevL{eFO}Z;$=<*jM;i9l&Z~>e!KY7{YfUr)3yGF+%d?y9*DNxpNx6lJpt_cuHLW(zA#%AV>_AinO0Z)oUGDcEKBC^Zxq&&sN9U-S`2tK#XFeq1yK)IYh&;sG%5?gHy&J_hf=9AcYV5zGF{sjSV_7s`i6294Q|T0r<*j*&WvCZcq*pPkGP}PefPE@O=XVUB_Ui91VJ(fj49#%;kein$$P5;oD<tL87H+Ic<M;`MBLnV`_<sk6pyH+8QyR9`3K#-}U$RKLSf8g)q4tGT#nqn6u_^6KkN+h;DNPH0l{asL<URFe9f>RQ4{lk%cVqbSx8VXq^nPrWnG+L6xfYvH!5Y(*4J2INR<<9&B1ner*`)tnyB#BamDLR=-1EKQ%LJ5u#5|4b6mD%Ug~R-UP08<Z&68@Mv_rZ-K3s3X@$#u%l(AT{GV#j!z+8=GX|tP(jD5;!IOt-2-DX*9t=`2AAOa?(X(6Ee4ua+yC57(AV?v-C5e!JNWasw}G#vqf;{n8AYNIXJtCn)~z5LyyIC3ujTzjh@c#dC9eeb56Dz%Z78Isi1{H}d`!KsB^auT9;W*)b?m4z`spHN5_(&FO5>fql^+pnB7jY&;n-Lc5z08=OpOx@s&_%4^W}7-qi=dzWVQhtX7ouP6maU40P-|-Cdc>!KFP$qJ(d-95zLnDQW3jxY;56MUNB=dY>tVPDb3N9!&?(xMGO!@*}EXy)Mx{^e%W=VqZNuj?G2Feb$OE;Kje^tabC<LlMOR={q*dZg&^JAG$YTZdMS_s1IYG~r2yIo=KtEssAk0Reej87G&}jFHP!>$K{UZs&nIU&tl<?1|De(UHreIpPCT+i1^ru=_z-NrmFuOIZB~Yyrz;D7@JE{26Z>8O1HiO3LgQR^nLXF+U(Dp8AUEk?5qJh!xS6G`ypoLuf^n1QoYDd?=83Z{GR_8U4Te8+$btdYxt{UiXDR)=M=CAJ;MJ5zASZmkKrVP2B)1FuAoVQ3E9`BA1agLi!qO&yKMQ#tiS!L{yVe<OjdK0=SJn^>woHFu)DdTn${%S$A)J`X?N`iF%I0|lTmx`j?k9L>@cwXf`={;7v;3s;mwu*S4M@J-(ogT}MCd?5)`#($MRbb6q6@<c9K5Y@`oPQfD-mpYLEI*kpA!s238|;Yl%oPi_Q6aa8p8!pQd;vI8p$N|5Eo{6l=!4mF*hnSmUAC4E!{RGfhDd*e0bJ5XJD>N)Tlhiku*>#zg8Nh$(U<Nn`M^_-z&C-?o)7MI5T*s_Lcd6Ip;)jd=nqC3Fn?`Wcp^UT1U14oxPYxtG9=(cyM8rj#b;?fzv{v6?Y<uQ`mT!l`kkEovAAx^OP%`MGbh0yN`7`Y=;w@9OgBxs^yJAq`q}~q*Sx|fS|$81~J04qbqpf3+qH7zta?|j^UmIv%~Yw2|YI!+0>nN*Ii{+jF=(m=Sun(Kg=V-R;KL9hEfM>k}#PcU#{Xq2&?>&o=T~cb#$HOCpOpuuOyIGD8W3`d#J@A_ASn{sD{_ecoY<{hx)?ds4h|e-Zm=YD9gzrXzOdbAc5Er;F}eGF=z;KNF8aB((29d_?#C@k$V!_Bx)RaDik<%inuu%TCg*1Eo}DGS`S(qR;aICTE_{xnLrX}d8aU8CKQW_NU4A%72+#ERz)HRrr6C1>9ptYHk8Rc(uc}ve1=x#Pn}a3L|}rQLbJXN*0=3>9ArZF`P05HsDpAcVe_(WG;A(}tYf||>V|IbDiL(Kl`IaD2_UUDbwbC<+$>=Fs~m?MsGf2{V+?WXLuL4Efc!{fPCQ(P9#X9v09h5bO@6K<22~g2DScvwb<@@|Oe!~*+^-$JMU1u9W@_<Av-1Ww+gg||c6$}@c%2+oM(#xtnPj;cFuHGJ5qB4DMP~!yv4#nTpuOFjO@ckk(7p0U0ADzK1%vLmsh4GlV&Pv>G<ph8DTYGyiim{V{G|z4cAdZG**bD%U-7&!98d1m#U>N}C(szktlDwihSeF{t*+5yoz9i}Wt53Ynn_bv31N?fplJ`hdF$-exD4zw=^p1J!zBkBcY7Y#X=GNw)Rlp1&zy(D0<xIp4lg$i#iVGq6hw#3YK~|Q%Mf=?UEUT^I_FwOh#f|&&PZ(r<bmG3POP<1Bom-E+d0?%8cKC22X06>Z+g_DWC*mA22^TVLU^xYlFg7FN#CV27dS5SvRMozaZ`7oT^HT-CL6IQAb*^b%4t;9>qa7_z___DBl01LNDV2?&F86B59g3B0gErAFEeGpMrW&jU7Bk@mw3adN8Z4*WW!Wd4k^2}j7P_LH{8aUuqHD!1mGy{JKzngMxADNc1<RhH3+@HjIUo1=E<X36Iwwro{s?fg&yLnS5_^X!iXQ;3oL);6xR&1j_EEou`{`bLKnafnEnwrjRVWVS3R|pG^7qP;$Yb?yl6dy3zB8n;<6;l92PP`xZMsYN-M@g_@R;YB4YAoiWZrVi;&(`3z=!_*IHDpdwzyhRvN`!G+I+>iH7h>nMKm;xB#4n{;@F+-(oB@=02XbSMFeyzO{a$h{GJ~Ns>QW(W)sN5}2nW6*xE|YcLMo9AKJynTeLz%l^w@doCTQ=J;3);6A8fQxgo%S)qD<N}ekt;xCHY#G7EcN`e+c95WF14@nP{^PeOg)vGPn3Oca`q=O+KILawJeiSh!l}tq@)RLQW96I8BD8<&@G>vpV6`OZA4~J1ITtBaley_-V2hvvphBVpq;?S_oQIaGo^L!Y;tH$pYvOxoKghWkv;O&sEz{++tLI9YpV#h3Tw&WzE&mA;1K1kx{TBMbY_+$}Cg3Q_yV09oE#|jfpl*Uh>!<Og-bIjvDgrU5dq{Ok3sNAd9*M;rI>C)I0z;)cu7eI^_BVE%(??V%Eq)3X=L?W^0oL;v~Hzw@dgDzy&YN)(eZ;D<5sKHMUj5jar+7AkoNY4Jkkg<3b{{OR)G0K<~G%ci@0vohQzyPIjlBF6%wIFJh+tp+XWShwxi(Ft5xBy86!1cN^lTnErF%=5xh{fxJ>S0Mu2t#*bZLPQ@%J06qq-?AukApD|bq^7Ep&;kU?F6TNS{ziMFr0JwnS1RhEYuhCnwfBTLOz0r&DT<Xm&8S-NR_f+qA-V~D^Xc(UP!d?T!2Q~KB!V6uH{s~v7EXP1Ic4w^>KARiTff7;ZotuK8)h=GlIqmOD#iNv91MirF1gDKJW?Oxpa8yq9IpMk{Xfq24fO}JrRR!LZ5Gtsvu3-3#cxhLTg@y?8C@wzB;`SIZscJErqsjF~)O&o_yigSCtF}&W&g5!bm`c8@Y}}v+K(wRI&Y&ZmeFrp;`uk_^Z^)(ML<>Dln#gGPJJ`B#X-I>qRF@qA>S*$HSiFyFad*?Kh#w`EpZ}qoEnF8JT?QBa3nt3E_&;sUT2+u|CEVk@2=f)JO0wV(yE`7_s`8_BSQ(j(NkW0f<30lxkZgNurWxB$<p@-4=q3jc1s`W3KlO8D*?qpjM*6CxfysYdI?n&<++0>_h56e%efQz-e4ol0gyECrTG=;%xHJC}X4uZ1Ok+$6ymJ$Z7ukdG+oWh8oMO2oxf>=p^EVvD#E9rkl>uK0*vJS*tF|5hfqJ!N&e7rN34(hrxB2XJ|VLS3KpqX&8YlqH%e>Cz*(VBdq6@i<rk%fWj!R?|{6$RHZqB-)Q;;l9D4>om|cnuRw3u)ZTTQKsdxdtXRy8M(4r-Z`_?(L;{Oi!&y*E3G(^<h=|8|WDZ&pfT{ef`x?cyr^9HL(TWpte*>R1f<n4Ok|<%YRK;*2@dX;^m3OM@0a<Dssvx<;s!uE%|BB!uS!yhd>ga;f=(PEj-=o#0GSr$`M$QqI*(N0|axZ4rKy{;9HkBMQ**!Hn9~Kcxxh+SBt4V=bmnB%&efG#(sN!n^KA=fG(1^RO`C-Besq;k5DPgz+Bh|1@YT6;zz@@s|iM8sby3xtlyi&TbW#?v_NZAQ;VAN)ykNFnKF8b?|4)ihWw$x2i*A!lx4e5tNbwkjgt5ank<oNhid;_jyZrXh9Xa-(_Z6B5cY{xb*bnk=uwa1|v#EVcSYaUjKD^RTDD0Mb;iUF%>VMc$Fky0jv=at52RJy}kP{81l62_C6>a6~&8c^?Bls0GdX^ikWTn>FoXg?=%%on~dK>VBiL+aAdS%Q|PFVaRrR>Lmn$_g_<Q1`-<N~72@$^gQ2186!!JiMu_40cPZpkOx=q@-ooo1O!7otb$Tad7}(=YzFlQhlVPX1Q%y83vwVLZgm$Y+sO#NI)1;oQXl$yegB%?~_0WDGug0S&1TP?zMu21y=%B<2M_NRrHS}+<#$Ye#41=MRfNQ<8_!OM<c0yTpY3VWN3mRQa(itn~P*RmK5!S9=uh?jc6?8QfbS%hAKqO)%L2(1h{9*s)&P>5ou+C?F{<;GeUZVGR0Xf7?7Y55N|uHia-O0qS=*W6)ZL>ky-~jb0<X$@~IJy)h1KB6L{geG@*5(*mr$0@O$1OJ6<yIq*8U*)XS~COR6ukFNo`(I|SiS?Q5y?5)V<H+m%kglGZa$q%P2tv9|=*uA*qK8ioES1i+Z6wgA*+D@G(p3-UTSuPQI8DMwPohxd`M4q<lfGJg?96xX&el03x97c5RAUh=>R<;wE1IHdY1UrQFkO)SLgRW=Tbt0eSsXAvMJT9DV#yBPjO1yoQ$v|x1%e8CNGI^0aD6d7uAi^ZuVRFsQ*b`rTuEZT~hg#M)r2o<unu%y6CN2Ov>u7sWthgg%!5m`N8wN@;~<t89z!G|1Ojv+FS5?zsP3R<%I{5W}AL;gs&DC;zvjlC-D`fhcq*x$1ke*m5{OL&qhKQzhTD#<9&H&E#cZI})5N)G}I!7fdB?lolE#F;Hs6qZPN(`xBUlFy|pASP;dw9~mv&}RBr=-tX<&M*SBq^x2!TP_u=c#<yDz;dn_4MnQD5s+-m@zAKohcq;y;mptq8M(^x07M+Y;r)atM-+c0Hz5lxA45ITqoHXEj$E#=g0LkS(44vDAbw7{BaLeSoISb#xIL}@PDAe=4bqiiyROpyI^9WO)qk1~r-UXE+uvS0Y6;C=kXDT&SPO*#Ld&f1f&f~*K@%X;L@iR;UlON=&k0Di86Wn-qnq`Rs5Melo@teG{go(1X0Ce6g6^bP+mu(4w3JxmWI3tH(N!f0#D)fc6w6y=I&lD)h{)~>D}P$aH)fpk1;s!Q<9Qn8F+k!3bj#z+qstTEOU3>DgmjFgLxCL=rzUB}8Gm&Ys&#dam9lm`Y(d1IB56<&QJ*Xb5!b)r{<F@W3QNSya_pxP)>2UcCBLwV6pXHAtO?tQ5;vm7zfAE!sQFIuH;b+1)fLn=YR_dsU@0Aorq4(OcV6kFD&U)0e6h+O=V6CWAqi$RVrUYMz|l78$w~nY+?k8W!NvEplis`T{p6$o&Bk9&3_Aid;UOh7`692Xp==B=Cmb9SZ8c~NleMW_D5-e?qx|mXkA5*+`jw;X)8@<q<f3}z8h4KTx;7a-BIPo5;;5`)lEkf6?$%@<=b1;Nk(lRmwbWZloc<kqWC#OXP%d$72#V)Qq^x;h8-O~b45g!IDzi>V7Hv~P6YE&X`q`mVT%D;VBvrA@7Y#8?1zn@z!loiQt7By=I$Ah0D<1SzxZ;)7=xM^a3gt1@*6VTe3mOA;0R$+N)+DmEL{BjW>xJ}PeMCuyUyfQa*KH>_u$yTDwJns3%%I4Eq6kxP5?E29OnF>KP(%|M%`F=4iJJ_VUeq_1F?d>)2#<+You`i_rX>p3Cd5h=O=bKQMJ1RVyS^lp0?EZV(`?YSq)n`^2woP*ClBGTP?|?lHO#?@+%W`<E}PENOuH&rH<qRS2BiKZ{F61!t7t@_ZJrU5!aFs{nFF-gA~X|7;>tzHwp<uKeM}+QTGPyn4S-g;EF!gXHN`PluW91vlS9!|dp3xh$E(Y68L=c`%Pm6yk4u+vEzvsJ3<WAhqmgtpr)Y&cq4+#&vZ|{!97Bf}sN|hl>R}}eLOvK|=(3CMx)PVNrK;@Ub(3$7U-GMfTV4i10Z_z?>OOgl0LI7lz?9Z_2|b^^jzpO$4Kl!#5WfJ7U<(HSLiVtBq`!9AVcCMgR4(GNmGi8Q5jz1bcy*B}62?kkxZs7W3uRN`Gaa1k>Eyw(t2!r)#<8lStz9bG%1M5PN2?=KpzjD(5vsk_sP@o$V`a%ZuXmb!ZuNw&Qj{M`j*~<xRK>RJTy{Cq890))a^IqfoSLIq!6=_cR_c}DCP?S5YR1?#;VA>}Xu)81g+yySvkWMGN^`r8qTn1E$L3lKrQ}s=pTR(#1;yCEaVekeXGz{=oDaqcC5~zlg;~qz9E)beWQ-WDAk3$)6B+1Tt}lv<LDhSheUjgAUESGV_7k8bHj~Ge6Qq*<&;u!1O%gn5k)h(unpH%E%p;E*R;-jnTQZVHYCLcJfq1%JH7`YlaT#mU3rDT{SSZ0Za=9NSR0`ACXl@Y!(C{4tRw~s}W&sLJHdUZOBih94%fQsdqbpFYklfers)X6_Lsl0S*xr){cIKBO0xN<WXa0lR(zr_JE3Tgevj-`EA*1UAvik_6nyAX9k(okaYL_vVCz9!`H2s&=CE7|rB7iw);*BweyA>Z|?l@CVpdPxf$(|@wFUlO3YcKBZs1$wjooh;8)ImgSZb*7zOfX+#mB-Oaa;E8`?>3vo$;y;;l2m(E$dA?hQnw45G<m>;DmT+2vH(@hq+V1_Ht3PMG<C+$E)ho;%<<A0H5QM{saK#aRtQSUBN7wP@YL+QkBXR;TpYX?xOqU!Lrn$N)8}&MdaUyM*F|}M=Zo1-B376J46X;c*1Zl^E@H4yTE?5{le^XWf+wkxEjIKTmv*TFcSUSxyc`4IIL1miqMo@|&2DF_w|<3;*VC(L_b|H5tuU_lHQi?lCGj$XaRoLug`p^vA{T^+*f}$GWrE%5Bse(La4d*DECVpDXXN#S0k5J^2}tiWODhic*W<q-j4_vI$;8>pc81a{&4z}HJkqL6$3)(i2w_@M{AuZ!a3z{pkI0otd(73Cws=naGgrie;U96&qaK8VkeZi%Rak$HQd_P@WL#y-S3%?cNV`Nx5+__|@=_~kkYpR_c_ej8ZZ0Gu>x_XM(fSgYac>q-zT$NUnZi3Cv7Drhe(-@q-BEYZYf7w%#3Ir4$<Q3S6cNW^Wia2@gVB)T39L4y)MpKuQGq?-q3QKcLkKFhG=_KoA}8GhFAOtYYLzBnWdu;De-@hJS!fF{Vny#rpTP;MlvdW$LSr*LlgfxH{46IrL46X2G<szX($M$3*_^7?HWUhFrY9Xan=}{$rjBsErlE|4cS3unxrOLt4)3cJ@Jz+w7&S!VyC#n0q|TgAwgc!<rT~juBB7DQVKGw$X-H!s^9VscdgvzvSTIgDbU;R)$}nhEe@i-DvALQG(RIP#!migG?lQ@fWDVfU+86ZG!wgqVYl24GOIR5bz`Rx?b0zmv;d2xlUMyU~f?<SMTATl)%_qyWV7CmzJG5;r&!V(_)d*-3PeqLwU5zzJWlNHyjm(`!ElsTAM5F(PY=~4|vqt@^f=b6MFTFm2bwdfrj+%nK4i?S~j!&dco|0OvC71T`%;HR;&JaIPD!p0S5Bh9au1m3{DiLBC!lfnlBvwtmLSA|7RHrBV<Ln~=U0`)kuVO7FljWr5v{WQk^1;t*U<<-!S15=}hW})zM|tc=S5_Pz^4Yurn$#@jZ4+vM>TF(FR#2B>=0evgLD7Ieg!7WqvP-0j(L}?^2cdvxRb-1DCWv2dh-4Kc)`SQoj*(dOJ2yqqE$vl#0g9Q|bg~WMor&V6#4k!|TDU@noQurddqa2UaTs&_#{iWNE(9Q!L&2yC$efbj<7sv|dZLguPqRrVx|%z0vd|$Ie{f;JF47Q<O}S`N-wI5VN2OGvX1EVKxG7w1q07&d6Mm6Op>y}LCKNFbNvO02g1r3wm#jN*y5&GsxfvPxnYF@sybx2_#@Z^B&rngoaXkE5@^QU5i;v`Gg0D7}bw!(J!0Ko~wNQIStx+9Pq+xz8=Uf}_??QnFoloU4s~m@=X>~P8+sU08hwR^?bf>8+l7)B@B*=sll$yB9R4m`Y7bH$JO-~IQaTirnMwX_T19I+W4|_06iUd{~a>I+G!oW*Z_n`ZarM*Q<<Avm(x>=xrGgpu^0x66;RJ{wMJWi>81fv>grEF~%t<J+r<(p8BDb=Fn&T_om>$2sBb2Oh7dTJpQ#>OB6S!X!6A(PyX3V4uan9x?U{dfTdt;&N|C^w_#n7rR5=8ae^QvCz8f-ghV@Q@AA<-we_!cYs;3#&}(7&(rMJcWy8w>Z@^N^u4+T{uC7pEbtmB$A*~Gr52u^QxV*sst8R^mn3~5zrW-ZgECz)y!i!Fw>-Ip0&j&hgQmt?fVjW!JV%>2miOO)`xzbN78?FAwdhj?EELJdp$dURk%`J`#fPcmM)0&g(NgvBni9JsYXJ6i7fmvtxxd}RIU{V*`;vI5wK0*fI6U^iz3mQl>Ula3RH>Q`T|>l)iE@6gj?rd1&kvj3;R;qe%{2nAbTP(_$Gzcssj8JJf|$jUJ|yrXq@D$FH8@2w`_i)#$-s}YkP6!>e7^ipLn(}n?<-E8z_sg><ZaEvAwSlFS1-j6-80F%`GjIX{}0s8?Z74Jip&ZWq2pqc#mA!T-_7RCnxs_g**+$UC3DDRTnH3IR_i`j~-<md3@AmK1+(Y%^YLtrK+$LL-D10i$ycYvZb4sGPA6$LZe$L<ajL!E3QR>QTyySn;K1zWpx(%WaXkYXK!SR%aZI>E*>yUVw|Sk^S@-F8cBZ6&p-_m;HgG<RE^ru$+JKmV0pu==bdPrasHL+a^P<R%5#e&D9>5;-fnXNXl(JSO3zvp=94W+tH{hHuo$Ny&Rt)X8#%e+0|xjyL6lRqH~mW+Lilp2jG#80>vX5Q`B*L<sZN+o<Rn?;!J@xeR*modD?p?x$E#=zJzmH2x?%{7{3=gY7|m;x=0cL4C|KxtMa(YaaciPg5WuF&-9pW?wdTGGLq89Mn#r1?&2|F|a&l#C29^==I3^t?=`Wj}K;^R0ic>NcqYvvDd4Cd8Ft6f7adJD==aVaM#xsZ|k`r~Jy-EUd-f%wG*{sUo=303KmkYhJscX&EiC;qdit_A`FD~T&SrciCk}JB03OgX?%kyhPszFP{jHHT2acwDrvSF*8@pXKyyhJZ%5z<Q8&a#8SdX`b5U~o><Y+H7ucu5;-dZ&78rY4CN6lEZhz@M@=T#LTYP%dR+dZHUj*^CxFsH!qL1Chi_1B3#^-!aSb5a>=rIDmcnJILdVM9EV1Ir)8^NQz@A95nDPKm&^g*==i8Q{9c%y8uH%lmje**xR{rt0mWlN`(S2k{dtb(v=rQ=#t@0^NYrbd>Q|$P&d7vYwQ$0O9-RUR3>Z(lI0g#RjQ=6rq?xXer&2DE5$##iD*tpr7u$rR?;iU#5Z~N3d?hI;HP+1&5T7I%mi|TW2LxXNa1%MPjuoSprRKPc!;--Gh}uzBT>?Fbc{=(P2-%`mF*ii7Bz*$BnnHU(i!YXla^K1Vq2eNtNdX6%M2D-c`w+klU-c;hfu4gu_`~ZU1}cz+VFCw_`L_>4x(d3-AG4iSca#f?`4F~Se=ZBNHOef%myQYBLDq_X66*^V*OU^bSIm1trXfJ?oZ4TcFYgQ5M>~oKsIB}7$qOJ81P;#ukN{xE+#;VqN99$dZzO_g((1?z1sZ07-Pi=fHZmSyZgJ3#{H!A)x6OOM-RZDv%tl<Z8J5!;Em4oR}aW*zG0H}1^&-nlI1(gWl#<VxP2zSu6!lv3az&jmpfLv$%xKAQ;gDKgFR)MX0NcTH1VveulpTb?rG%%3;meJDG0PI6#j0VasJe1($YCTayI`1P`HkW')).decode('utf-8'))
_LEGACY_ACTIONS_6C8S_3Q = json.loads(zlib.decompress(base64.b85decode('c-rk<%Whm*a{L#rxlld$kaujU#uA3z6ewwkaf4_y;4uss<3-y$!~brXDpuXPCo(c3&nc1`a91jp?mh3585tS*>;Ihm+wXt;{cnGq{L`-|KYjgp{r<O4SD(Lpz1^JLpPu~t@BjI)|Ml%J-#-5R_dovQZ~y)6^RFi#K0f?a`|#7(zy5ah%g3Luu1`)+-rd}toGzQMKY!S4K284cd9!){?d!V_o2xG;rx&xYf8Jc*{Bm--*!}#|?alkI@4oE+$NByJ|DH}e_UYrhKY#tSf74>pw_i{0HlM#dwDp&p+b<s;KJC7meK;J5&ztM({aaV_w>~~@@+#1f>1+3&=2L+hFne7%d$5PQmORYK;-IhFUy*lxy1sh1iN+K4=kY&)x6Rs3-n#uS)A4ND@$lU*`^9k3*X>LNKTAh=b2WeeetBGd+1$<-(fqr^)dQFAa=wT@-+Y}fqIPlq>Hl}e!8fzsv8ika=Wu{$qqOheyQ}TeeEiY(ojK{cHJAJ0YG3*|3e#Vu(*^b)njEkbniWjmvK@OcW|QG)W~}{<K4aT)r$cw}-1*Mi4`Dk^!Ma=sha1=o;nB*^mV+*6Ba055eDWS!s*k1oO+Jrc2)8E;n4@go^g-OcWB1|P+4~uN@CI%_?mZ9Q{*q4m*yqy;AJT!x|2uip(C4Nfp5d{xTV)kklgVLfTp(kfIzL;T?fc{{nA;=dr;QmgrUmbAuCF)mzWny5&Fz<u*B}4o@Jtvqc;%NEOQigcBhA6%tvzW^xQBL*$n3|#RepAFSb#5j{TuT;@8i1e-KO?mr%eLPyT*K+7~x>yR{RWLjKDpCd$nEKmYK}^Fzs#D$8-RJV{aIw%vFJ(vInxUK%deFGLJyCA3OZfxXDEaDjrnH_Ek0z_09A7C!S89>#G1y>EoccY&Z|VxZgjrH3sv|-vTGZw#?gSJuWp>32yephV|>y#y?HI_kj(yRzdE%VG!F2?csa~qc3K#__tH<_68v}(s9VHTIrCi*blq6P7W;p?iAbJ(>ZGh5whNOC(!$~%h;e7ZDm-v9TP&4j?<L2-!Pk~<v~n_f;~nT{T}s8u~C9vC4-SehR(q|hqC^0fUDQXzCQK`e5?*&jWBiM$U6+-r;yW`4WI-e`S#t72g}?!4PPmGjRv057l6zxq6!G&p;Au!NmRYpk!2TrFg72qZvPT>Y}}1+pao(S8x7U2FU296jztf}pdFkx2Du{>bO9-R(03jC{#I|$kx{i9l<7$2a0tLx4wl`1jXn;_KH@14`u>UNs+qoTVxa37%$%b^?=$d*N`$$6a7&YVH5*<Z+Y1t%WtP+Scb5;_y)~xJF!6EWm{waO=JS`^tGk~zx3_-<mP`p@N;?$39nvtD!{H{@z@QO}`y-%HPY6O;cc)=S&Y`I4T^b_`Rp9AZCf3wCnPN>I!o)$9uJy6|u)EUp$7wj*<BdGow3z%lFx1)Qoy<p|xC)|vTVH=~X4N7@pT0M=5@Ky{IYM|7xZ2L+Dlp;E=y<Pzt>+4pojcgkS*KmIx-T4`LcA=o5s0CJj#tH*roMUx##F8qhE_~2!MmHA>xZ-$Xj*OmxSgPH=i~d6vaPrG=W%b1ucf0?GY1((Vi0F#KGe~zARD}gvtqC1-9(6>9E>Gj2<#t_sWjS9C`}RbL$vsqdS6R0R2Mx=_g(tfQEl`yMam@fw)s@XJ2z2&gx5p>o6f_rUK0_@IN?kkCKhz>0;BWobfcqhep*zv0UKuYNgot&>a+mzJawkV_yRu3%)C986?JZA%PvY0yTjPnI=8%F#;R?OiIgeL(UrqnGhT%Uh@k9UkZl^Y0bIZAI@8e##h=awDEPX)$%7wqNFg{cR?cL@jNLpv+p`d)dz)tD#Z)f^QeXhtF0y2xePI5tl8kCb9Nz_>NJev#U)p0mupLAbO!a(nmcweVK=>az4d9SnewxH1TU0Q=Wr+{L_FKDNM%iX<$a%i9;D>yqnLV-V1uy_YTf-XXw#)3fVgEdnhl1RsgH7NWWZ_npw(?3g8VJTMo^whIz?c`#HfNjz*cuFf<&Xsfs&hU4;b$rRkB?MZQo*Y!k3dfNeuiA|F-Y#h_CfktfN!z4VF~0+35Bgq0DoqA9)<J`aJ%*yY=d(Bc30LE4USBIVAK(3j>;ctLLr=(%I#OoQmW>87_I@hE_W0BXz>30@%qo(l^6L*?Jx68zaEf$yQROsZy`bl60$yx*R0(s28+&y6*zd?<Me@-?N%b#@`AXHm7imVp@h`aW6Dv1BYSVAPmSRQC~2*E4vkb2dWZ`%JxX%YshAsOjpZr_Ok1}NNnnX<5g(p?&Ka2N7By<maU>1Y%CEIXX))&7(q`Eu!}m&Tq30A_4`&AN)V>P;R&!1y$G7mInsA=EMxk#us&!-=(Ao1mTD?7N#e)m0b*#n?51bYXt)vr4oWjA&tbIWX>C9bm&r|Mj7B%3>cOUz7*!CwjIm~-n)yo@$Nd4&cNU3K10l|Qu4W)C-uCCyRucI@C{7%!TI);M|43Eq|Cj?zDwyC@8sl&?b7%@jO&z8(>ewayw?M&I1wUP&W(lD7P->zcluw<OJy8=W}&|3b^2wUT|1X2qnsE2wGy*R|K#dRjt^oltg1qJY-{;(F=ZSe`(RmWYHQ%2DC*VI9b2oYeNHQq632y#mkfsxkst+4r$7fbPb65u479CbnzIC%h4f(94t&R7$hKeyMH)`k`;ZMSxEfp{j+#aRX_Or5c!GLEPUNLL|V1LRi}!eNR9T@X=w3co{{%p-m1oW>_;RsH0734;hsv6s-S*TH(-p2xu`WbeQ11A~evFD8KAwv7hRh2XX4^P+C(Hm?#(ms`mqB9&0m#eJXTaWP8^nExu<p$4y)Tv3lJPW`9~vklN7Y4nK)?$AR9%3<SInbce42Na@qtz*n!Z`xW0PSqxpJGaxfh+)@bByADDHfwdXFjEZot>N`1*{Y1@i^MX?Y6}2$eZI9Yak72zP{T|^(A>qFdjkYvTy3&00K%~U3WnctTQA#SMO=YGNh_rRa!3$k0L4a8nvi=YEF^GrZQ{mA^TM#adehrAg@W5LJO*;C9$9bGI*sF2*TG|x&b4RJGzLvtNpn~UbC1NLX$RWgVsfR>Lw0fjKY$Jc7aHvD<KgTH$%xV%fFHH->CASA;{uYG<sLg5Pq%7mWPo&kZjok@Z9!2%<I-`|o{_?6u^Fk&jEx^&5a}LaZH`l|^EK4hp)S-|t@5EY(&a#)oit%k)5^g+@ses{^nv1CIbnf=FwdL3(DF5PZ#nhHL(g##Wdep}IhUM<QL}CoG6{mK`_fSjLD4(NWF9_Gy)roaED2b18GTu){&jG+>epqs_G|ezjBk_;Jj*dG72}|VGTJ6n)FdC#*vOc%B`d@O;DPKqkd3QGnP!)EPX<;r2pfSB-@hWlqvy0}(*aYCry+oDA^$xUt?XJglmtQ3W?tfwVb(F-#34{7mrhtX-X@Vf;-;~&EON2aI5$J;paw+oMVnz(kQu`kSENjqkdK-Boc2IbSP34&rLd}Q1aX&HtBD3#j*O7rS@EpaHP)7Iw5C|+^1Ldm>CTeTno0{Z*z3e0-Eq}74e4V;Zr@>KrKC@%&6WFSXj)UzJL5z&5!ITAAcYRyMuFO==x^2Y;wi~1PT4jax7lMf{n8R6ftTHv)An2@IL+~a7{GE+1Ee7mTr)xSjFdVnMg(6Jg^4$2f=Yn^L!2@Y-?!uj+W9Zii~1Fodqtes0@9HX5C-LBojhJx)Rkn)5^9}IIj($fBq}Kt*3+zvatalj_%!i`(I-+bua9YOm0QlWA9ORCY<h8I*yd<C51m;(jL6mF^a}Z(2Em0%2v3|H(icb;>GFv%{Ui=qp1Or#;<VWkS~Jx!5(2Gk$Q5@)Tn1}H&7M-KPNTU2yKas#3kP-;MI{Ill6NV&eiTkj`*wL>I>9*Jl`WZ2-cxAqX)j4Z^^j4|!lYZDfyfF|s2G;cgekPIRm{++QNU-GV<RZ<Nog#wpgO#MaAwRqHKd6|>jbr))zs`BLEGp5p7wl+nHreWibXAc2xQ>NI2!HI2szYJUO^0J6aa!&T%gK8aCISib==j23uLp&)QeiY5?rlCY#?>VDwENPDFGXW`>E_|GY6e1?9t$QI$~<ddqvDkma1vV9EAEFhlp$LBQVK9>Qia>a&{_^94^!xS1RG;kwdw*m*H5d(h8dLr$j!b;1qEsff+9$8*VkO+>!#<m6oi=qTYQq<0YQ9maSEi{insWIK0S+3ydezCBYllkjPd$A;%a^(~6IwqX8K0{IswM9t*`eqb@me%9;<%4JpX-iN2xJo*tDz?);4*%NGj*yoBKab8gjT$lLy;)e>e7@o`Jye)oLeP95BR4bPVq5$CB0vXL;>*Tv8+kc@Af^{%R*%xVy#;3Is)J1=<MUkRa$*<bWc_3{ke`UV8IpazaUS~4|(vhs_ee0?OlXw;f)<RizrMfrB$SaI>Q`=0y@%~mayCDTmQTtlNa8H!S2uo@2Mp%O@MeSXn%HW>0=RW#VAvM;H;TP*<6Q|1{MU0@SZ`f_D@84$_+)ixMgW4i)m@NkA{aD7OXNxFw)VuYtQPvjFQ_rfZOL9GckiGu!0HUCT$>;NsO^;k-RXF>QlA0RLL!Q+rxc6_|sGnimCD5!TX2ldu%Oz-UZe4Dt4aOm7T5xW=0@YqS8c|3!XsuBH{D9@Xf<8og^rSC#^bo!;mX*Oz!)QP>V*(%VgVLvN6e!d0n5r09f_!tghsvTWa)N(}SH&C1Y+=woE;!Ye-x(H>1F7GQ9jljXBPw8~IrkVPV-z`lm(=msUyIAQy;YHTPxmJdV7*h(%Hb<mQ=xP=edZf{LsrZ@bYegn|Nh8h5DP$B>8qeh<h$K3Mdt!u0-C}e2z8x_E7xzY7oO;L-$vWwX%mxPQW>LyTRTE3-?jS_?9<{)=wWKuLEaBsGbYr8gDUBf99=Td!9Ofqq9WZ)wiF_+P^93|C;l*c@GO{NtLxF^>a7HfCQshYqt5U}<O42HD4&HzKXOeOJUEXA(S$3|U3x)1AZ<=@eRLaq32o<X-D0~y-hon-~z4Luql^5AJWH-~|g`gxqm1UicUakyTLW@iw1^rn@`|$ZIasm!t`QXGY)`1td1iH41x4|A<zElc9jVV8jG{8#|c9k6~&;>GhLl^X`5Mj&Yf{H9;MVX_QSRiK-6hX2vbOYqtiG}~VgD%x<0YRF-ms*h4Y@l@JaZ`s_52EH>)5K0*fdBw|;rDTK#3E*BXi^GDrC4sj{+&uRpUWA|Oo8~koM$bBs}tV0aYvEY<2VRiGf@P-vX(SeGLAb{^cN(pxX@l8;s3l^rM*;QZ8)^ah<5~jG?_tb-dK)?E68BSua_k?0Ln~Ci1?d93i$km{5!=_GguEK8v-7cq$Eiq$u~bTodkCsrpP1?H%vmKPx`iyLOxK=aDWQiq+<3Qul|7u=+BsD9n&zl^>q}E#(}d)D!f-}(f6D^Qp$C7=O%GUhDkqJ$~6e`4;RTR=$<_`XLM$ERdrv0;49S<SSEKxgv_WOkjOKt@wMf>k@*dF6FizgV5a2NYoPG@exNcOQqjqf5uMbaO9>6i8^4o$bAi`AIATtHDm6njr`yX><_jZ8&KzWF#wNkeIFOsd0jNu7PL!N-?DOzcv<ZCGwYJ#=NT8cF6`#pGHKP*Xxue*xrqORC$p=x1x=t4XYy_H4qzNL57@3wPCGUx)K~eyHgKJy^)4<WEQjr#Az%N409%H&hpe50eY&%G6TojL7F}_TAkA^`NpCRHts%axk2RgdY$ULQ$3o#dC|C5KcFqChhuGfTMPmy7CYVg`EJY=J+-t2H`<MOkmDt9x;G*`e?CB`?7sg|r~o>nDAtpYPE)=Mxhy3-?JUE4~LfL`&Y$zD3BCpq0%mn^O6ABSA=%+d@`29WiuH_)gUZ@xy!7+<fTmgIydvjF}*uQo()9Zz2lP05I&r>|Up!mr6VLT=m88WA}x2HA+wDaNVQX<}xFb|Tv^X=%nHB&gNc5S8N;Ewx&tSTFZMb^j7)s7vUFqIP`TAdf|)O8KjRRRTc<oLV&~8QhsqR6H6P_LWmEc)69$XQNhuKkgoZ#gz=#em^pml?A!-7`hmiXVjUr7jMge3sIzYU~4cbx${>Bl9mSIY8S4gIXWsMA(U(%U2a6%Sz4J4iI*`rIh@B!Qj*jplDy_@o1_OVxkK1rt9<G-5*m?xr1F|Q^K@o_KYV38Q}fG!k0j1HqA%jzuXaVr2hwH*X)lmLsV}LTWX=J^)Dp3#pwmULW6xd`O>4irUIq@8Xz3_KEvG=naGq9%Zs@ricOnRPcGSWdj#f=>sB}`f4&yr<hw{20YW)|h{kCf-f?8yjmX4>Xr)ED(ODh2o%ZWNF{Z(!JB7E5rR+N({@qo)KOsUz?5<4_}Mi2|}{ceSFrJ|qV2q&yLOJPysTQOFHaSw2vkd5eO7XZ=}A>v~X#<&n3eRJPe_Cti~D3hu(;urT$VF{72q*XJCsek@Dam$D3IoN8I4Aq2Jn%*9Iu1-)!y|XoU)@7=O1@ctnPjp63YE>FKK*^Q_>-|X5M;(4Tvs6fH`MmH%Tff3nhYAK0vmw(=7plOYG8u};7O^3)Q(J!o$O*T<A<G63a^y&XqHxF1CXpW$XB_6Vq6(`KcB>nZ0-7`QE9%QcVl^W>H!5TB0J}Oc*Wb`w!iY)r{KZ{ge2!rP-K-1B%11-4(mOiM7XuwAh%7S$$W&1_T*|=}YrMonSE$uOeU4fAwO#S0{5utN8(SV0m4eNxR7h7jDr`|isYFQ+Fzpz7>enM8*b`U;0nO_0U+JV1<Fi{IsC5~u$y$`qQYuVI2_-Fz6D(EaA&RV;+=gr~Kco}ijz?PjC5AiPIs=qe*MfP6En{f`c#A3UqLj^m(=^FB%a)|Tv+yQ9$(e3Z=Nwv;a#d}84NpXc^Hq(`l!Tt(`mI-r7DdFmHIKm2g^9Epn7RKdJtdM1Q)PG)xGIb0lo)8tvkzTbLW0Rk85!6iDpHec!fB;MGYMsO%4pTBxI|VaN*1VT=^fIzSRledD%6}7l!_?Xj08A#?sE#KNMHyneZ~kvaCZq&$9#z$pZ0^Y<DRh&@Q+_BYl0vr7|L@O%TihT&s{Go^~}X+(Glup)j=I<d3987RuaKT*wILpA0i}GP|mE#EE$qYd5w%(fzQ_SoZRDc*SNc9!ot+FI9UQ%P}DBw_E3x1&03%5a_3pDimqs2!sp7XfkgnuNTV?)mI2EqOT=Tdj4eY4Pne&xAw}RwAqmkI%{h8v7ELlSBr_<R7w*GFpF0x$&V~Lk+6oqFZo^C1D;BfA<#d@PadGm+N4+_`QCcKfT%B63>(Jsp%;jwDfjG;UpVx&Xr*mi4-j;M$sLRR169-g&zz12!ySj@#(7dAui7;fvDOr+@UEk`}XawLO(n>Z`+YYbo5Jn%fKNW0@vlWflNpSqy$yM6PLrTmWi5GGX^O!n`19)ayS0q*Q!6mZvKENd>bu5iWJ<87Y%~CHqHa%BYXRSulIoD`PO{XKnW^06tttqo;Js>SEx{MbK!@+_L16bMg&uJ#zS>E@t+@v14Zn(`@JlX)@?&2si(IqenGi8ZjQpGC^wxW?j1z=OeJWFCiwK^}LKr@Md7lB8Of3170P{JbSgHd(fjU>0Gnf=Tuy^DkUMUs(XN*2oyab5xAO2Bvon*Sp#VbsE0UOhQlnB`ZZBe7L%o(^G9cGHvGsn@~a`lbwDO}GIbiAF4krI*Xo>TwZY+RzcsJUzYepQaQgf!4Mh&kT|fYM8m2<DQ2&wS9|fT$08#o;`)*5^EGmuyvo3u~o+^1w|SEOIURmwdM8g_`JRGLkC*I)uUr5P>e2^EN-VrIt3Y&GT%}~yyj1np%ulrmpOW|eW<urvrJ=J1e^&{5LV}7w+DB(DlK(4FKy3wX_AhfL>KMD#<R($X`o>JnIznu3i|_0vPv8qTL1|_F{`0f?m_0<Zl%*2lbcu{D*BN3cGbPi7em3Z#RW~V3nyfG7M#(m*Q~o3=+P9Th$2Ad;*Czi<EH$boPl>odwuTJnQx^zq+~t4f>$-;uo<m^vQi!%S7XvWL%DiG!&^__OSmk81*+6~G71*5@MXgAsFC#7JzOb({!n`d=h@^_(^o{S#+_n#B`<j;&5=xgjPFjBA+cDMf|fFQEYCFoLuiy!Q|6DX%?$2IZZ4LnGfvb*Uyc-%X(Z~V7Thw6DO0kdXR)^LEiYE0Kb@s$ade2HF2|Wy(ic`FP7~G2<RFcyyew@wu(m|~FxL4_;it-G!@{ixirANoQ6o}Q36xNst4Z6+oK(^*S{O9&UI-!$R_sy9I%NC7Fd2x7vl5~FkDJk&SIa(y^mdUpXa|pXDjIFaI%+8NNU%Dg7$T3v9u8KDnuO&6JEoaR{wrc`VnirYD;=SRrS4p4F2nUOiymYuHPmhw>Wm(BLrWrdk|JBI%@);vsFzZ_cnUajX%O?43kqGnbQQ24q?F=$y_DjMt)N)K7}fYM;7A?0aAIfbYdYq#w%5qYi=COT(ut~9K&0&Rk%_F-*%D<_%;97;-*l`$?PHv2q={WSa$lIkl{lY@M9v5hypqGg6$e8JlG@3@wPN7d1<g(}k}R1SGT|yBBq|X(K>L}Ku1npUlzA8g3Z%rsG=;jo?^vY)t>7EA)dOfnM@ZHsID{_ppiNu@9amXPT__#4VhN1<Pa1ni-i%QmNH-#*5cvq7iqC+FBcAsyAvzy9ZBB?lr6f7U$Bq}2S8kKwFQBYo1eO*`2`)O5*E#mlP{F8%U9>c%U~Ga5D5@1fREQvUiS&t-R>?aeEIEy8h8n0)G8x$;pPuuftWxo$Vl+yLL&qDxdK!JPX(P(e1;DpoWR*a#w0oKKCAwS!;G(2^1<F1$pG%S!t0aDDd4eK|Cb@Q>E+w$e=(>|-#@xuNo<A<rw-V}O2bVA>v_|KX==QL6m*GVsIljQ0ViUJ?%CU=^L@LHPKeAXOSNBF5U#^hAxG>p3i`A`zc7vcL*Ic34o^GgRf}^R2e_2^3$TlMhFq13;A)#)ZpHGe|OQ8|m<5IrRq~Gc}1?W?2c1)?sAR7g>!TOWxp`IlYIoi1Ep2Qc@SFY7GO?1;Tc{*y9dqlZ6C4O#&CG8X|m9u%?bj+v3)(zli;eI1HY>jLj&f(I^PoSJDFaj;oN67re)H8?u9zeQ5j5#c_EP;MLfAdY3Rv`642=Y5QVEDDpA18Kl-NC?#(LuH0Oq3wv!E%#}u!zN@gf7@X!-@ic8VIi*Cq;p^ECNIW*9<m`J0&5|6~R|3%P0|}-I6Bu!9JSk1o%uX@cp=?qq?vI)V$t2bJpdor+pctRwkywd%El>f!JI5ut*28>mUla++|;?Ws02`KM-po@&LwhvM_rYQevG&3#jPGzSOK}<w&mSg|{b^W`OD#X)e2;^KVlZ|FSQ`&Da_!p{2EgWuQu6k}P|0CL*Uz(K0I2P=J;$O7Z_zZ4TrRWi{lb)Ejo7MJYimV}(gX09YaCph{*#!;)zA73Uwh@JRDbtlWo;6CqAd52FOBFzS;q5@tT0=7~vpr+lzw=}#oiLf8O#eKd@K2t`P|M)tg#)us<)M0TA+rnQE4k037=97%Y23xO1sItFR>X11XaZWJ>&<*4I=!1=z`IJ@UWz?#xe3=k&EWol81BqWe;9x+v~61`J$DK+(a7T`^Y-Ij+!iy>&VD$W^~s#<6k{YqW&L~v9y_Lzqf<9G!+<#G_}bFQn)FU~MP^uyF?j9|7GTfec8%%+fIv@(rGwWo@zR6_Kq*EN)HRZi(YxJ8$eHJ~W1C$$!HvFag|FkqMYAdJQ>)oO{1E1#E1dZ?CiUuGTH{)q#Yls*C7a*;SY%e{p|QY2Sn?n{g_O9l;GCG3>L1uz)MCRVB#VTCBRAd??zyPE)PrpL6hOhHw^Ll8em)wB4CZidm=VM7rex!M<=jacd97{VPH5jGdhX1l(V*Q+@ccZxW<x(v;1(2D_{1zrYaC2WgEdLgE1(76%IXcEYYqBo;h;$ZtWIaX|h+1+Lyp&hc(vpQzENOrg-R8k`7<&n08CLWX(_n<88S}tr^*PUSn<RoMA@458Qh|7Z(^rW~G7w3;VuN3GrJ3+P&5g)tLYP1leWW@Fu!QwgKb+>}*i%2USkrNkhyP%TxIM!<m@)CYeuUF&{l$oKP!zK`B@I7@_;9FD!65RE*6aCTZ^>qk|$EbZx{Jd1CPcX1c?Ib~IDhk0C0+AyYCf}l#vw*K$buoqVaxax_ZF-?;NrRnIQO+@wQE0OEXd;iadY3HZSgKT~8-hYzC?YEEm7~)mSZWfZMzV2Y)S6Bsoo+WnrBJ<^a~Z@Xr3>~LPDu*g$R)>|R2XZDnaXbF?{x|1SIQlMx<?R6BENU)0*XYAxPsCF5hMOtd=Of#+dfZgn(_gRXl+i1w`{Kd%4J}mtXWnKt=Crdw`vZX(7?|{;ND(RJ(!SO%hOz3=P{9DCE9<c_v$DBNdQMFsGnAI%uBW8o{4EDZbU>GfP^F!Q0HD#QGWK)zV0S`HB$B?x5jB5M=>Tw4Y-~qmODujBi0fm-A4;<Z$2riC81U3QRtUWR4FL{YNlBz)55EdaBU>lnU@Sq3RnY)`hqqsFtY^24_HB7UuiW^nm%iJyxaB7Uregc+*xI-LK(NUBdVwtR*#3!I{1kY5E&2Sm1FyAKve9Kd%C`g!I<HF-5u@w(#((FC?8l5D_rM?k{4Ukw6q+U_t$>--s+5Rb^m|=P4oZ')).decode('utf-8'))
_LEGACY_ACTIONS_6C12S_4Q_FIRST_YARN = json.loads(zlib.decompress(base64.b85decode('c-rk<%Wfn|a{L#bd0;(QBz5C-*J>Ke88%3^3ade3Fo0GNAgm4}-Gu#j^^*0-%CImu^N3`#N4yn^#msnzyScgfFaLY?@4x;2x4-^=_D{c@{qW_}-N#=)-#$Kld03xq&(HqjxBvRL|Ni=yuOI*R+wcGR*Z=wY`IoaFKRy3d`|!h;zx;ap^QWI~@6OK8KHP84&gaF~k3X*0p9g<<T(3WV{d)7``u6GU{A%>|PwTt;pU=)`ho66bxc~U&!_)CUR@?30&xalR{OQA=zkEKvX*THFFK3(e<I{6nf4+Zs`tkYG;j7Vy(}8$g-`ySGx){H8|G2@cKtqPFJ$@Qb1!}<Pb=BE}Jv_AJc}`|0eck<vyzBGb?T2-3JW+r4{{Y@LYBzc7?q7!ES+wK%yPuDX;iRv-nX3FO9O3ot`2EM_ar?A>7%!sncc-fdF5UTf5k202884!8asKHaJLBY=QSaDPmV<LTz@t$*_V2^(ZfWj+^s+MtUAN})I9%mR_oFcURXAN>|DnkNJE2&?<So0g2V*uEj$+2j-{>>88+ST%C(j-4yyFm-(^OfPGvROpo1uEN^0Vcn3);w{LnofReM|MRl)s7R5e(t(gaLCD&6_@mhj$!4d_8*~(Fbqfj^p0);N36jr1yP3o$xLl*#Ga~O<kWGe)tBD9o;I6iZvM=rp5)*=c(hf)!DwU-h#0`LVjA95q(<l;r{M!{o(1?Kdm30KHYu#*V8kh)8M6FVl0vLJ0_Zg{jEJ{PjwF+9FftFD_8mD*02EI^!hjEcihKi-n$L$zebw`n0JNwI55J&!p-;@z!-sh0{3dSv@J84_hH!EsE^?Q0>|DkNSUhwKSd8@V}U+}4`d#JXg@aiqxB{y9jN-CO17`Efv9gD&p+{W+FV}+cnTi}y=B9B0LK0Ck)<&hZ~hWEA+}}QKI?IzsY-COS2nEQpVt3r^1Tmis3iulXH7-{0+K~jgI#QGR~$ogDz|fJ9VD*7$Pj3R>ZFUIi-CY}#_FY!yc-#~emt(*Mg_dgc{DW^z*}nbAKnO>4UsZW$nbEhEq*iwr~#a20e}SOq9fAffQGBI>&ZXH(*8Ke+52PPA8TS#b?e2B)q`MqB`P0ST9=tKGvkY!;7HQtGr*9x=wW1cWegM#QgYf)LgKAnD7(`uWAo$f!@txz)(RL6x}&@LVh9=y)uAuRAsUWF3qPP7oHBrTU;;FuAbijd9ea7J>C6Co<S;11k&3Yl0FIn2yW<+&56UrIDG&PbiRe-pzHe+_S<&G=!Ghjg;0>AZaQWbp<MeJIyg#-T;kk5dq|4_$e?sHC)<K`D5w$aw9-kg=H$SW&9{vJ=bSZAcF0pFEmA6|^NE~B2ZAq8l(ndd$eIrVbpM~RQ7=~l`svS}?q8Kdbw3*6i8rmB}h|0r^crdGJeH=a<F6sDj8VtL?V+Y$1b5T1+9-I7)@dzYWL9O4`*DuY?+IZ;GOG7ge&+^_P{4;?%?L01n^G(K%dyg}HtEkn=wrLtHmBlu3d{WHd<W*lc;=}!uXOf`vRq>Ch`yJscnR|r+5QAHAbANyLoTdVesNElTGxYU<{3t{MkG{ASu1nL0&f%mMnKz7_(1|TF9@N?eARDp!$&rUV2b}>!2W0*9zU6zzz)0dt=CYMgp{4+;?s&8@jmo%h2wX{EYVj!zKduvDMbJcmVje$bz&Zr_4fsdEVr<?D#t4*ij!v}k*^t=_Y^>2Ib7a8zQzE<L*mI6Y1zd}fl{%F%w94e5+Cej5MJ;jIY#AF@Fh|t3xTc{LMK;rMxfGP0LvOsp0A+Z(k+B@FvYZ(Z0t(H^%GZ&(#$f{W1OeW8oc4R3&WM)NbxAH_L{Ayzyn2=*$^)kBou~E6n8GZcm_sxQwx={ERM^qF%a3t9i#=spr{#OgV?&&awotoeZsXRmdtNsdtJiI%A;zr?Heq=Lkb57rX!N&ahAXoP!Vf725%jm(sbq)A9A~=e8+By5hlifj7;afA!y%cN^x=tyS)+3}cInQG7p*r4N96=10*c3{7Cra2h8%&#>C2g5iS<s<icmkGA<mr4Z&5QS>n=(=Pw$2}BQr;uX2|<1Zz%XP%L7RyPf+9N@W&R4UXDd~*vCWMx8?}!e=CGtEi;?bM6ubhe>i3mrGn-jq6iMf!#wWq>z_W|{du>*YF<+L%Q%&;1q|P9-<S8z=JBpvkX?C&A%Y_Q5=}5zSvH2iJsy2t2|pLCL$I#}?HF%&cu^%GvvW$dCvYwwxtl|)r@%x?il^tV<;L<blf#1~riGpdIle+P5$v?k%`C|o1C6l23Z<>Y$7ma_4(1&gq-=Kqg|qSj$uMe3ZUrud2&2?pf|w}lfzGAP%)C9vIn2QwV9dZgCO%}7yBnOcE{!AGpiTu(;ucDK;4q+VQ2LP*jG#BG<uP1ok~E$%V$hhdFSR0aioru%h(KYkN6j!4zbsx5a@#C_UHM={=6ZYD-;6W0Qh4CG5TWmRFKhQX`JJW*HHAwKERe_}C+u4<s;N8Zah$F&XsG?{LJ6t^026<(p((qyR<2)5)+BT4%T>(17d^(S6MA%A;};It60aq26#`F(NDj3{j|pjQS;Zj)qSf%mJRO8IyHJT;VJ+Sgx1ilN+~|^xiM6;zr&;+2kDpc^S>oGxh6pf?8h{Fo1x1k?$*s*~JDa{V!$*<q3E0PEB_-Wz0K6CWSw#wF3~Uesy8&G(7cO&QB`cNLt1RM;K-8H*-(|w%MtrEzex-0#&ZJK^Od3y?dY)-OFE>DmH@-%*@+8l0j$F$y0#j~k-!8XF-a@P1=wLO5`@i7^eaq-U+J}y*Io~eiPKYry_sVkAMB1JVL0Hjuxs}Wa%*3Uxwr%pnN!JTlW0O!u!8&OZjP$(8HUcQ%yRwB4ME=l2I!agLS24J%nuF9_N2kPVGzu$CnJdAqevUKNMH1t-QzV5+p<LYR+QJMm;G3<!or6qPw#HB-n5?!6Ag|B27H@_f0u2P)ENt!U!of$#!NQgW$UZrK1;hBbt=DC&qh2iHYHLt>DMrFqFzc=w;y^uH8Mp<R7dCldUN~BjZ8}LBLE?04A(nd}&<$%U+RN+Yzq7p~*(kh~G)LBtK$XGlxKD9O%9+q#c8&qBKpPa4LQA@snaay;CUcHrtclb^I39qyEq8U*n6y=biO5!iU~;wOV$1_svt3lBgP~PoC&t0SuG}h+`6@{7089+E7%m2d{s&7=uH&PjH~|9qv=?<kL(i)-6OF&isn`$0#qe-ElCx>m-xr~iPU+Y4MK<MugEBf6b2=jPspuDR$zaR%o}7qrWcgEy`V{y_OXf1DdTYU9ED|c`f)7V3qfR8VESeKQyyuqo=&+}HeQ0IbsY2uovIx782vO4o#wiGtMH~wf2K>m%6@I<VphO|E=O&+q<nks82Jo*KKU<}{tQ({zOUh9xjYA3l64sDhD=}7pspiF=f87NkS!|5lR#!d>)=6Dd-aAiNj&UgdZmV-roF^i{H|sYIocnSM_zFq1JUj7~IxtY=qygqW(}c%z8;P#K%z$Tt(O(OIS$zg3x~()Av!$gP6EwV?v}32K4UtBYbW>54gD6?UTrKRzOAEzmWi)AP^d(`OP5rK`k%U6L$rufe-(l6utRdGb3x3ojBq~HO>3|6a-%KLv^g$4dw(*>2?B=qHkWPT<^n`6(fQKdfPX*urBqs<}7Fg79POh7!T@S~$o;;H$;4rW|ZamDEsY%5NNDFn_qE7m!M4fbX%%D0<Mpwk8^huiNGZeBgWLcv5=~Me#Pfyc$D<~|WS)m%8ie#pNQd|j=S4BqNNLMI#81=?ELnMLNl&FY^1~3W0lCh9OYDgqrVw=?hiQyE^T_qU}B=YjMy7<mgN)LnD6q1KXO>$ggUhEJ36`^5@nom-Nk2z4>|Dj^I3HlzGP|eR{@*a|8d=kBp_-9gFSrhimx_#iVRp+=IP?fEj_ECvFs6_24Ju9A-4z)Hpslr{X+A>%=^h0;clR>VdA^s^UEd~ah41T2mMPznto&>AYMInBwGN$s`qUJ7|X&o<V*4Gsn;Ibfl%)Xg+Mh`6D)zmCYt69YW1`8Y62JtF!X&a@b-%JJo)?)!=h<X5-A~G<0D3o+#>;W^^!^4Ey%Q`7DkwFm%Xtr!xVP;_hX>$lVIq|*3R+A(RNkemu<}+HEK_o-WTMC&kjnte7m(jHPz~!GTa#m(_kOEERI+k)91QxrW)+4PB>d$i{cJHH(QedKZkBCtyB2Fylf`Uu+TosD_8}uz8gGC3ORQB@H^jM=nReC<fY6U$nHI7!aS_=pbn@4iU<!Y|k)28A%#)uI;Wj=w}B^`cCae+)#11))txRaW{$D~)aBZg>S@mw}ZBep)SwqHrn9I;jnt-U57Dj7IlId7vCDAeJw$CH5cd_N0&rJji*N*U7~Rjo8_3;#4jj7juhRm&**9w33x)47=n5eWQH!)LI3FCoy6Zy3`F_FQ!t>@brl5=EuTDHAj2I%-4s^ViSQZ}XDH5t1Y8H;px9!l?P-4_(wchv(lilRPE5aV-kn<)q2}d8$yIG-F@^4T^~jr^qQtD7l=fx@LNRYyKNiUeUNIhD%1rox43LUy!CiXp*LhlN@y<a&;*UIJ4kt7pscgHB!noF$HcJrxBm@N{|Q&-aufL5;sa0znax+@S@seHTYn+MuH!nM#D4Lo{ub<y0Swg@e7?d)7jBkmdY8+KZNhInw%P~#z)byBuk2?Q`#l-Og1DWy%U!ct;Ro<&w&bFDj=O;M(Y|sBCA;Au``Do;~VpBf=G=j<M|Q;VISm02D@fSTLNRUM9BvyXlU27>zV6SMd!3mK4m*zUv@02oi4_~=-Sl1Vd89IEQm!SQXyBu^)3nhl9#T@V=4ffxZfEWuT1m+3tW$fOHOJ+&X8rH5*{qq*bwt8W%)m))nMg|#UZr1;QnCWY;ztey1u2Ncf@zIge0#86G@l*;6?>Sxd@XbUNo0h%uS_FNb0C+K@L%dPl+B1us(0H1`nV<S_-9|G8mYWrGY8%IBr%Y5%{$n<ibr?KQ$atc(t8Rl8`{y+)A>)DsI>^lR~9o%1#%LFfn3YeO1qCT_l+a8W&3}w?yk|wf1msZBJI3g{ljb5)4ILzGZ2)D>&BQ@a#0rhA381%>Fw>x2SgG3;XYCa#$;bT1fIgq&80wI_{qOpCP~5<NzbYYn4RL5(4_B@xKb^Lv}+AErB#$U<3v+IpUXo^&`>8Fb=r(Xtmi!zPwtERt(o?Xcpj*CcJ@K+(;l%vY`r++JX89@}0TQpXJ36J#JJcF;+vVSV`ex2Qvi_0g8n<c_PL7&W8F}`frImu~cj)Ko5f`c(rgIgrY6$GcZRZ5s)`xZo%nxWDtxO(q>e83ZR@e$gRz=5PegyC*o17G>tnfDy}nEtY9Y%KF~3u`2v3YM}#!2;Z*7L$bVU=z8;}Hw0r_Xoj@d|9FPdt3Nk+okJ>>30&sAxD{l6|-1@o0L*I8<xXFO)as8chJ-T$m@`_<CG8U)&7F3Un^qERuitQB7L*A@yyaA=J!N5#LKaRP~9pDJqv-X7fZtiwry@qb%DNSNm@(CsA5-5Z)BC4g3uAKx}>JprW?S*K)4xOZmHL|J&glM4iwWwBln%tpOLu5x(1PO4_nwDCafF5%jiFN6uxu!~4G|U_1VZpOTt4G<$gVU>>ia~Uqev@Mnm&c$~UAKbvaZa)xXkKg$R<=r2P>G&ieKAT<W7v+K5eAofjo{7QU405xj+7RtIKY4fn=~Sh|BW;Lt#Zgw(4PVjwtH7}4J#~51gP?FHPly%dB^VAQiOe&@e;3hz6YcM$wL8U(;b}$S}2P0+Y-bHfkxXZ_K14Me#ItdF!5&X*XJNH2!GEkbS&N*C0qLC)eD6$R28^TXqD%Z<|Ioi1F8jDm6f9-N~%A+d=>YkUCLmH`pjy2h$q!At9a1tyJbhbGWx?bP2L9dQv)3$BY-OgB%@Sns!twQiMqw$x<+S5B*!$D3he_2DTzJ+@d~5PYUxV<*1mQ!dO$%1pnHxsMuz3mS$5&7tri1L&BswxNmXAhJ3lYQc1hLwi&PN@Bh$=Dos;*eI2PC2L|q7Ut<Y#aPk+z&yk3S-*@aO1;v^ljWKBdsfFHJ=&9@m`Rg|El5Gs#p^m7{7#$mOlrN7yR0Pc$tkEh;{CM_sdZcR?el~E=MA@q<=pchpk36Oml*#sN~VK7lYPs}&4xd<z9cR)*2L->il?7(-@w116dc8Pto+BJIKO3b3^cP#CcK_WcQC(oO>c7So9O;q;h<EMXS5~(p{WA!E{t%-dcrkBeAEUFo6ck3#jZlxMEJgQ>Jw)#oa*ZKZwt+lc9hKeDb*X2gbSM<T^3V!->rw@>>>usJJrS>~1wo`rYY*s<%Zr*XX&Lv1F9`p(tI}vOU@wQRI9;!%kIZe$GOc!-J<-sX>x`(31kr3t)njX~7$dq_!tUW+VUAC$0<o~YTJ(t^F*;kqs4v7S|?{S@ybk!X}BL1Q#0Ew})kyu(wWfVhzhi@UmSL!O@$RvjtPfGhLH7N^YVNs|`%N%3>sUkbeOf|{~g#}(VHxg_3wx+sL20~BQ)OkY{9>V>>!6-!*L)YW-&oZS8l&ztt$nZ`j!sSevC{ZvyE-VWs!p~R{O1XM^ZfXe*Y~;zqzi{NNj#==OK^CV1Dl{?=X<IlhE;A=Y@g;0e_khLJSON0|<Q+p~_&N$L#o{(pE!r!>O84`0({>r3WBg#<u*5m9{#cv1%XzX?wR+5w=tvs4Z3+D_rY4E)(5^XE1Sb_3nuvUMRRlIx-)rXK>i}MIrPsQqz;qNdFU!r!H`FpdnqaP22c=cYI91T*6`-$RQR$Mv)pgj_X_Qx<nX^}cV>-;5f=jridl^V9gUIdaQy$P2x%m|!O!5)+PFyy@S{yN~QsW7J)CU=|fGvQhR5RH`ePLBUf@3R-#`?fw5db<duC&O^SWn?;!X<iQSgW3L>i2^nKUmjEUpF*B5}65IdqQ(`H7Hehgnt7v083Ful96-;Pw8=i1ICRv;Fi9*pUqjW5w2Sv54V<dCzY|)E;6M60nM0`70p|8%&*ee04ECvzzBf?SQRU`U<XZ6HP0bh;z27i=a(i}5Y~R6v>Zy&@v5+g)|U)C9t25HcP;yyAco3*rlhlS%HSp6Mc_=<&bLZi>&k_dgIHT!Z5Y%|0X5Z7sZ|9gOCvmBX?@SA)CO4|RQ-yU7!#VEaMuQCP7!Rzjl|!I;777lDr1U4TTReI6qpiC*<=ph*DhdXf`+*SM=g0y7v*kaTlKKD*}R3cBX;7m_1T5o1rqy+HgiHK-Qg<=JvwgyWpzD!BEJ^OQ?qj~6*N+Uc!Zc&A+QhdsB6hE>Nks^cEq)lBxs1|>#}Ba8>Xgm?&JwV|BrL7<jddpNm8C}MnaBa&h^aIHXehpp(=t`#RAmB0W4_PkVCkLS)`@C0YVcXE*DBy;LE8#Yra}jdCbqVxLss<;{S?4Cp$|YOyZ4`^sU11GNQzeo>X^MDPTJy$H6TLR&toVn<NV9mIoDcBCBg1A(Ua+^1fy1ZhF*lizZl$*+t2(MPAx!8)6i-BELB6^*mdpf=8G%opVjY42{E0;4c)v?O0JV6kNuRv{o0hK3)p#H=j|eL94WfCEQw*7Bt+3uIOD!6szh#&#vE-COZ{ytDD8IO(M%fLu&Dx&AKa_%uv|R=}&R^Wr|eDY-S*x038bJlKx2f`D<F_=X97l2bh@K6OnE3w*Uc*CD8j+nTtFdmkTuwjgZoag8a~OS=31iJ=EO@7OD#ZQaWLknBzBJT13aqs-GHo3Zi2Pp@)8_$U>q}7rRR}he=&VRv~h*g6n>uk@sH5TE=T2A@3N}PJ|~E(?G0Y=!{{&4%1p%by61_9z9}WALSPqVC99A<pLr8fHoy1EhqesD|hv9Y7yvA4T+-(J$p|ph2O7)9ln1-#Z(|ZZO!E?c~f8az{CAhx+WWjjC0;E!PdC2P%L3Cn^<k|-LB8OF*QY`SSW2MxK22q0k&D?Kqa->8YKEO%qgC1dhNCqnQQ?qOaHRm%WMc@K&yTnWi`S8RI|vB02gKq<5_f9L@6<>hO;*SrRec8KO{+|v1<c3Jz>V3fNtM;5y%oioD^S+NYoo4S^hOd$-??i2JjS?xnl$&F`la7ZeH#wC(K!*U{pq?5}Ht!(`GUboiKsn2v}5qJGRUhE%U8qFn~~<HPTn*JTDjYG6w`I$_#PBMw6<UcgJT?pxUy;ztD?ns)Q^r86uwRi#GgG%TH7ewKf>FYQ~D@P6E%2FymCoh86%})wanMowifb<0@PMMD(3jRL}4qS9}HR@`5fhT5kc-Cn%uJ(h$_iy|LzY-X@5~xdPEz4(m3xxu%_Z7NjE3Z1dW-HP7Z+=`u30mnqFSy4B9Z6lp=xWh%-Z^I6y-Q+ACCWU32t(cO$H?M4w1XRDFG@O>tV#cANnF}*BgIM8%oo02%QW=|-TVrGT&Av&yZED_&+OV)UM`fhZYuj(@0tQ*$rtnFr`t_?|$l>~gM%bu!UrloG`YW*qihv&c0pb-yEF><a?Mz}F=&}=5ZUXMJe!YZkEv`)E>;LfK;aBDkM$2P08IeSZ7NDv}?6B2to0KYcS=xPre@i7wu6yYVK62p9(t^FD~Lut%22z&}Fu*yZ>CQ8E^S%5OTQm%Td2{PChT)8NtzD4t@uaGvls}av-mmB4V3Ca9%;fKzbnl23xQMQ3|rPsOOt9^3VmL<k=J&Bk#LN(B=5^MGrC0+x;7Gs4>8^7>ynw67{$S-uE2rZhQ*5!CzK&Ll3V1U<iF9{<w-B&zzy*kf*yhc{8mQ!CSyQliqYkPxYO%Ixkr$;@F@)I7YllA@>dtIAA319C6>Fi=1soT<9$6~d|@az(})xDutk(Z3CG1Lp_R@36mD>94@_|((V5DFX)LpwDmE#cj&i;PLnQo^+oQ*nZPGB#`22!5qetqi)l{Z{6EnXblK&Jqisf}N<&Wd>_rY8y0Mr30^_OrG<~en_DPL7Ll{-dP6>HN%YI1*_6EZ5FRic0D=i6~Dd%RC@6Sq0(38yEYWzb)@gpkf<TbWysYW?krSv_i93hYg`S@p~^K^;Y}=<?y3EeShX!7-@;JsB>s3VDSEKhuX@F6sX-Soek_i$US+ov?R29R*(CKNnky76+aME90ykB{rZ%1Cs*G{J1Y5L4QzGQ{sJ*%BO*R7s5+ox%VuRCNo2bzur9LIj(qx>^sC!gpeoc*-D8x!y8_*$tr{tPqbh8BqV-y|vQt?@F^T|RfffuP13}CKln*`#j4G1!sqgtVssIFfMvVB>SSI%*i#!?u$bR)`=h9N_F6dFS=Y(WRf!(2&`^R`|~l9XC=1@c?~|FZ6RALLReWJ$`o`zRo-i!0i;KDOzxWHn%jun-v1#{&=q@bkH%^B#z<BHqcw@a6ND(b{^*JgD;uKr>e9Qfz*)r)L*f<Z>c5$zm$F^Q3<0r5xVceYIB@`F~K$rV{{iOd=RHaZ&veEKT^kYGf(J9bHzZi=3RL+XVxeFslL^b7}ODSzGY^5ydbnqak39GKJD${<E}KCCjrZEx%S)%d_^K>Obg;5>p_p9!PAxa_z)|r$CF-A`lI?XF3SKVTztI#u``mwOM?<k`Tdx8%_<geiCH8UGuM+OmPwuU@jvo=`Bk31r+s#tA&>+rDEmhv&gezf5y`#RLAzN4zM(VlPOhOmCeqs9utJe%LA?in)gLq<Z8%0!#ThM;zX42<e==HI?-_IfKC|$c1tpBTuHQ^T=S^bXz?MG<n!W?T^5^2pu!EWN=q`Q{P<6M@AT!I>7uJNZaZ9CY6<yT;d!O}?aMLKc?VtOF_euYNlx}vC-U(kk57{zDNi&$oyXd&Dry$F`83w3R)1w3repfO2vh!=N-ssBS#7e2hG$CgoO1tdYa@`&-w2|JXf<}3zFsNXvz1;z`j4cgSq9*$49xkPVIc-80_z&w7@BDWY2d81sJvW9E?z(<jP>|Jju($ni)STF6K7x)Y?i}i0%xWP_ep``Bn1+t81Up$;aFT|@<d5ACeC=x@OrEs5R^#^d74%q@tmq8naeh?qF73LF>Jlkoi7`ZA<U4hB3g?n%O2^H(qCRU*#gh;$s5k7)LR22mx`7u1SUm2t+my*#G+r-X`?}{f}h6rfiId!hBvswMV4oqdRZA^2a`Y+4Y8N3MMJdZ;42hOErBbfUD8$+ST})6L43s2a|Q{Q<O(ZaOzo|laXuHkZk2jB?88A%fhXG#L4vUV4LQjYWGv-BDjPs3R+cz0y()>B!XIV%qDVI)-I+ydKkgS9xYv|RxO~v*1A9ygjlu*4psSp`61UnoB8RGEmvUOL{JU!W4xjkrNk9uRJu%B($W;~DoY(RI0O&LC4Re+A@CGX{*Y2j}BsG~?YBuvn6=X$AnbqrywrjJ&fn7A~C1+bsC|S*<Fo0%B*1gvQmgdxyQAlg%vgn{LBWWGeh+q@QRDf1eP3YJ&4G>B_odS$0v?z4}7q-e+mDZq=q_v*-1xiHbH4?iwS5eYn5Vzv>h*GO(BUZu)REE&tO4y6yU&O4Yf84sakB?e?h;dV`=E;*fFh}<-qfI>g(Nu_)s0UODt7zWQLo5Dt_#p5aOQ7K8pV8E^(Mo)1Y!)nV`UcvC4~n<YvMz0SZ`FIN-e9Z7aWVGKm!-#A<7<@FudbW?*g)<)P%Cv(pA6RTMvmpzYmj*cO(>=m41{HF!ZCM67^@*-@?yZmW5y8`LZreCu@@Z6LPcyWW{?SW$%%Owfw<OW6U#J{fN#t;c{As$fwnMtUI!JAhL$dQ#jj+6hK~>TpX*jLg-U4@yC{NUC^d*CnWz?H4a@)*7p}mhpU(g=;2#u2QHf#|_i@-;gk6BQglhBNy~3(IF_e^&M-8C`PCotyeMS4aS7#+rqRIM7&(B<EcL!D=p|L;J2IPkQSG5n~IaZpY`;+Y=Ho`%>4*RV<i8qx)keSV>soTGA{||QnE?W')).decode('utf-8'))
_LEGACY_ACTIONS_6C12S_4Q_SECOND_YARN = json.loads(zlib.decompress(base64.b85decode('c-rk<U2j`ia{MoP)`Lk=5|uZN&D}9pGcsg*h0Q=143G^11e=FR-h%x1IFd+S-cwy&)#p(5IC{ILDc<vax~r?JfBEl|fBo(EfBgOTlYjc<<cH7iZ{Gd-;ripJ&v%=XhtrdP`|Use<v+jt&zHx4{Pz35|NXzdJpXd?<NL?|)gFHM{I_4Pe}4bd_07rY$=loelhbAM@y8!Gn-7!!__*1;`||PqkDKdHC#RRQkAK?S-2QxWy4ZdF!`<z>&u>5N|Kj4|;eSr29sBV9?O#5B*uQBp>Dw<S_nVKO9^3l!?cJvzAD?y~%^nU1;^XG#X8+c+`CGR?H+dCk$n>@Qr}<Q%2FzX;&K~UHt|gCivN-7L^S8*mKHOZt-9+Pw`m_B5@U~gI$y=ZQWICQrJ03s#dA}GA`uaRm!Pn9e-dxY$zh55LpEh^%MKu5HaP`2YyPPkgkGG%ai>O_kfBL_jaq!8kcWf%#!8sh@*(mM%_xAdEX>Pytv@<7Nx8`y`T<uG@qcHteI$dD@p~(R|p;^J?Eze^Q#%wYi&5X6*(P!*=-09FA{O)|`?T4_PreIwzgu@MNhVW?RXUjnsw2?)JPCj|tmg-|Ef0EB57{cch2Fy`5Z~7qa-m!c5a`t{i58lA-$Gzu=pT9{beeCbk2_Mpd?cYw`H1v1Vhp+Invs>jXuqKnk)VM&#{ObH{b++$|w_t9Mkgqmo#F!Smy}h~Fy#4g+pEh@&-rv0c=fg8$(BPF{Vl0vJJB~C5+gp3mo^TKC9Ff_VgRA`f!LR_o>Gf~S@4Szzx_6t}f1Nf7Fz*`kabkpng<J76fH4C11n$-I(zeWG-iK*#vp%K+2poIEAZ4x!e9C^1jRks2e~@_uqW#$6kH$?dI#BVTO17`Efv9hu&p+{W`dnWHcuIc`ddr6M0F3+nPqxNjzWH0=gxHpO`>dZ!O;v)My|7{Z`fKBVO}_Vm4Yg81?z&+R+Y0UBd<dg2X0Z5|Q}6B;AvMx*$gW!HkgV7bySGjbEdTBl+uqYTYX}jt-gPI?`?bs1pcidrShyV%LXnQsl(pY5o2cbMOooCzMi>1a^-Hl)f?g$qkwb>g!8?btz8~P~^=Dsy_7C{8I)F98)QKbSFod5%PUkj&5`^U2cQ+m^bLTXCrRX&pcuHRYGP8&(Ac%)bIqfG=^<GDoUGTx!{CIu$*QjITZhQkR5Tn>=sCIoR4$*WhdMF0%;IuKw9hsmDNa2IN>)6v<y+KDt)oxIxBbCD;0AD#+cKbED9h7~<Qy%pFFQThv`o4*Qu46EBjt0HYz#A$N=JtnMn$)Y=@cOg8AkledIX!=G{kYv*W9l3e9~X{k^=!m^{B(DH|HJ0)?r*@7DIrX0hr+i*8s>61+{79fG-B~^1T^XeK`86)G|b336ji-TV`QNUJRQr#np!7QtjR-|IH=OKK6VegD?R@?4QJcl$dgTr$*%)Lon79^d<2TCAnLdE@l!La79o0iYG@_I+TL=6@FsAzou8|~gh!*}y#}_vR+#L<!H&*5?V7WP!tp7@%Mu%b7%J#^Rh((+t7l+L<yv8A#pDvazrDSAOpAf0)$@NoPtce1@!d(;*4z8@xVOf~($T4zgN!0Eh_f;u>gZOG4c^09vDfl$B1BLQ#*!}u_7BKZ8f_?)ril3=T6|2suO%3&iyo%?E`98%Hu{+&WfFSZJeBdzO_U$uH4(t3^Kh)!M1(R<I8%p-1>L*A=zKff=;)iD7L{$lh8aESg91*S7C@e-&eRxRz$clRx5u)gF3fD%MJZwj%&!HG*{yP`3}&<1rkY5n(wty9^flvLcwh<2>;;*qK^wr;%&s~e$xwXlY=DA~+gm>PB8MB)vxH4H%;wEgw>|4Yy3=X4UQ7d1;06Ys?V?Tw5(wu1I?1+Xr1D*0iex({xu-pr1=~S1`Bcv}XZfx63WR^qX&lc6G9`e4G1G5g;$O6ZVK5bO8;f9M7%s*=W%f<Q*Z|f+6QXUh;jIyGJ0Ds)r{e#W$d>FK?L%qA+r>@BlDwQH3Io))JD(=ELEHbc&O0`&v}^27ijGnX@&ed5fZW;t*U~&dItsvz+ZOiamdNShUmo7Q|Fem~0{dD|9IwH?fFq*$Dg8{r#T)E)G+^-7hWP3I&0h{(D(G+_D*=9ug~NC6I<o6^mP1Lq>lImbx+Umx^a3Xgl8S&a7&#Zst*tOTIUZGqCv<4O;%Vx?o}SBW3xM?zyf0fUt+jgK)|1Q#Wh)5;jq3(K23kYN;gFqMMRQ7aQ7PeCT|AmsSpvW{Mn~(|?+top^I!sDA2Qjx62RalVJ@x$7CS{|TH7^=a{zCMIYF5AY1&D|RcHqiwVt@nFizG(4pq?S(<D~Y=ni;u3Yeu}Y64@H3@zFQU^8`F!6;_I_2)nnrz@|e8CUFN&{auls+H?&K575Fl2)+StBc<qGL^IQkhKiixr++xhrKr^TOa(Alsh9dayRQ<LnM!;kPZpvc!(1<K7(?|!)s&y@Qvw?86GmE&#Ag@S<HZG+3uwkum~Xeo+e{8P=cYg&vb8^aCp5CXHM}R;!%^}pG694e4#T57QnWKnps(tg&Lg12>|ikDnS7i<T+Qcne=buHwm!96V+^mS0J*mD<BAe;{1~XO5DoG=WTkJxMPVj292*3T5hEYIQSUNh-k?golZJ;#QEqF|B?%1s7KR%3|E2$5NGHH(e#Kh*GHuy5iu5vWD!`}vp(1+p=L~CHDcUc^SE?g7V%a2szbDn*w#a9xzIL{^t*inakeC_7N*)#$I+R?NBps|b~I^LZPbRe3YpEv85-WK`oVK-*GSSfxweJ*zV3?qimd_`>$lLX*M&7;cj{QdG5!4RAp0@g`AT$L3_|PCapK4y!0o;(uX*sYmAo#cumr&ai$`4Xbt?=qJuI%f=TVmgp++ykp9R7t=MRS!%Nhh!gE4!Tgh$1`cx~1}+%ucJR2hmUg?7#~9j@t1#ISp(fHZdzNrDHCYy(gNW!nMxcd;<;0Q}0f-SB%zjg!~!0?oZNZUl|mAaP8=7R*QX@<HdHveBe|Gf4rAQmS!l*C^7VcL2Q|?_$QeC9qYg2Ny9ra`9l$0MJqbP1W!&35v~orb94Pxh~l#J7(OpCS)xA=Jn;^N0a`6oZU%vJkmzcJN^gc+DGKb!@ew6fn?Ppt{1a7H?qys)~UH#G-Vif;mw1dLBz>K6jFtJEihqZ$)T0SyV4=@$tIvmy6w^YLc<&t<4kQzT@R6mi9#CCG|wWO<Y**SodL8g1SMOq)Eq0}(SuuLlp&YkfHp@$$X_<%B_r7R%d;vv!XcAy1u2PY3|mg|(J2sn^qyv$gB|NR{Q31%<XQtKPry$kKR?UCo{m&SUa0k_s~}2|%MpCs+Dg-&>Pf!JvQtx47}+-MhK$@@S!pd4USQb;)KoB(^}NuSyxgeIN$A58)5BBdY1RvKsc1u}lU<|hGJUR=;KNcTD9IgYX$)B+0Cz;PER=L|<OL#417nd<r-LmVPUz@dIH1LBrN<n8O??v%_U1T?s@=o;el!*BXRnfr?SySdd#k#v2sbN93{jew)<23|^C04MD)mXB!{qCo6XALnRCNbos7FgO3X4T`EHdMiO7{b6G0!xMv0{773D=L~p@L#v0$dEg=<L<X@~7+$I_n0uOHNl)YQ6e1;}->D)h6)3OL)r5t|Jc+>U^-)hz$bm0Ut>#ZvYT966<kMq2t3o0RMsF!9*8tIs@x&HP+qHtS7tFX(tTf%^MHXTiOG<%?wFlktCR_$s*ggV!J5zlQ9&h2}2JxA3JNMKJE+z<(NZ-U8RIasDamt3MLq+8oNDzs8Ho=X-<gfkABDz8esAaEKy5U6)@xqNzMkqS~$=ki*UAa@|uVrPvKEAwg^{6Nb=N~93muzM!Fq7N)V`oRHVe9JeOx2T@Vb?1ny8TOJ|&z<BPe1_*1?^=19j-OpXaqBo2F2s1J)7iTmT+KuJU)5H36eI<DR*YV4XV6TYE!<wH#alb3KymJve}x%Zl_`k1@sua~%J5?Y=bK?C5=vO}&=C&jW{!eJ$Mi5<g1qsxn(!uKXPQylQq-g3zrO-lc^zeon-3X8>*>i3wm4akj`Url0T1mN&uL=$FzbLatN3_CIhKF6f>8TwTyTA!`KPlz|yD@_j*k1|CLN_8-EMm#90zgm<s6BY2H6VqZe5=pX!?S*Q}PP<A}xeIEZ6bc*B{5=MV=p-A?z3C(er74E$xVD#Mu_T(sf^OF<8(?;U`}W7`VUUBZineT#jTzB8EA5I61><s2v^0}s&p5%u%1@_BvK+*qCZ|!`j5P{XcVK7_vW-*et_q|m0xRlfFAbdLFH887%AwkfsT(2Q9(2`>8Zt2uu6W^6)<UgVlh`EMHnDJZk!Zw<+#ydKwM&8&i~)6pa@EfQn5jjRDePV2Aozq75m(TQg1mrQrqP(1zkk)Z^$`NF`rbGL1-C3f=CkbmPEW}RD#G;8v89DuJKEI9=<ZJ;;wbwiy1IoP4KK`jF;ypyNA`QfZl&F<I0+1q^!deMeUImVW+@*-y&GLL*H+r7)dobBLaY>?+K!{<>*3VY>SHTX6529N<RZFcAymQF$`ph5?x|PV0QU*Yh;E7?jZ)KE1;l>QORsoIGT|zLkqv&JG~~eHk-YC>d29}LvP7I5T-2Nu7_MhNe&xk9X@sT};N7QUXo~-%RjW}#(F16cN=ixMif@kN-$dTbIre+Lb^iw0QQt&_5@C;G5U(Qxo<%3sq-3yvsKMs4q16zi@|*|`j*z}rIMF(&tc%PE40fIrUerjF)>7JG-Cq*NPA944iSSI998mAtxX|Q)q_&kLEvKjzwP&+_SJR_F=fSfObl=Qb6(6<gj&xSit>=q@T^O?bZ4!v3@xc@^Thl^cWr85#{%6~45bABH4v4LyxHxmjx^n7@T8M%cR!|X?rIS%lb7tL<XDLO6c9S)4<!gC$<cVHm-iLE%(NEim+)B~m=E)-^`N2Xym(E(_+1U~=xlg@w>D&*{{S64z8!xH5a6EzDtla9r34$S!XKB=O&@^2LbYLDX!W)cIpN44hqTZ~9MaM2)hK68u((vnyfZsP|YXMgg0Umz5X$z61&>4M#WOYTLPoq$Xn@IpANA^$2S{jzl-&9{hq@cb|jzPN)etRm|xQ=N3tH#$l{Ae->Wt<63%{N2eFDU&1zkt&LSTb)X%@!y$)g=PB&*(7&0kBXB-BMz{3&kO8P>t56Ev3+c1-OwsZ7qa5?`N@QT>(K2d8(a=WBZW6qKU~+QC4Uk_?;f*%+}J-(^biB`55N&DUY)Ko<g16>o|;^>Es_KpJ_C1rfPkW=36uKd-o#_^j8#q)gd)!leU&J0V#AL;loMJt}a`NMzdY{p%x{s3&LMp*8v`{JcLb)19b}|QpX1!8?;tI=;_(*VqT{_UP(@W8flIvPfN4jy*4<(`U<|R9x7Wi)09ZQNS1y~78Z!zQtcL&%|Q|kY-NL|z>^}}-@8JR6s>4_#`OU0e?`_5@>yi2kJaYosB#Gr1>`F5b7z&wUs)l96#~t17QFi!oDjwa6`W<5rG8eW^LaVy_c9{{+%D{%>?F^l(5PjuM*Ts^T7Rzls8n^}e#?HuGrG1Ek$rfgO@BiP%hM7FYOPhH{G*fW-IaIBY6@_OAahM<&B0DA0XU8AaLa;`eQ5)50j-TP3BZdK3bCbBgnEU#wPRc|?nqK`Akk{}2~SrJsiR%yVR^iZd9NgAyR2E2m|KgBl2#jI+^F(~sy=_Hdn8t()RgT@#geI?5ZmEnLiQ{Lfo>_`@;_XYne<zs_Mt)?A^9a-dW@aQjJv}sB-ZL8*6Kx2%!lGY3SnVLVaky#uM{13aSo6ROVAieVK1XyiDWAo^f(hCg9KoeN+j`m>{LR8<+B<azglZWCG7dRN`t$o@+D}<mcVNSaN8Yak6eT^S3s2sUzp{ITWN!U8V`0W4+dzOPiFDck!yK1tjeguC7FO^FkAXn^^u`xNs=h79CT#J%tLLeQgc8PqLG3uay=NTRuoqtS`>A(O<_OOilUB@h?G3|BV}Symrsu|ODFnRPf(-P7#fMbx+6=B9^)1&Nm%Wk3!<ae8rL$2>phb)vUHtWt<oT1ry0|wC#ST*n@s)Inwv1%B2JB{Ipn2l0n;`Tg^_{S(lpJD)RkbQl6?k_O4WX)>5-f;fjbvxq%N$KmUew&PhMp0jGeEgFkgfo0B$sx%0u(&1%C;w=sqVyxbuK7CD;98E|gpwal}<{)y()=xf%fB@k)g#+4T>}=(_{$_;VdgfHakYwHzO|ln;+;_RV+i|J-foT-7s9#FFLgxZ<Z;+jk=)>XJ>c2qwfwn=++}PRzcu+sR~Q-+ICTR~=+2jpilPAubn^c^sWmzt6;!v38U5l-~^xb13<Nxp;1u6}c39&a2W;FmTM%5za3q@7_%jrVCW~sJMK45zZ-^`4s;+fHRk2knOCo4ouakE(`fPLqBcq;Ovv*^98M(G*Pt3Q#~uP1u>~5v%N)*;dttxhi`)8_Zwsg77Ov-Z(K*Iq8CbYfnxF&3&rEG^)QL)DhH5tVk4R8v2hJtMpMj~U>@>9QtN{DPs+kz2cjg&jj)W2oIwr3*Fm-P)u`U{0l9a@a@(|eHnb~Eu(ja1XX%?PM>-WO(Q49Y>OYapio$C$0tixozM#8gi21N;UZ?>{*f`_R34`t|D0VWVA;pV`0b5-DMit%5aa$NiCLkUKbi~``ShGTpHx@Jyojd7CC~sbz6$(V)4Imie^{H9*;pFLEM{=#z!>TUJqwF1~37yrRODaVL8A4OlW;fK`R=SxNu<c}fo7QFw50Z$1G>`pIr^N-N`_e5d6~0I@R+r_lO-IE~z85EE<4#&i#QDx-m~S-}9lHqN<3C~{s6(l&<*|^v*3AP(+Pu+c;fIAk2}RlZATt-sW0K62+LhO8Ai-82laY&hSZd{!nmGZoNEreun^dhBRV%~7&%4Z_)@9<wj&<s7aS3?Jx!L5fObGx(D#_|{p7aZIo&eLv#%7rLap|0qt;r-M&?cU+UhKL9{z?;Z^~wo)5Q4in<KRnT;xkHNBpDJ_sM=UHe8Sjv%@HHn&3wS~GF!k%bhpu35xj<yLps4&cSU(bJQ9Es3@FOCkYJcxPL5;cC62p7<z)I+sG^gI-ZRml&@wQNzBg9(Sd#hX0x?*0Pv^Rw)$+hHJc$aB6COo)(eY!gB9xXu!f2P^Z^l&pY$A;I>-o9?huaJ_<)eOS)uGlXPTH}>r%)X93ri4#SHsLS?Xndnv60ObR=R0{^pr%FRsc7mjHl1eRaj>`N2n<IS0==Z*tiNWMhTz--_FLUfDqDlmHc7r_yPE>uP?{0@AqQasH!A&Vr7(pnwP8V7kweCSyC?4UP?ACa+m7A3?^2PgUZc5FA0^)Rp;5-84xz)wiuInn$2)<S|oW|Pi?D#5qf5zm6m!h7Ej6!83$epb2EJBk<|&Trs5|zL0}bz3wTyUt+FXKT1>JyS;oT52haO)fr;Qjgsy}o0-kJ|FHYyk)O2teHVfsz)yfsNYZ>tDcxTaB9eA<D%?U+NM1+f#Jfx-E>BVD3tp;UF7WS@Dk2ENAyw!-Ei_#?eO2y(~2k~%gmoJ@NUN9RHDqSYIaNju?mwmbGGS!{IBAV=2rQYYd)H|6gOHV2>jlJ{u!i#n_LO@K)Wt0TskO@{k$k#P1E2FWBvkF&lbCO*SkO)h6>FLNSAv7Z7)o-qp3$M`=`L@g1b~1ap;=5KCs)*>dhYGT<c=6KC;*L=&!w8}xZ?DKfVz<xW6URnB4?N>VTfy-%vR<OI;5*moBX?cFex0}QJp2$YME%eC7VBs4wb^o#UNb4B78l|h&gC--8SsOQ=GPV3ds&m5tX!SSN7%<TQXgZnONeGdcOR3VON{U=cam2m^@ZM;ZEghc5l-8#W}dl5H>FEFS{U#v6N}etjvx+#>Nk1?wp|(=(~2h*f@$79Bb6j|Z;ebON3u#=f?OP*Mxjd-tMeL_$CL*U8KsH>zAA$_z4pa@27{8!kYy(^7xpo8;*uh3SEX`#h^(wtiV!O}aHHNPZM3V9vqpBSZmW6~;qp1MZ61JWs$W$zpOLS&1MsEWcel})hy-;fP>y`G^O2oSq7hm9QwjmsFHIRGml0FvO+E<Eb0t?%&`Jy>>OTaD5fiahDXsHrGBT@@D-}@iYsrRa|51hT$U!Z!T*PA<9s1i-aR~HFq+CU1JXSVB;~8qYf5G$%R8x}rxQ@<%j-^4tNc6OwP>nUq%}co8`r;zV0^sMqm>9;_z9PRcNaA*>?th!6`8<5*4Mw?UM4#`3z4>&f9+keCh000LrI76sOCA>3ovP}eRo;Ns>|L8Vn1a8ogL4)Qv{<0TL0y&AHMW#U?$GoCgRMI~eqH8ZR%d+`1*&qCsI}@;a2b+^0^c#0SUES2z^v&$?935^TG<;VHcb|#O4Co)Y+iloIsDstgrZk**~flt&8Ze7r4>-Kxjl?;uY;u$S9%wR;YuM2u8mb51n4h>G(Sq*b>YcKFNvVd7sfgd1xw_@2m+Eh1pOx{7wZIu^YM)EGGl!qfU~~-#5!CnCz;5cqnJS+vq+4flv<vX5y<mdl{89Eg9PTD;67hYqN=;@Vb60o+ckLUu%Qz^r34rnhG!RuW~@1$cEXTwohChuOQ(SYjN2@71!Fp-$o2Q@3oI?eWnB&nXgqK2(#vv@_<T#zfOTKk4&W2GsYLy;ss1u#zSqSFa!~~qgt^eR-S)Mk>WP<`a8a)j0)(&%*yjZP#km}D?5|FRUXPD)b#XVtNjoM0x<as~`Qfqnn3hi17)~jpW?uN3(`|&Mo!5djmlVxN@*EjFVChY9h3tazVg^h&$%`d~=CYJLpyvL|3?iayP&`F?v>?P7L06`Kr`VR1Fl~uUw8Makb?P-?%W>&dX-THod0W3YkasF%Yz~~l(;h`k8W&>%IDxtntJs_x*UPIu1&YIVD5PxUCC(~hj;zT8wpY4Pnr#=4JkFkAuJOjc&?F6aR@<7()S1O;6%EUBZBioEN%Mon9KMktE0tLT{)b%)sofMtSoo}>szWMMQCvGOk1#}+lDWJf52EGkYn3#(Vw9Y7u&nQb!kr$~URA5Ej}fShFMOeBY7p)s)T_3KD(R)|%&PBF=g^r}ewLuaQV-42s=Q+GMwe2wD6XzN*jarWQC(B7P)J<mxsHbQW*x}>k6qhFF&7FeP+_Q2@g!j8GWz~@(h@b{-V=Q}NGNg%?!b%x2Z_%|6ohoWWYmQ*nvm79wy{LQu!6jKfZu6+2DX%(IFDso$9wQ{iuD#WZB$i;wr8d3G^*a3zPSwKsz&_-o{}gRkE#}=Dvm3I`Xy2Pcxg^>Wbt^p8ZEpW#NLD1<sMBm!SY*$hEhcng@*@H@ieqet9U}9Dyu%6o0Phy@;B+6=_h+u*0(Gp$Cz|{o>B>Y$7jFlqnG6;sg@@ru$9UiqFC3RWcG0`P)wa6J7pO%$@)r^WbB>L+i{dvY_6HASVzQts9Xsx>L@XiiaGyhW$G1!tf@AiR5+lPZ&!<JStU_L`4a|J7?rawZGO$dsXl6hT$HL>%#nQ4kt9o8r3UmN>7ZhggS6+;^?2HW`WqE&_0>zskx$bjGG6=0kp4o}5KFfjiLE<$K7tsxl9(_pD#l<nO1KV#)nk|ueYCYVl!L#e&@H>kZTe>X`c;Ley!V#@=)^o<w9JHLg!P!xEl&1s4%9`)HOkw%tmY>y`uJZKSXPmiQ>9*(%R#)bq5Y8AMQ*b1g%M>`mT-R|4MV7IqcTgeK~@6=b>T_P?dAhgWW2080YjZ)s+4Z7a^0>5A&DthL5mJE>V_136hJC3r<WD@NaB@R4cqj%)CGb<%ZJ7s6l7A>h5@RWG3#MaZR-|D$lwrKJe^ki?5t|Zn4U@UCMyoqz{NA8*eWHev^v?ZXnciA?mTt4k~n)W5I8||fXUR_g;q37Nu|i@dud>&lSbi`4cR@2KuDzg$lZmy9Ihk#m{;M}Fc7Ab+eLz`CUeruhld`y(`IV@9;r}nlny{t7jg;1A=<vwuqBRemWiqA7(W6$BW8q<&(dNu>`0aM0wWOJ>D)e7vTwc7Vt&*-A3#1oT8ZLBRu_~*Ily0It+hXr99|QA{AP<8b2kV!$tqltu%3$bMP)3=NvusGE|!v=7QR-%bw*38jG2-`YgVF=giMO1cWF$)s5VumWdW_N){UnQ7q+|y!GBk^LdarqjQk`CKN>}pQ_30x?~jyjiI)GdW<;sBP0MaGci}z{4R<adozW)b|49OVeQJuUvVTLUN#ws2ij!K2Q}>*cZAn>XQk6n!@l**&#LL$}tVG7Fcf8wOz}bW}J^(oo0jGgz8j8Bh!>d@pDrjJGq>{9Snibu8TyDu(tqQH8iZW76-q1ZED=!yhtZf)Eb(vFkC_gPToIEXx?(Lyf7dNU#*@e5!+)S1l-x7EjZAamBmEl)sT`^IFHqo+8evb>-4b6%bYeX>VYD5hiR7`nL&14%VdXDQylx-k*x;%^Oy8@K^vI}(qeBAFV%h6ELmLldg!7O_ERf#B><pjNkm2+H<$Og=AF(~}u!7>tKgqhn$2GIPMt-`BR>pZdVX|TOggf{_GGptps_$cMvf_sCBm(eRFtE2}_jRKC5+p87@+FC~H%!$s3e1n$iz)?_M3jTnGTFqlbev!nUMCv>TZ(-JwOaUcZ|GGHO5>J-qin3{L&cuOhFbmX+vQj46;!bpS@N?l9?l)WQ{BZs8W9W-K{ohQ`eET6Y<ab}1xWA7db+!#Qq<!ErTt{jfY0rMl_Q+Dy3h=ELXc(U1wzac|7id}G;k8vqYSkPvqS1^sW<bD*wpvoKk3*4Ed@a<I5MNAbXEf%Xad2~QfQMO9bCHTkm0V_q1ZmlJd8d)gnU)RCm~n#Z#c%zLTb&Gi?p`G;{GJ@~l37k(-JV!T{0-eVaIw$K4C}>cHi2!>S~BEp%zF#{2J(*ZcC}s$H!$lgF`=v%@BX%ZYi>6Tf2C*`_Pi7rYPD<Du)y1nwhz&Fim#Nq8Ll+zrTbXT-R+0$1<@x&hi8q7+*SM^RGNxxv3x8DMAx1eOrDPnM*2$HQC>{U=<4&_PE+ff+1`CZ9%f%w<1gEJf0Ng4Jd(|QI5rRe3!QmfDg')).decode('utf-8'))

_ACTIONS = _ACTIONS_8C6S_3Q
_FR_ITEMS = (
    "MELON",
    "MILK",
    "STRAWBERRY",
    "WOOL",
    "FERTILIZER",
    "WHEAT",
)
_FR_STATE = {
    0: {"last_step": -1, "due_step": -1, "due": {}},
    1: {"last_step": -1, "due_step": -1, "due": {}},
}
_WEED_STATE = {0: {}, 1: {}}
_WEED_REPLAY_STEPS = 8
_SHOP_PRODUCTS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}


def _get(value, key, default=None):
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _copy_action(action):
    action = copy.deepcopy(action or {})
    return {
        "farmer": list(action.get("farmer") or ["PASS"]),
        "hands": [list(order or ["PASS"]) for order in (action.get("hands") or [])],
        "market": [list(order) for order in (action.get("market") or [])],
    }


def _seat(obs):
    return 1 if int(_get(obs, "player", 0) or 0) == 1 else 0


def _farm(obs, seat):
    farms = list(_get(obs, "farms", []) or [])
    return farms[seat] if seat < len(farms) else {}


def _align_hands(action, obs):
    action = _copy_action(action)
    expected = len(_get(_farm(obs, _seat(obs)), "hands", []) or [])
    hands = list(action.get("hands") or [])
    if len(hands) < expected:
        hands.extend([["PASS"] for _ in range(expected - len(hands))])
    action["hands"] = [list(order or ["PASS"]) for order in hands[:expected]]
    return action


def _clip_seed_surplus(action, obs, step):
    """Remove only opening or carrot seed orders the route cannot consume."""
    step = min(max(0, int(step)), len(_ACTIONS) - 1)
    if step == 0:
        demand = {}
        for future in range(step, min(len(_ACTIONS), 24)):
            trace = _ACTIONS[future] or {}
            for order in [
                trace.get("farmer") or ["PASS"],
                *list(trace.get("hands") or []),
            ]:
                if len(order) >= 2 and order[0] == "PLANT":
                    demand[order[1]] = demand.get(order[1], 0) + 1
        seeds = _get(_get(obs, "private", {}) or {}, "seeds", {}) or {}
        action = _copy_action(action)
        market = []
        remaining = {
            crop: max(
                0,
                int(quantity)
                - max(0, int(_get(seeds, crop, 0) or 0)),
            )
            for crop, quantity in demand.items()
        }
        for order in action.get("market") or []:
            if len(order) < 3 or order[0] != "BUY_SEED":
                market.append(order)
                continue
            crop = order[1]
            required = remaining.get(crop, max(0, int(order[2] or 0)))
            order[2] = min(max(0, int(order[2] or 0)), required)
            remaining[crop] = max(0, required - order[2])
            if order[2] > 0:
                market.append(order)
        action["market"] = market
        return action
    crops = {
        order[1]
        for order in (action.get("market") or [])
        if len(order) >= 3
        and order[0] == "BUY_SEED"
        and order[1] == "CARROT"
    }
    if not crops:
        return action
    required_now = {}
    seeds = _get(_get(obs, "private", {}) or {}, "seeds", {}) or {}
    for crop in crops:
        stock = max(0, int(_get(seeds, crop, 0) or 0))
        current_trace = _ACTIONS[step] or {}
        current_plants = sum(
            len(order) >= 2
            and order[0] == "PLANT"
            and order[1] == crop
            for order in [
                current_trace.get("farmer") or ["PASS"],
                *list(current_trace.get("hands") or []),
            ]
        )
        current_orders = sum(
            max(0, int(order[2] or 0))
            for order in (action.get("market") or [])
            if len(order) >= 3 and order[:2] == ["BUY_SEED", crop]
        )
        # PLANT is atomic per crop and resolves before the market.  If the
        # current request is under-stocked, every current PLANT of that crop
        # fails and the existing stock remains available for later turns.
        balance = stock - current_plants if stock >= current_plants else stock
        deficit = 0
        for future in range(step + 1, len(_ACTIONS)):
            trace = _ACTIONS[future] or {}
            unit_actions = [
                trace.get("farmer") or ["PASS"],
                *list(trace.get("hands") or []),
            ]
            plants = sum(
                len(order) >= 2
                and order[0] == "PLANT"
                and order[1] == crop
                for order in unit_actions
            )
            balance -= plants
            deficit = max(deficit, -balance)
            balance += sum(
                max(0, int(order[2] or 0))
                for order in (trace.get("market") or [])
                if len(order) >= 3 and order[:2] == ["BUY_SEED", crop]
            )
        required_now[crop] = min(current_orders, max(0, deficit))
    action = _copy_action(action)
    market = []
    remaining = dict(required_now)
    for order in action.get("market") or []:
        if len(order) < 3 or order[0] != "BUY_SEED":
            market.append(order)
            continue
        item = order[1]
        required = remaining.get(item, max(0, int(order[2] or 0)))
        order[2] = min(max(0, int(order[2] or 0)), required)
        remaining[item] = max(0, required - order[2])
        if order[2] > 0:
            market.append(order)
    action["market"] = market
    return action


def _tile_at(farm, position):
    try:
        x, y = int(position[0]), int(position[1])
        return (_get(farm, "tiles", []) or [])[y][x]
    except (IndexError, TypeError, ValueError):
        return "LOCKED"


def _trace_actor_action(step, actor):
    trace = _ACTIONS[min(max(int(step), 0), len(_ACTIONS) - 1)] or {}
    if actor == "farmer":
        return list(trace.get("farmer") or ["PASS"])
    hands = trace.get("hands", []) or []
    return list(hands[actor] if actor < len(hands) else ["PASS"])


def _weed_repair_action(obs, action, step):
    action = _align_hands(action, obs)
    seat = _seat(obs)
    game = _WEED_STATE[seat]
    if step == 0 or step < int(game.get("last_step", -1)):
        game = {
            "last_step": step,
            "active": {},
            "post_recovery_market_regime": False,
        }
        _WEED_STATE[seat] = game
    game["last_step"] = step
    farm = _farm(obs, seat)
    positions = [_get(farm, "farmer"), *list(_get(farm, "hands", []) or [])]
    unit_actions = [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]
    active = game.setdefault("active", {})
    # The engine resets all workers to the shed at each day boundary.  A
    # delayed route replay is position-dependent, so carrying it into hour 0
    # would execute yesterday's movements from the wrong location.
    if step > 0 and int(_get(obs, "hour", step % 24) or 0) == 0:
        active.clear()

    for actor, transaction in list(active.items()):
        index = 0 if actor == "farmer" else int(actor) + 1
        if index >= len(unit_actions):
            active.pop(actor, None)
            continue
        age = step - int(transaction["start"])
        if age == 1:
            unit_actions[index] = list(transaction["intended"])
        elif 2 <= age <= 1 + _WEED_REPLAY_STEPS:
            delayed = _trace_actor_action(step - 1, actor)
            unit_actions[index] = delayed
            if delayed and delayed[0] in ("NORTH", "SOUTH", "WEST", "EAST"):
                # Rejoin early only when the first delayed move reaches an
                # in-bounds visible empty tile. Movement has no unit collision
                # rule, so the move is executable; the current raw-route
                # action is deliberately discarded to regain the timetable.
                # An occupied destination can still need the next delayed
                # WATER/CARE action, so its bounded replay is preserved.
                if not transaction.get("first_move_seen", False):
                    transaction["first_move_seen"] = True
                    try:
                        x, y = int(positions[index][0]), int(positions[index][1])
                        dx, dy = {
                            "NORTH": (0, -1),
                            "SOUTH": (0, 1),
                            "WEST": (-1, 0),
                            "EAST": (1, 0),
                        }[delayed[0]]
                        destination = _tile_at(farm, (x + dx, y + dy))
                    except (IndexError, KeyError, TypeError, ValueError):
                        destination = "LOCKED"
                    if destination is None:
                        game["post_recovery_market_regime"] = True
                        active.pop(actor, None)
                    else:
                        transaction["preserve_bounded_replay"] = True
                elif not transaction.get("preserve_bounded_replay", False):
                    game["post_recovery_market_regime"] = True
                    active.pop(actor, None)
        else:
            active.pop(actor, None)

    for index, (position, intended) in enumerate(zip(positions, unit_actions)):
        actor = "farmer" if index == 0 else index - 1
        if actor in active or not isinstance(intended, list) or not intended:
            continue
        if intended[0] not in ("BUILD_PASTURE", "PLANT"):
            continue
        tile = _tile_at(farm, position)
        if not isinstance(tile, dict) or tile.get("kind") != "WEED":
            continue
        active[actor] = {"start": step, "intended": list(intended)}
        unit_actions[index] = ["DIG"]

    action["farmer"] = unit_actions[0] if unit_actions else ["PASS"]
    action["hands"] = unit_actions[1:]
    return _align_hands(action, obs)


_PASSIVE_WEED_NOOPS = {"PASS"}


def _clear_passive_weeds(obs, action):
    """Turn only otherwise-certain tile no-ops on visible weeds into DIG."""
    action = _align_hands(action, obs)
    farm = _farm(obs, _seat(obs))
    positions = [_get(farm, "farmer"), *list(_get(farm, "hands", []) or [])]
    unit_actions = [
        action.get("farmer", ["PASS"]),
        *list(action.get("hands") or []),
    ]
    for index, (position, intended) in enumerate(zip(positions, unit_actions)):
        if not isinstance(intended, list) or not intended:
            continue
        tile = _tile_at(farm, position)
        if (
            isinstance(tile, dict)
            and tile.get("kind") == "WEED"
            and intended[0] in _PASSIVE_WEED_NOOPS
        ):
            unit_actions[index] = ["DIG"]
    action["farmer"] = unit_actions[0] if unit_actions else ["PASS"]
    action["hands"] = unit_actions[1:]
    return _align_hands(action, obs)


def _fr_state(obs, step):
    seat = _seat(obs)
    state = _FR_STATE[seat]
    if step == 0 or step < int(state.get("last_step", -1)):
        state = {"last_step": step, "due_step": -1, "due": {}}
        _FR_STATE[seat] = state
    state["last_step"] = step
    if 0 <= int(state.get("due_step", -1)) < step:
        state["due_step"], state["due"] = -1, {}
    return state


def _town_demand_now(obs, item, step):
    demand = 1 if item != "FERTILIZER" and step % 24 == 0 else 0
    if step % 4 != 0:
        return demand
    town = _get(obs, "town", {}) or {}
    for shop in list(_get(town, "unlocked_shops", []) or []):
        products = _SHOP_PRODUCTS.get(shop, ())
        if item in products:
            demand += 2 if len(products) == 1 else 1
    return demand


def _future_quantity(step, item):
    future = step + 1
    if not 0 <= future < len(_ACTIONS):
        return 0
    return sum(
        max(0, int(order[2]))
        for order in (_ACTIONS[future].get("market") or [])
        if len(order) >= 3 and order[0] == "SELL" and order[1] == item
    )


def _pickup_reserve(action, item):
    reserve = 0
    for order in [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]:
        if isinstance(order, (list, tuple)) and len(order) >= 2 and order[0] == "PICKUP" and order[1] == item:
            try:
                reserve += max(0, int(order[2])) if len(order) >= 3 else 1
            except (TypeError, ValueError):
                reserve += 1
    return reserve


def _existing_sell(action, item):
    return sum(
        max(0, int(order[2]))
        for order in (action.get("market") or [])
        if len(order) >= 3 and order[0] == "SELL" and order[1] == item
    )


def _repay(action, state, step):
    if int(state.get("due_step", -1)) != step:
        return action
    due = {str(item): max(0, int(quantity)) for item, quantity in dict(state.get("due", {})).items()}
    action = _copy_action(action)
    market = []
    for raw in action.get("market") or []:
        order = list(raw)
        if len(order) >= 3 and order[0] == "SELL" and order[1] in due and due[order[1]] > 0:
            requested = max(0, int(order[2]))
            reduction = min(requested, due[order[1]])
            requested -= reduction
            due[order[1]] -= reduction
            if requested <= 0:
                continue
            order[2] = requested
        market.append(order)
    action["market"] = market[:10]
    state["due_step"], state["due"] = -1, {}
    return action


def _front_run(action, obs, state, step, prepaid=None):
    if not _FR_ITEMS:
        return action
    prepaid = prepaid or {}
    private = _get(obs, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    moved = {}
    action = _copy_action(action)
    for item in _FR_ITEMS:
        target = max(
            0,
            _future_quantity(step, item)
            - max(0, int(prepaid.get(item, 0) or 0)),
        )
        if target <= 0 or _town_demand_now(obs, item, step) > 0:
            continue
        stock = max(0, int(_get(shed, item, 0) or 0))
        reserve = _pickup_reserve(action, item) + _existing_sell(action, item)
        quantity = min(target, max(0, stock - reserve))
        if quantity <= 0:
            continue
        market = [list(order) for order in (action.get("market") or [])]
        existing = next((order for order in market if len(order) >= 3 and order[0] == "SELL" and order[1] == item), None)
        if existing is not None:
            existing[2] = max(0, int(existing[2])) + quantity
        elif len(market) < 10:
            market.insert(0, ["SELL", item, quantity])
        else:
            continue
        action["market"] = market[:10]
        moved[item] = moved.get(item, 0) + quantity
    if moved:
        state["due_step"] = step + 1
        state["due"] = moved
    return action


_ENABLE_NINTH_COW = False
# V16-RC5-R5: bounded, public-state COW placement recovery.
_COW_ALIGN_STATE = {
    0: {"last_step": -1, "active": {}},
    1: {"last_step": -1, "active": {}},
}


def _empty_cow_pasture(tile):
    return (
        isinstance(tile, dict)
        and tile.get("kind") == "PASTURE"
        and not tile.get("animal")
    )


def _adjacent_cow_pasture_move(farm, position):
    try:
        x, y = int(position[0]), int(position[1])
    except (IndexError, TypeError, ValueError):
        return None
    for operation, dx, dy in (
        ("EAST", 1, 0),
        ("WEST", -1, 0),
        ("SOUTH", 0, 1),
        ("NORTH", 0, -1),
    ):
        if _empty_cow_pasture(_tile_at(farm, (x + dx, y + dy))):
            return [operation]
    return None


def _cow_inventory(obs, actor_index):
    private = _get(obs, "private", {}) or {}
    inventories = list(_get(private, "inventories", []) or [])
    if actor_index >= len(inventories):
        return 0
    return max(
        0,
        int(_get(inventories[actor_index] or {}, "COW", 0) or 0),
    )


def _is_cow_place(order):
    return (
        isinstance(order, (list, tuple))
        and len(order) >= 2
        and order[0] == "PLACE"
        and order[1] == "COW"
    )


def _cow_place_alignment(obs, action, step):
    action = _align_hands(action, obs)
    seat = _seat(obs)
    state = _COW_ALIGN_STATE[seat]
    if step == 0 or step < int(state.get("last_step", -1)):
        state = {"last_step": step, "active": {}}
        _COW_ALIGN_STATE[seat] = state
    state["last_step"] = step
    active = state.setdefault("active", {})
    if step % 24 == 0:
        active.clear()

    farm = _farm(obs, seat)
    positions = [
        _get(farm, "farmer"),
        *list(_get(farm, "hands", []) or []),
    ]
    unit_actions = [
        action.get("farmer", ["PASS"]),
        *list(action.get("hands") or []),
    ]

    for actor, transaction in list(active.items()):
        actor_index = 0 if actor == "farmer" else int(actor) + 1
        if actor_index >= len(unit_actions):
            active.pop(actor, None)
            continue
        age = step - int(transaction["start"])
        if age == 1:
            unit_actions[actor_index] = ["PLACE", "COW", 1]
        elif age >= 2:
            unit_actions[actor_index] = _trace_actor_action(step - 1, actor)

    if 0 <= step <= 280:
        for actor_index, (position, intended) in enumerate(
            zip(positions, unit_actions)
        ):
            actor = "farmer" if actor_index == 0 else actor_index - 1
            if actor in active or not _is_cow_place(intended):
                continue
            if _cow_inventory(obs, actor_index) <= 0:
                continue
            if _empty_cow_pasture(_tile_at(farm, position)):
                continue
            movement = _adjacent_cow_pasture_move(farm, position)
            if movement is None:
                continue
            active[actor] = {"start": step}
            unit_actions[actor_index] = movement

    action["farmer"] = unit_actions[0] if unit_actions else ["PASS"]
    action["hands"] = unit_actions[1:]
    return _align_hands(action, obs)


def _owned_cows(obs):
    seat = _seat(obs)
    farm = _farm(obs, seat)
    total = 0
    for row in list(_get(farm, "tiles", []) or []):
        for tile in list(row or []):
            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PASTURE"
                and tile.get("animal") == "COW"
            ):
                total += 1
    private = _get(obs, "private", {}) or {}
    total += max(0, int(_get(_get(private, "shed", {}) or {}, "COW", 0) or 0))
    for inventory in list(_get(private, "inventories", []) or []):
        total += max(0, int(_get(inventory or {}, "COW", 0) or 0))
    return total


def _cow_target_after_buy(step):
    """Return the selected route's cumulative cow target at a buy step."""
    step = int(step)
    current = _ACTIONS[step] if 0 <= step < len(_ACTIONS) else {}
    if not any(
        len(order) >= 3 and order[:2] == ["BUY_ANIMAL", "COW"]
        for order in (current.get("market") or [])
    ):
        return None
    return sum(
        max(0, int(order[2] or 0))
        for action in _ACTIONS[: step + 1]
        for order in (action.get("market") or [])
        if len(order) >= 3 and order[:2] == ["BUY_ANIMAL", "COW"]
    )


def _reconcile_scheduled_cows(obs, action, step):
    """Increase an existing cow order after an earlier partial purchase.

    BUY_ANIMAL executes per unit, so a two-cow order can silently buy only
    one when cash is a few dollars short.  Later route turns already contain
    the matching placement slots; enlarging a later scheduled order restores
    the selected route's observable herd target without adding a market slot
    or buying beyond its cumulative plan.
    """
    target = _cow_target_after_buy(step)
    if target is None:
        return action
    missing = max(0, target - _owned_cows(obs))
    if missing <= 0:
        return action
    action = _copy_action(action)
    for order in action.get("market") or []:
        if len(order) >= 3 and order[:2] == ["BUY_ANIMAL", "COW"]:
            order[2] = max(max(0, int(order[2] or 0)), missing)
            break
    return action


def _guarded_demand_cow9(obs, action, step):
    if not _ENABLE_NINTH_COW or step != 289 or _owned_cows(obs) != 8:
        return action
    farms = list(_get(obs, "farms", []) or [])
    opponent_index = 1 - _seat(obs)
    opponent = farms[opponent_index] if opponent_index < len(farms) else {}
    opponent_cows = sum(
        1
        for row in list(_get(opponent, "tiles", []) or [])
        for tile in list(row or [])
        if isinstance(tile, dict) and tile.get("animal") == "COW"
    )
    if opponent_cows < 9:
        return action
    shops = list(
        _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
    )
    milk_demand = sum(
        shop in ("PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP")
        for shop in shops
    )
    farm = _farm(obs, _seat(obs))
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    milk_price = float(_get(prices, "MILK", 0) or 0)
    money = float(_get(farm, "money", 0) or 0)
    if (
        milk_demand < 3
        or not math.isfinite(milk_price)
        or not math.isfinite(money)
        or not milk_price >= 225
        or not money >= 800
    ):
        return action
    action = _copy_action(action)
    market = [list(order) for order in (action.get("market") or [])]
    if len(market) >= 10 or any(
        len(order) >= 2
        and order[0] == "BUY_ANIMAL"
        and order[1] == "COW"
        for order in market
    ):
        return action
    market.append(["BUY_ANIMAL", "COW", 1])
    action["market"] = market[:10]
    return action


# The second-order market counter uses the selected route's own premium-sale
# schedule.  Only public market and farm state can activate its H7 prepayment.
_META_SALES = {}
_META_ITEMS = ("MELON", "STRAWBERRY", "MILK", "WOOL")
_META_BASE_PRICE = {"MELON": 250, "STRAWBERRY": 120, "MILK": 160, "WOOL": 200}
_META_GLUT_WEIGHT = {"MELON": 3.5, "STRAWBERRY": 2.0, "MILK": 2.0, "WOOL": 3.2}
_META_HORIZON = 4
_META_H5_LEAD = 7


def _new_meta_state():
    return {
        "last_step": -1,
        "clone_confidence": 0,
        "h4_active": False,
        "h4_evidence": 0,
        "h5_due": {},
        "prev_market_inv": None,
        "prev_town_shops": (),
        "prev_action": None,
        "prev_shed": None,
        "prev_prices": None,
        "prev_step": -1,
    }


_META_STATE = {0: _new_meta_state(), 1: _new_meta_state()}


def _meta_state(obs, step):
    seat = _seat(obs)
    state = _META_STATE[seat]
    if step == 0 or step <= int(state.get("last_step", -1)):
        state = _new_meta_state()
        _META_STATE[seat] = state
    return state


def _meta_public_signature(farm):
    counts = {
        item: 0
        for item in (
            "COW", "SHEEP", "GOOSE", "WHEAT", "CARROT", "TOMATO",
            "STRAWBERRY", "MELON", "PASTURE", "COOP", "WEED",
        )
    }
    for row in _get(farm, "tiles", []) or []:
        for tile in row or []:
            if not isinstance(tile, dict):
                continue
            for key in ("animal", "crop", "kind"):
                value = tile.get(key)
                if value in counts:
                    counts[value] += 1
                    break
    positions = [
        _get(farm, "farmer", [0, 0]),
        *list(_get(farm, "hands", []) or []),
    ]
    return (
        len(_get(farm, "hands", []) or []),
        tuple(sorted(_get(farm, "unlocked_quadrants", []) or [])),
        tuple(sorted(tuple(position) for position in positions)),
        tuple(counts[item] for item in sorted(counts)),
    )


def _meta_signature_distance(left, right):
    distance = abs(left[0] - right[0])
    distance += 3 * abs(len(left[1]) - len(right[1]))
    distance += sum(abs(a - b) for a, b in zip(left[3], right[3]))
    if left[2] != right[2]:
        distance += 2
    return distance


def _meta_update_clone_profile(obs, step, state):
    if step not in (4, 24) and not (step >= 48 and step % 24 == 0):
        return
    farms = list(_get(obs, "farms", []) or [])
    if len(farms) < 2:
        return
    player = _seat(obs)
    distance = _meta_signature_distance(
        _meta_public_signature(farms[player]),
        _meta_public_signature(farms[1 - player]),
    )
    confidence = int(state.get("clone_confidence", 0))
    if distance <= 1:
        confidence = min(8, confidence + 1)
    elif distance <= 4:
        confidence = max(0, confidence - 1)
    else:
        confidence = max(0, confidence - 3)
    state["clone_confidence"] = confidence


def _meta_sell_qty(action, item):
    return sum(
        max(0, int(order[2] or 0))
        for order in (action or {}).get("market", []) or []
        if (
            isinstance(order, list)
            and len(order) >= 3
            and order[0] == "SELL"
            and order[1] == item
        )
    )


def _meta_trace_sell_qty(step, item):
    return max(0, int((_META_SALES.get(step) or {}).get(item, 0) or 0))


def _meta_town_demand(step, shops, item):
    demand = 0
    if step % 4 == 0:
        for shop_name in shops or ():
            products = _SHOP_PRODUCTS.get(shop_name, ())
            if item in products:
                demand += 2 if len(products) == 1 else 1
    if step % 24 == 0 and item != "FERTILIZER":
        demand += 1
    return demand


def _meta_remember_market(obs, step, action, state):
    market = _get(obs, "market", {}) or {}
    state["prev_market_inv"] = dict(_get(market, "inventory", {}) or {})
    state["prev_prices"] = dict(_get(market, "prices", {}) or {})
    town = _get(obs, "town", {}) or {}
    state["prev_town_shops"] = tuple(
        _get(town, "unlocked_shops", []) or []
    )
    state["prev_action"] = copy.deepcopy(action)
    private = _get(obs, "private", {}) or {}
    state["prev_shed"] = dict(_get(private, "shed", {}) or {})
    state["prev_step"] = step


def _meta_observe_h4(obs, step, state):
    prev_market = state.get("prev_market_inv")
    prev_action = state.get("prev_action")
    prev_shed = state.get("prev_shed")
    prev_step = int(state.get("prev_step", -1))
    if (
        state.get("h4_active")
        or prev_market is None
        or prev_action is None
        or prev_shed is None
        or prev_step != step - 1
        or int(state.get("clone_confidence", 0)) < 3
    ):
        return

    market = _get(obs, "market", {}) or {}
    current_inventory = _get(market, "inventory", {}) or {}
    current_prices = _get(market, "prices", {}) or {}
    previous_prices = state.get("prev_prices") or {}
    for item in _META_ITEMS:
        if float(previous_prices.get(item, 2) or 0) <= 1:
            continue
        if float(current_prices.get(item, 2) or 0) <= 1:
            continue
        target = prev_step + 4
        if _meta_trace_sell_qty(target, item) <= 0:
            continue
        if _meta_trace_sell_qty(prev_step, item) > 0:
            continue
        if any(
            _meta_trace_sell_qty(candidate, item) > 0
            for candidate in range(prev_step + 1, target)
        ):
            continue
        own_requested = _meta_sell_qty(prev_action, item)
        own_supply = min(
            max(0, int(prev_shed.get(item, 0) or 0)),
            own_requested,
        )
        if own_supply < 2:
            continue
        demand = _meta_town_demand(
            prev_step,
            state.get("prev_town_shops") or (),
            item,
        )
        observed_delta = int(current_inventory.get(item, 0) or 0) - int(
            prev_market.get(item, 0) or 0
        )
        opponent_supply = observed_delta + demand - own_supply
        if (
            opponent_supply >= 2
            and 0.40 <= opponent_supply / max(1, own_supply) <= 2.50
        ):
            state["h4_evidence"] = int(state.get("h4_evidence", 0)) + 1
            state["h4_active"] = True
            return


def _meta_h5_counter(action, obs, step, state):
    if not state.get("h4_active"):
        return False
    target = step + _META_H5_LEAD
    if target >= len(_ACTIONS):
        return False
    orders = [list(order) for order in action.get("market", []) or []]
    if len(orders) >= 10:
        return False
    already = {}
    for order in orders:
        if len(order) >= 3 and order[0] == "SELL":
            already[order[1]] = already.get(order[1], 0) + max(
                0, int(order[2] or 0)
            )
    private = _get(obs, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    shops = tuple(
        _get(_get(obs, "town", {}) or {}, "unlocked_shops", []) or []
    )
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    choices = []
    for item in _META_ITEMS:
        planned = _meta_trace_sell_qty(target, item)
        if planned <= 0 or _meta_town_demand(step, shops, item) > 0:
            continue
        available = max(
            0, int(_get(shed, item, 0) or 0) - already.get(item, 0)
        )
        quantity = min(available, planned)
        if quantity <= 0:
            continue
        price = float(_get(prices, item, _META_BASE_PRICE[item]) or 0)
        priority = price * quantity * _META_GLUT_WEIGHT[item]
        choices.append((priority, item, quantity))
    if not choices:
        return False
    _, item, quantity = max(choices)
    action["market"] = [["SELL", item, quantity], *orders][:10]
    due = state.setdefault("h5_due", {}).setdefault(target, {})
    due[item] = max(0, int(due.get(item, 0) or 0)) + quantity
    return True


def _meta_repay_h5(action, step, state):
    """Remove quantities prepaid by the H7 counter from their route sale."""
    due = dict(state.setdefault("h5_due", {}).pop(int(step), {}) or {})
    if not due:
        return
    market = []
    for raw in action.get("market", []) or []:
        order = list(raw)
        if (
            len(order) >= 3
            and order[0] == "SELL"
            and max(0, int(due.get(order[1], 0) or 0)) > 0
        ):
            reduction = min(max(0, int(order[2] or 0)), due[order[1]])
            order[2] = max(0, int(order[2] or 0)) - reduction
            due[order[1]] -= reduction
            if order[2] <= 0:
                continue
        market.append(order)
    action["market"] = market[:10]


def _meta_front_run(action, obs, step, state):
    _meta_repay_h5(action, step, state)
    if _meta_h5_counter(action, obs, step, state):
        return
    # A fast weed rejoin marks the remainder of this episode for a wider,
    # inventory-backed sale scan. This is deliberate opportunistic
    # liquidation, not an H1/H7 prepayment and therefore has no repayment
    # ledger at a later route step.
    market_scan_horizon = (
        11
        if _WEED_STATE[_seat(obs)].get(
            "post_recovery_market_regime", False
        )
        else _META_HORIZON
    )
    if int(state.get("clone_confidence", 0)) < 1 or market_scan_horizon <= 0:
        return
    orders = [list(order) for order in action.get("market", []) or []]
    if len(orders) >= 10:
        return
    already = {}
    for order in orders:
        if len(order) >= 3 and order[0] == "SELL":
            already[order[1]] = already.get(order[1], 0) + max(
                0, int(order[2] or 0)
            )
    planned = {}
    end = min(len(_ACTIONS), step + market_scan_horizon + 1)
    for future_step in range(step + 1, end):
        distance = future_step - step
        for item, quantity in (_META_SALES.get(future_step) or {}).items():
            if item not in planned:
                planned[item] = [distance, quantity]
            else:
                planned[item][1] += quantity
    private = _get(obs, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    choices = []
    for item, (distance, quantity) in planned.items():
        available = max(
            0, int(_get(shed, item, 0) or 0) - already.get(item, 0)
        )
        quantity = min(available, quantity)
        if quantity <= 0:
            continue
        price = float(_get(prices, item, _META_BASE_PRICE[item]) or 0)
        priority = (
            price * quantity * _META_GLUT_WEIGHT[item]
            + (market_scan_horizon + 1 - distance) * _META_BASE_PRICE[item]
        )
        choices.append((priority, item, quantity))
    if choices:
        _, item, quantity = max(choices)
        action["market"] = [*orders, ["SELL", item, quantity]][:10]



_V5_LOW_ACTIONS = json.loads(zlib.decompress(base64.b85decode('c-rk<O>Z1oa{Mnm^Pp~aH%Z?(Qm-W}XDCqAHr4}TFo4%EV5|>g-;Dk5){^~ERWC9!GV>M58R*t(wyNIu%Z!YS{Q3XR{^Qr*{{FY$&i>`+vmd^Gy8ZCW=bJANU+=ePkLPFq`RjlG`~Q6V%eRkz|Mj>3`rH40`~36S$4^gx)js_2^{>C&{PgL^o7=PVv-fwqv-4&1^_P#^?dQQCzHGN2zJ0y>xV?EeJHMQK{p0rb?x(Z!#qsB#@9#c*egAO!ADhR=f1D3H_W9HMKY#svdedUix1Y~;+b<7KZT;!){^8@(r{h<X595LOvc0`Mz4c=H*2CiluL2DjzV`HKIu)n^lh>KE2YYyI$<v%HMt$A?ioEOd?alkGHJ+$HhyMWHHfc9`>;AtC$Fph2(|13e7Q?8o`<XI+=8o|8X8Qiq^0;}}-cJ|N^t<uuflGHeT|{5*zD^fWyEy;!&z&*)X3{%0mF?h+2Y50{r~bXa*)Pq*kDhntpzEQzJPlX-(!(eWf8|aW*nenpz)omZFnP;<?7^4~hNGFW_BZ;B?Z=%C-RQZ~op&0-cAAWJxeyLFuo=vwm7gu6E@&f*4jq5;4lUKkQvSxDM=*r@69&wYH*fkN9^Y~N@a^pVf<D9s?lkU|2k(DLC%y0U>4bObz~TQ6-qiKE?uS=+?BrItFsw=EFb!NFeV#f!TO-@|#al47N61ebGonum-rwEcZr?xr@~7?n!>8L%|294oIt^a>C4nW9e#cC6aJaPx?J@Vz(Gi*a*tp8qj{yttO|SpJ{7(D0%6qr2{a3U}fO*%Lj{_qdEZmHr0gMs2CvdO!OFLvH^F9oF>-EtcK;YO13{vK*z)#)-*;t@Y?gN=eAli=wf7EVr(t)xERkD4R4Mcr&fBuQ5Q*(V4;K_X)^p*q812FDSk8F)WfAhD%39&8x_JtnjnyLghdtt-+`_uYAO}_Vm4Yg81?z~|@ZH2aX2v1*3@bPcQ-~AneY@~CM-MOG~${b`&i(@+mXW15e{jsY>?qA0N2n{>}<}KVHdCAZVyUQ>moRy-2mBHl36T?6Cw^FkQ^%0D0Y27jlq5WH*;RKuT1W?9b#h^E52op0Fx<_6Onfv~t?=SlPqCe`3bX2j2{b|!7Ag{v30oP$v%iu}0?`~iP=3{H1SJIUafLyhxuxEK@kf|6{7->JDI#kgGX51KK^YP~XFILC;*){<PN2C^@p*r>@IYh&;sPI18!D$1-M}|iU-Qt6O?AY^LV}p*2#p9q1N6N>j0O&PZcBeIZ7?e{OS|0S%6Vc@}d>?R)^r-)VI74r^jPnHsseN$EUHijExxYX5#TW$Zh~>0?+VdlN<`rh6E+VGY-iZ0~aDTJ=VS9i7S76DcU_Ztyy`pc2+}LGz=#MqfXvE@i1|0AO!M@Pl889QK0AKblwGopnR5zE2HMCBKSX>Nm<6u!~eH=d=uXO)$8V-55kq4U=Gm<;TpG)4!bOe&C!0LDC>*r=>Ekg9^xuKc3cYDhb7NS6)k33E={34I5aU{P-8(%ASxd~f91-s_rF>!oSgh8?qh@paxSH+p8zPbm-WUdv4Rtzq|-QC^oQ?3#;t@eN1PtdpX@xxi#);sz0xVM3?rK3|b2N`dr6Om{-)Yh#a8@%IL39sejM2MgqjO$+tlq`@w*4t1>O%d}$?6_a%zLsF95@%2MU22rIHoEH~WfFSZd`jb;TPtZL)<giCP6N-eCL)w^Kx7+ddz5!Up!4l?qoZ$nT4c5X8)o!L9~5xvv;gunpD9Pf13t;byq(L6+5}UW7paKdI5xKOEiafx95%;99-HRq%Hb`*AkhI4lu`{+fQ>eQ>z7?;I$ELl)7}6XU$-~8@k0(N80W=BWU^rzwVyK|vk;_vo2E%p0-XyfFo5hBSqh+iVE%8MG<U}4KL(#jnz=)It5^?g2T^{Xp5)IGi^D4r{)eIgY*PNuop@x63i`J!@gdlLYu8IJ+pG;aPgfTF;Ey!3Cyu=U27qa6gvPn;GJCGsznIBGL2lB)Ch!bWqcclec_kYS1mh;pIi&?)%oAr@WSkAy8VrBtkOc!8W30x8pXn?d9;vh>gI7}?ft-c^3JLmsklaPs2dT3Fud%lgQY{)13R{~1{w(BqBywuN?OHR~IwfEpudE>&Y?=PRs3Xptm8y}Eap4SAZpdP~QZ}*1ObUrzpvNgcn7}`Ny8ZKhEn1#a`%6C|GwjHrIoj{`=NB(TR6zpWhoPKRbkf0k3?mL4*RA-2;AO|P2~Gn+j3|_D8;np1sls#0hk?`lWWf*Z<OV}&4SkN9nA4o|Zia`8&qvi0&GfOn@Uhg^qeGHq;#$PVY0Yl~bKL?;?a7X$oLafO)?Q79V_QZoyLR|qv5j}1og0Io!8^6D%)jOQ7Re`0e8>s}cwUp~w)JWq*#>m>V$QDK9=77ah1L38eTN553q@Vri6s7F=VjKuphbJ8UiyoreQKE0i{-R6CpJ0EE3KL%_qTg{q%5?0tWe^dFH5=-f`h)YP89w-;-WOtVsp6g!2a+&ctYWgML%_i-t}aeIU{CK`uUW;=?`;_u(>JwwxRUGN}?w7?Azsh3UjqT(%}Z3(4z}vKQqQwcqM_<LkS9^ZbX{QH{!Uh2-4ts=)-$vJPHa9M4jSr<d?{{?;92InB{~LwDmRpl|cLmaMBtF88ifWrjB4sYyM`qe$I=f=spR5PX5$~E(K1VCbo`-7VJ!0#GE~~>Pl<FO0`zB=~rPCKxZPkskSbbYA;ecsh`L~oCe6eNCe6h13IC3_Y!W0GMO`dC{E)Gv?_n<yoEsoCfHkO*7w2szCGuGC}ih9?fZfPHg6`h-nNZ~)`hTk%-2QT(Cu9%$}YE(1w=BDq|3*eLUl5K3z+^Y4<d)Ir<~9ji=6sU8O|FZNYdaFkK3V#l(hvQ;lj4b&z0n%awVnKCuX2GZ7sv3a&yW3+TmNopldaoi$9v3H@Ml>!gR6Q>ww4W<gqdWFcJ(U%gw;keH)9oyJ#yq8wigzOhN?hUA%itFl-sR*Zv6L3#YGO^c^?#s*P2w{7Z_4QQ;}YP>8J}G$A*CZ332yg}>(6I#NV%!MrdWPwv&`F~b8O&=|<RI<Vh{Wi|V)uF+$i&b9kxl&wjcNz+>ig^$FdOI=&ot8pFJXVN{+M~2H1l5V5kdCT=8u+zw_AkFtCV(pppa9BX5v)tkJV@JU$no$MOVY3V;n!`5MovQ|53oV^<y(2^uqve96HUk#H*1b-wwa_FSpf=li+5Q?zbtngJNH}kL)T68jw37zpYLZWV)H%uKP>;m%(zy*Bm3iGfhnByoyU(tJZu*j)xDy~kD-@y*VHwfDzkuIdMZ`tgKpx~Ycb}oER?aDL0#?gLUuNpIjm}j4nlx8^E-8mmj=X_qiHJ5cqni2J#-ZbU8*W=nXp<TG0dNqH9q@)#<4&`?x{{@34Z>ES#@82wdG2UdgjNBLCnSJ=p@+E2mZfDw*bp>*<}I!mW)ssrY$9fIb%jL$HDJm}+#n7t3SSS^&e4!M$moJ?zwnava4krYVT;QWFLOx91lM*uplGld58+2f)^~^rn<*+~J{m%LSC%-_)~~gwSoiz{tE^~>yJ)ng(&7!_m9mUv*Kuh$4fA7T9=^j^K+JtSZLi$HlJd2FqKLyB>q(L|T4>c21PRR3ixraU#ubbMHYaeVE<n)}b2)xFY|oVg(aev*0LFtFEHxqEoE55PrQ{hhBKD%lPrM5zsZjek?x=%ke@J?uT>we0QC*0+s`bQHkdB3bm?&rN_z||0iZT_MP^*l};pd3=5v}=*y!3Py6`OW9`-TxITtBZyx>tn214%0ZLz?V)acJ1yXsHp!>>kGIs`$M^4roBAkmw8#ydBaNSo5x;1AsXycBB&LNKW$j+(A>Lf{f^-1z6dTPga4X)vT=nRw9B?t1!<*Y5e4v?FmmX&phr#7^0j>CLF7l%H4W>UD$q{u9{uIt>ccqfMO&@nkk*+!3afns=O4$;iCGH*mV|#0u%;k+`DI_hiON<OgM^}S>y_-z-D0tO9~a=+^=)u^ADp=zYBN&#W)wOH4iNbDRIEYC=y<OYl~!g1yR9=s)W0mQGrY`nNX37LIR6F>F>KvR%SAaKoOIgpng}pP^cb-)YL9?pVd}|OM?3Dt6P4?PI539tx$Ie5k%J}Ho2YP+)j&V3Z#aMQV^8)CDosgD4vWjn}i~SBd8$Bwn+5SARU=44<5&lX+^kgT|Fj>&(o7%j9#+culcm>P@td-<#^DPskHws>47)_b+#DHR1*RD5X@{X505SezR<I64brPxFF|$1<F58naIxC<P`9f6(26d0XejlpiMpetS=hrhTn4fal8k&du%d^U&op3Duhf0;mrj=<CgUhAUVYv4Xl^w}Bc@1NTM;>y!1dc>3GmDebn|zF1Tb<9l=B-*qf|E)ICh?$4}%^B7kU>A+}CSFl=2#qKD=JIqAc`4oOQ}5*GJ2UXP?V_4VJ5rDe>XLPAY9+kt!9#(1rsCy+u%u--L#F^H|AGiFs+ET?>*mG`4-9(gT?dsr-PkPR28lp&GP9ej1MP(}nDg9Qb9|=*u|Z8E%TCb5kppt)>Bqa+#T_W*Q-IAvt7(Oy(dh`R9qzP#{qRIF`8+T}pcjOT1i!qHnrZk4Qb%*j-9FR7abqK(tv!9DM36+l-qST=uM+yjU52z-0vL;T*j{x<okLK%!6pz>B$TFPC8ddx_m%cJazyG;|v)4pzv8pCO1Fs2WIaPKT4NuvxsJ#ZEJ|4T?l<5UI;E;vF3^p5R`jX}7CoT)*&HbtB+)>*@MT_+;?zVgN{9+kpZCQmyO?p%mF8R6o@drSnFiRCUT1W@z=$s2@UUvei8RB0hTFfeU(tOE2p3UDSrxw4j_wQ`U%76!65Tt2BOHLa~yZVr-xt9(bJ+O;$%lEYpd?QciW()gh@GgghYrD0Sd3ixg>|E5@WB?Fg{Y=<~9#qB+Dg`p-PWs7HTYY&*3iDH4*VR9{>1vh#_{yXoCG5}HK(sNqn2`1G%lJ}#EM+m89;&sBs68f+WuI<pp?-<9=XVwzV8-Zpe^B&EfZ%WqU*hu`28TwR<-QO`rOokEMlHUYjmB4TVkszM~<v{o}jTI{HMVm%y-m}u`D7|#f_T`0u;#lqMb%eNYu&k^`bL3*xkZkpo#V)I@C?lvqISf%2-CCG!Sw)2GN<E1H+l@Lqf3)J_UrTRu|k$PoGLnP%SU!KK_Jny?xK@V?10h?G#C{JdxYh-L*L2}!p@;P%PF^uJ~9rP)o{hWw2Z+wfN+|kE})Y8;hMwcc(lGGZI!oX+&g&7g37gTeAZEf!7mm=o~&kO*-G)nAEB?&ghVkc}D62(fw8rRufc@Ki+W~hO90$dxQRN6xT=bA<D@T(&AZ!yy9lR_43@q`I;7ZDFq0t8sJ9)M|m$RRN?Nv<tnawWQX>8wg5LsmEwBJ8s+Mcgqf{J){zYTJ}I!(jld?N{Y20KY;eEzoM%b<zSzG|i~>3krEv_ZB+(epqm;#}$jRPO=N^{avZaDHbTqyU$rww|0rO1lc%8z-PAhD49nk(|57(MSL|fmfodx@V<*Ax;jc+o}`oGOBR?vibfiuw+BEr>d1I&QkP2d9U!WV8;ad<;DP)#S(#5qDfsH4ib`QEfKb)9M6Nx;Gt81yn;9p_t>hNb+yqVt3Ey)}$BRs9M3?=u*ZNM97GRK4B2<736;Zqfg$6}0gU~lbc><p5!uF$lP^<*+P6WSbLKOHtBhVxo4j~_nQ=yfd*7imu#X%@5>X%DCw$!@R;g1>mEVmz4O3iK#TD*{8FXL`|W<qJcKz}bAdWsZ0cZ=b8oEo-dO#%q@MZFF;Pg4v37El=)B4ehNT4X5$h?&bE*GHc65XvNCq#3CoQe!8m@X~};;_5RPHA@>KMWnp8Y?2`1)#;M4gjbz1h?Xm3pMf&R%Qu!<^oFWHaHt8=s!)$E+^9p(T%)cKQUK>Gl--nzMRY7YDU4H&xgaGishk%rTSP$6W+^qmAQ`=2rCj$z)2BNgYo)w#33!obN1}%wy+Pfp1p$RjY&5hN5<Q?POH3qzdVp$;#YEvs+W{UYoZ<nNc}LCll1oQol`J&xI4-fOX%G;^0z{X1c9E(q8rFti2J(@3!!&sbmA?{iI9VfVav$h{mJOV4G+86#pakA*vW|4uWQBEvt`e(>(*8{q#+CiecWF#Tt5Tx2oUtDUaLhlKaKBE8sDPmnr14SM96qn^ZqyUD@c7|LD;uy<i|Ji+CFm?FsZ-Qr=V~#kx(951R*{pcmNL=EEdk)xokcJ$Xl|YEc2+7=$w-R!?xKNJR~`G6sq?9Pn70;alS(v6J9<4}=yY|yjq)H4UyIXcn@p+6k=Pjt8X-Lu3YU^dmE>^oM`NokLgEsA^&FcEwzC6;D~Sa;wNJ%hry`)}<sW%?0u4vF&{2+`ws_3wH4>*dkpC6LiIiD8FJx7Kl%ZBTOUm0qrb%mybM|B)036_kxdnJ6{Tt4S&|pXq&egPebNnz~{h@W{aR{4gUTd-!)9wc-I+8mmI+6t?&5h6vX$_)&Sey#6&SR!Tiyd3eti3|L5gIwGExl0%JZsX#Gm+7tu;HRXfofmYr5OWwfVearianFNNQqZ1E^>3`sSO&CtIZsjO8tr1H%@nC9bC%1a4B32;Ve|p8DGy&UbNKdh$;(DVz>XFmwY}ww>putHfgCR9{12BdRTO-5B;tnWrfPiOF-jJ6A^G&X<f-^mywJ=Mjm3Re^S*%c`_AijO2#KdZVeo33+XO`W2HG(n=9gsCoMPWH;tY-+U&8tp!rp>*s35i~fvyxh}OlsX3IX3gnuG9Y|rVI+2?+sq(z$EFGK&%jT_;+^y{JPO5_Z1_hBAU^I4Zi>06(^E9EJ1U7?aWC7^G?`m0IiHQeW847B(ib|aqmQgj~Xvhhe0lYX)lVWM2?$m;_UO^6%v(FY^JD*~CCwb_i$bowVSXdWbn(hE{nNJAM6NN6$Ig=~6YS;`jw@u=>n7wE0Jx-LOy$TRbM3G{HIq5OuAbJ`u#zK)Ky5U0bUPQG!MuS%goW@Gf>TfguC4+5nMBYcp*}u?QF;~dA4_dM(UCciACbE}lvUftvi;0@MHSnx6TL9|Vcq^JuIzg6KS@#&D-0KqjZ<bWc8bqovlY-L;vAQZ1Ydmr>auY=V=g?99BOw^CSRjjXm!MUm=Hm6@F3}chX}tcy>fF6b`kbswg>MTItSV}a?&c>cl}k`pSRc6Xmzo(#s}RLT!38I2I<SLjv&vdFaVdhbxV}UXs^8T3Ab4xEet3@(Z^Dl~%QD(?mK2A%jxB7(gp+s<n;N5ErN}T2bAn}4coKP*RhMFoY*PD<-=j{UA&S}%nqe|}>s}WO6qD0>nad$oUsDMO>)h7jmB9eNTUUq?>vzwr0He&KgCN)?!L$1-w<O_Q2}Ot)`e|Hgz(o&8Mui9jEpsNYYW11pbS+oWaXV`eo`P8#Rf(NWL~C=dwaPtz!=myN9PHm0Nn0J&g&5Sqz$kG0AF7_sHE++)cf>^mFxAT^Zun{6PUZW%2ff^GxM$6a3_uMXpI5?x(eV7A9hnP(44dI+4S#D^q8|;+pgnwz??*_wOvOwU$9ZR%sZG1>vZ2k+f*sA1u~3ugQAdL+WxHr@BylM%x&t!YmT&umm1OI~lQL=K0y%qrYE+I96hQ<fB7+e`ZUwz}l2jH=UCXkkc9j%H2KOx<OMI&29J)*^8m)^$nyZqo8(U1#0?op7$oVGVLSdGkr|}i|B`+x~-lZvc3vhu#)8v+^SBn0)GO1UA^(Ll6Qm(p`2G(Up+7mE<P^qQinbQ@VBYQiwiP+L=W86fZPoQbE_rZn9dZW#C_K6=p3%gp^sYr#hRJc}{iian5(7Rmz3Zo&mYmoO-SgL(MCZ$jah?B_$3W#=BCck~1+BP0qL8(77_D2d_R#RAFWIO;dwQG~1PhP4dEvoV4#x1T5H*i_aS!JLAE9XEKBITLsXL>Rn7cZ+g)z(jsNfhwg6tb*H-9(hyD2S(P>6+4rh2*?~o0HXJq=g13x<!WL0RQH*0`=ZrL@<5oL~AM9?Nu_sgoPBzj$L0y(j*BZ5uw8aZ9oHOrkZ_Q2@$?B4&@LaI#Z722)Vv6_=qhT=sQCZZ!;&l2`&jAj_J!!<nq%}DbJWRTnBhi04-gt)-4<4df*w+d6prUCxGSuCwAmg8fEL6EA3Q}b&-)>d;;Ur5+N0$>j=gOkWvpqln_)oi6<`x6V(_@;MNpfOhDP{t=pbckxH@bsAQBF&+ltv)6>$a2}0UTfTg3&&tX@BOY2qIOS7x2ZLy|<P@9f%7y9T>NvoBGUm_Jcg5-exI$Rjm@nvWxF9NuyR*lgY5yNwxsV=Z8LZ3<{5%26_>p@3j*1h*106+b@e*Vn3=AdRQSoFz>m}_RE?)1EyQ+FFi+TjbwS5X&gY<kx@V&0DTme=?7OIB>Vka_~(lf?ZD!;GDXd37B)beK3%NET{0p%}Pj)8NaZXemhb(uk-SLlIp$j0B{dUBz1EBNllQZyj*QCgZu<k_Jdr5dPp+5}9&qjFL8AI(9{t7Z*D)Z(vBKkmOSQ{wk>ovqPlTabh)SPM~y+pwP7m%&p9y*D92r%NSp4-GQ9#W59y}zQSJ_`Nf8cGv(`OqPixdmS7<6tHCG<;q4jj>CAh7SF2wL`aD}-0}Z2FjD|uzbH7mv`k$<xK=Rz<+@^ihKNAxGf>>Oc%NICiO$@-MK&QmXZyA8fP#vZaq|OmQc=^rtKu{`3()|3y`jvDKjd7O5opa?u375D%7y>}DinUD}h~6-4u0!{gMw#v{H=5<IT886F>9#NmPAC;hsXaf%I~3(|3m?*MX$5$*>;ztO!VUL$=p%8th+kpSXw-?I3^tkrOR1NFl-ot#<?%%Qv^LU2JAP$bZFQ7<xbN()0M~X(EEJZ*X`FvC0Y#rk7wf?)PbA|LL8YGjID(6O=!Bp}geJx~>}sV7zz#Dht|8$hMKaJYfGcT~I4QBEI$7CilSBxP;66_SX=k^2f=?~pM3}`dk?}fA7dQ+rfCFDKv-Rzk19hU*%zX)z1AP&uT7-uXR6Gxt0=16%Ts6>uki0}Z>%$<MDepLBc@(OCMzJ^ROr>a&qW#pDMJ94mSY!!d`pYzV%qh|wA(go^#r@PA{jr{c(j&h$kObe}?NsR{uE(<}62`opDLPzU>SQ1p^xbS+F*<=1ul8lz5^5{01()E9iMiIapG*&IZsH~(gh_QwOc8hQmmRgq7zd2%GI|H2lh&(GQjE2?4Di3Sg~gx(A%49pRepZD?L#4JT`ZRiIe9pDCu!WEC6iWbbA%inaDtUpE~P=gOI?AO<0MFI9h`HvlI^0?eb3V_lPMdbLawHP-^ywO>pX*mm+~PHrPhBMsKD&FGz;!>jy0eajiu8(CC34n(W#fbtKV1QZZ>3FEJ$e4!X(~bMIlI?*eF`bH-uR5p7fbGcylI{m+;AJ08d_Mb*RsKu&=KF$eFhu4ZeFh(>bL2`qwlS5^t}&$@0B{3a7EtT`v6IMZ}L0hilj*msRT`*5~#PML~TsjvG$92)K$27lq{%10`Uza)3VT?OiYAlSX84QfQ=#g`(G&z~FJEyXFi>zK<|lLjAU7D5JI653n!~OJ^bJt!$Zqu;n_FnaWc!T@ig^n)})ZLDf7vR}_PwOtd>(v@Lpc@Bo8Co(Pom((*iMh2O2BtLA7k<%W?Ghv^?}YLMOb*eH^;Rtr_zrerE()o6VfR?JiNYNGhG_ZA{o<iS)0LP;I2q=%`bQOgxm+qU_6?_$B!N_U{^y7Ge^6h3zj+)%;f5;Tzk8VKOVK|;MGfKtpft-FX)hiPO`OBj(@af0QiQrygZyQZq^z)vUIY;CpKR^-iwmb%PLKQ%SZq1!ZWD%kqZ&-=XyuURAhR!hcGrw%q~C#2b_g<<6aJsAzMdO6rohJyP!TF$mm88+1QRQc49H6@mQbs-h8Lc2>FWcd-XQVwF8O>hLso_DIOy0Fh~tH<PeaT9rYRHh6~lj(hoP~)Ms>(!};sx?osiMjouuL^kFONtaB9hOic0|Q1R;4zRin9-qf3vxVTiK&1n_a=7C_jc;K?IJlE!JJM>@@;HU+m!%QnvB)r%b}{HlBZ4q#gH_XUZ^7Mra5^qOq|#CfU4C2L=_w+5#>}S3#}w4-B6o%wD5OZf$fx8`$QIiE)Ru8RiZ!kz%YVoy-x1+)7~FAk{o7}GAJ#tROV8UvIKsy&lqVa$~F=Udsf8yfnq)30Wn*ol?xN-u!(h>D>%?@$(9qvN=F2;d1qts>?>lf3?A=7(|I&uoHZZ@tuu&7J0UutW9u$$UMC~bgPXOy71$6_63I(F)Dy;d5m0DjuO1V!NEvz#z1aJ?=Q=Qx{Q;h?_Sh)#VYEafTTn!p`HQG`Lh(UQQo+yu2(AHO^RoIFu3b*#XxzDF>Xo><eM?2*DZ8u~oO0?oGsYM+iYi(Uc^x_y@UR3&%JhJbO`2MJi=BvYSd+8nQE1d0dZNja%tCh(%T<N3l3WmrUdm^cCvl{L4k4$@BTP^+RPR3vmUm9C$f>YE@2oIxpbexdqfY||Rtc||CQ%b?cD5<>6%Q>LL28FDr_t+T``|lJ%2*QxXBE!6G|hhj|6oP%yEiNJ0k99=LbE>H-+h)_<)|yTxz9d%0Wg<0S2CgDntH;cbeO1H8MvV*XJ^o_4Zzb<^>oQSj9y#5%1r6~Bxjx}W_jXhX)1tf87gvZG4iNKu##;F-;1FWPWh)^bKG~6Q_TrmP_A_4y)=9*mqw}f8Ln|sbkz4W$ZNqZ3ofkz)wZ!$a_@zv2r|$tD<Jn;(6`odAQKRJD>$Ioh=OGpA7G()%ger#r(w{_M}d5rqea8wbf&bMC`D-Dr|pP{5MFge+86tU2%OS5@!5Z&zV2t3_w~38^bagoYApp>g!OQIr|A$VA4pR#kQn9TKOX-d6?ys~')).decode("utf-8"))
_V5_HIGH_ACTIONS = json.loads(zlib.decompress(base64.b85decode('c-rk<O>bODa{Mnm_hFhJP0}}x)awyeGZH9i8|wiv7{F^7FxH2$Z^r(2%M{uD-mA#Sh^%UoGv=+;YQ9(Bl^Gcs`Sbsr{M)a;{rzvho&3|!C*Oa0_x|lKA8$T={&KrLxm%t5`>+4`umAP+f4+YF`>((K$KU?@>*t?Oet38PzuJfIzx?%=o1fnOc=P^bb@JxJ?qqe^eEsQ%?e^p3KR#`@Z@+%M`(b<Y`DAsu`1;4~`wu^ztk(OVf4u$h_RE{khrig|-Th-V?bye6Z~pw{<Ka!~N#A}x*=;|4zHjSKA8tSYaQ|ul)#Af^AU<v1zdyY7Z28v5$4y=Z8Zv$D;nQ*|Py-gP3uh1ZaNm;qIa$y8`tU3Au8;3;-fW}sME!aE1Ms#*yUAN0{$x6yO*`(t`{}S4W_^8_so-bn2ybte?>{V$o6p<Z<sw>sH(xz)>7FhZ(WehzmW!xeoPYYioiY1n(K|Mk?cmG@cri+c{=K<*SelPN`nEGCUAN})FkJ0RA4g&Ot8}`+{zH=kc0#j)$y*-A9*o&!IGP!2f1}UX!?@F-n>}~A^A1DUPE)Wh*TUfjHbZ!{^0Q^u1#M)}p_5PEV@vh1l)uU65e(tO2?ORRn>T$B_wU$$_<Ht!LLa<=JB)kJgCBlLCw=Vm>4XpIz~kRe-Zb>N>4#@{?BZ5A3#`fHFf}faF;88dt<Ls+@)j)Z5%SZ<j2P2`Hy_@=-@f_$%b&KlpWnTI_b>A^VbI`}Ut%ng@;i<+2amV*q&?vt+B+hP9|u?Y#hqaRzUcLD%<r;~=XLKkwf{P85@6mn=HtW&2Mf32X8>aa?g`whhox<q$-EEK-e!GF2M{>+hC#|)75FK8AR7zxDSaUG2t@m_!yk>CTy&t~L6vM@Wdl*)JfDB!>GZk23h<OZ4tmRm^8k$d!y{W`FyH(wa6)X$ynWW=Qd5=SW>0KbzdmjJ)8u;}*ih#x$Xz!KsIAcU4&mwR1wQ`u_`CgpARFmiWOpuToH7R$(_-I_$yv6=UcYy>$o(5Q0M@`GU_QbPikA$%u!jsY!dWRQ*fW^icw+dc{#I)Cpgw|;?OM0YLTLYQ%y5EDcmOE<S25@<8N$MhS@+1ZA#<-UdVSIBi~guD(ow|`_Ge6ofV_$n2fVORt$-)dzPo`Hn2)W2UPV{l0J-|2!kOh+L8d&Y&}l!RI`pCo%(w~0=7*cxzeF7yXWJMMjz}#)L$&Wqafqg4(Zl;_2d51T?-?Fl=oTOJeaF7N)f;qVEba$oI#M}C1wgOavOBEN$3Z!Sq2)n8JP}<!)As?_NRRqI5@+ZQS8=|;Ahi!}xodyeDEI4QpNv6p;aE-=_j`Uu&%DBH)U{(;Js2^cKHuK#zTe*7{uNj<CD@PgO0VeKAvgAPIP}LF7&KyicLW^p3Bf+=?ljEECBRp`OJl^O3e_FU#F|<sQ!LKI+c;R%wLbPA_E&oTI1Pt<ypboH7Bi9u#-F>qljR5$S3%To>+5gLtXhQV)3=6J;@<5oM_7mgf!=wXVE8$Y>*GkiMjM|icDb=Fpbop{?5=QpQiMUW5s0CJj#tH*roMUx##F8qhE_~2!QF=s@9%S!plS8+pAQrC^?ZDLQnvLD{ygrj@wIexYUUv0tqdX(Er&X~6=Z{VJ}dTG-cN)G%E7q)r9jC7>0_e}h0+u;KO~O(RqksEhU((%>Ap)JWvz|wrbwBD-Zr1gc;_}sTJf3)VAEyb*=r&~87D-xdA3LQE-*UZPB%LGmZwE!8?a$UpY%Zir%nqXFY}pdG(6ywEX><uSy3A^g?U|y*a7ovjbnD_xm5;JjBQg*<hW^0upIgV>=GR;LFv{YJve9sxSH8jrz07PubmB0@O6932S4O+gL;;*$%ZM`c|N^oJxF&tO`)XZx)g3;;MqRvWFUcH{%?{Lc*gYK2c}30dP0cnu`JjQqTD}S0DvVO+ba<ML8o!N7|4{^2F6Ukfr)?728O{@#BD5skzu$P_mtT;6=MTf2Th2!ktnc6yzP8w>8!;6%SW6-;l$+X8}W8=ld&W(XW82T_3ch_%5Bj0|E%+l4J+*$`;(%hl!Ckja%cZv%e`SaLX2tKm+&L!?AJh8U|{Q{;o2(!Nkns0`l*8J@37y|puvwu#E<XZ|9S3HL5~ZW3Ginu9=?Cqk$tbT9822YugI*^O+lBW7kFWiRRpZT$h&B+ZH3~=0jWAZp=0wES5tp_dN8vs0M<wFzHG6y=IYF^Cut$dRuUK*Hw}Oc6rhmDA$zxq5}53xQpUBqcr>@Ngn(<5j@Gk3SoF;3!3@GaXtMPsfW=MXTwI$i_KM7m!W$Ck0PYa;f-vvXG?a+1&<-SOJ@K7kpsa@-s=&{yBv{j^L3nctsHI?P0&A8GE!qZPGj*H6C}_cR*+3JgE3f4lR}5v)RY?G>6;W)yY5%;ES8z}fjNctnm9z7ZwG7$0>k92h^2b;g4o{MjXM{%XXWeUv<k92;eob@091n4#irlE4Y_AuUdiL6wV>PBbXgH@xUr^2Cvcv>a7(NJIU};A3J55|{pfE;jpXuH-A@O=K&Ya^t#G@wBKZ_OA_(EqAEP!ndL-wK~)-^bb6CmRIRe~Za$aAh>Gr1&)`X&KZ_{KFm$14z7*cA|jf8qp`87J=CNa$^Pn7Ct!m<SE96<TiP2{`x|O^ImP8l6r$cf|SV692O8P336X#c(B90C9?L5KfOMbA4PY5)xy<NEU*nJ?n#Q5^lyMSR)3`HIGXtW)WYNuR6r*h;2QzmJ4kIS-+2OAkLN)2wQez435qmKH`s!wWCS1YNIx!Rmf~U&d~5?)eoLyyGAwTsF%>Hf;Qw6v<g_PFQHkl3v0mc)UkqN`uW{K_G7s7mFTz_gw~_u#F3xD?Y=9odGNB8d{xR}34#X}k+|aPRw!h8SX_6{qb><*mtKZH3xrF~9}X*)MF^-QW%e!!kBWWq+N^`PXEu4MG!)GW?VM>kT+^3`VfRj1Z|)+J3=bUH2A~8=w*&C+dTrbR_?2zD;qQ>}D6gspntN&72pY9PBAJ3Mn2+q`olZbyqe=Z{k^>m!RO8lOp-6|`0rYmfiy7&bz*eOmY+`og`p%#Mprr(ws^MJ{6r1-<hhV65U9wU3%(!W#&RF}+>&xt+N&i67?xbcRX(Q+z{{wREBXZ=tFQ?~|zRWrvSMgb280qF|>(pc|nlp^M@ZFuBLd3~L6jFtJEihqZ$)T0SyV9ZZ$tIvmy6qADLc<)DNKI`@T@aCni9#CCG|?iQ<Y**Sp#iik1Swmu0HBmKQNS%S%8*NNK${~W<exU`B_r7Rr)O1kghM7T1u2OtKU+@m(J2rI^q!`hgB|NR{Q31%<XQtKPry$kKR-*to{m&SU#Rt`s~}2|%MpCt+Dg-&>RG<ZvQtx47}+-MhK$@@TWKv6USQb;)KoB}^}NuSyxgeIN$A58)5DYIY1RvKsc1u}lU<|hGJ&p^;KNcTD9Ig&X$)B+0Cz;XER=L|<OL#417nd<r-LmVPUz@dIH1LBrN<n8O@0#&_Vzf7s@=nfeoTFK^eVZEP}p{~x2nsEaI=!c5T$ua@h9k-2N9>0)F*`wldpG9gzH^U)g6SP9xcg;)y1kVGUJp=_XBG&&oqm%VtdR9*N@|&f@EC+TnxYH?A6Nhr|b?o>jt(<PFGVZ@cJ|3R|R6_Ch)*Zc*@hRBM%Vj{9vsS8w5H4K9X4803c{2*5jf=$A^6Y{sYy6i7?)D2Clm0SocS>p6pVmoiKzqZ#+zIX%FZ&GbDvYl3=c;i)`PD?V>nL#!#Fl3_a9*?5vggxHAxxV-6K|l@cDI241Twm|&o4?DpcWLY1$jIU%AydXOVDz~mWNqL!*EVCWT+oDG1raG*g};cVmNH5EUe!lPtt5w41m<f$_`L`VvabUS>MAW#XZNQpstF3&i+AQ+?x+@W5U&Nwm07jp&iw|s{zk&dC5921~O9QLSE9~Ltb_s4~Sl88beTzCd_T)k1$*fm=wd_(KfhnfgxT+~EZMhs2l-fOn%WA2*2UgD}rXnAS`4S+w(4!J^|6zg&chn3tVb_@rNE-!Wp-<#k}allu-^^!H3l>TdfkqpKa*6S(N?>=c8kQ*<bO=4pN;P7Nb6J~#N=mBI5J2D48$E5Wc`c)`epRK`9h&R`(O%D@~GDQwbbue>AJSeKaT$C~s74V`H(_%CdNwS6Qg=)%9yGm5K3u>MeDjU)KJqC&BBpc4X=_CiGDTeB}wwGkFCYr^9Zr3XtV0MA~_Q(0%AO~9&ZFxjC7DVf;wktLijLSvQ(oB*);{*>YKb<DYau9=>oJMgo)+kiofuTLfHcq9xDv+WGtf-s4G;o@~Ea6WohiW^faD;e!&{a2T$izUn;)P3D3$<!ZVv}gw#LCr0q7kcdhdgoAE(uaF2GkYGRlf^hrWQ@6uy>7v;1g0rTtTl2qNruQefQ5DL;|BNHFy8I@#-T0;QWt987O#V0WhB>?{_*%PD~MIhmI{R+?vs*L`HXi3IRviEz!j-^k8^l&Wo8kaX7NyA$BY6X0=IRgrv_c4$FHy{4>k=80y^Unz^>nMy)m=DimU6@YHr3wO;2_Q>%}yC`o9`G*OG_QiV|UUMo`!-g{tPWdq!&D<gU-f-*`?Y8CMMMJK)DB*}cM1VuLJfzprze@Ak@i{-I7*2(g4a%@raRbaH9x%ibA)0`2SQGj=!3ZW_Pk5;Tki9`=zO)42Bi6_22j(-z*GZ)zJdFlQQvZG!^fD%EEVhpb%0iFdX)tqFof2hIclA+ZIr1Ck@8yum0uTY|OOj*~M6A0`)C%h<;CatBk!@9pDj-Ad?$@AcuEIDA_wPB&j0ZDBuNm))2D{9YX{jR1*flh;G5$L{|vkE?H#U1Iaq+8F|0^1m>{A~`1CGo)oF<a9@UuA+G;o-4uG6?lHR0qTsQCy!nTwOVHMXf_Y>nf-S%Bho3Pg7>yk!Kl2g?5uQZ>4K_b>xX$W8Q}gXVFjFh}=ri;pVv`CH28VI+spb<H^|)ExAv;^VGQ?p!*x}r?*~Ccj0&fy*YP_11AWE#GR!<%R$q$5!k>yT!c3mWj+m&;zhl=5*8i1co`ak#Yw}TGyZ+wlwAq9iU{!V<4s$LEQ8MI6XdEZ`g|ILLflLOC^@o!O48D>Z2qSB65<5)b#e^aHG6ja(tDq3J=MFNYCEEv_NogULv!<D==+92&Gi;j(58~|P14zb!|nx(>zV;o=76$m6P176#wMlEJE;TR!TGVH-Gi4_hO=w=Qs_w&(|4j+OiEFA4zfZXaO-ypIZzmqy6yv++NdTC(~aWc?r&YPz-JBNM+Wjd^v05+os2|~y%K4iZ$dzB{tTw{ym7s!7CF&aAC-K2wz+{h2xFm(^?|tx`MPQCctGO^r%Mh4x0dd=0W~WdHogRy7N%|zo{Sz9NC$<}$c-REZ%39<f&q&#a>a{np>R?X!lP%gKtHf#`P=!6OiWl_l}NdYRX~IpgX5*>?nMW+2G@41v1L<|#0+l9xBbG?LMA=9npel>#d{!y7_}3Ch-%S;O<WLU)l?H-5gN!8Sa{`oM6L~t*0H<lIoKYI=P8)-F#Y_jO4Rd`&v!D{13+xdA@1~TQP8uDD$E8OU}i7J4+iF#A_g^~M}!5omZmT~<o3^SY8a@+QVo08N!IR49A!lT;MtS0FSMe8o!&W6*#aJys`%JP{MV?XMA@zt;ZrK9rT##@#N4S<*^jY568k(6TlOhS7A>P)=3#xi&9YZ>TUiffYZ?T(rBxAIW1JaPpHLOpXL4mVI2tUPQn6zi%#Q8z-0t2ux@&a%2p9T%{bf3Bg+hgwMkNO>3dW9GMyp}93kOv!lqxyI1yzIZ`0-|D;$8RYj=J=#v<_{x*}y?2wI%>olEEw@_eqWLYXFNzQXtgH#HrKLNTVIR>cwGHcATFWBqrR+fqS*H6rd((5|Po^pHBAx$C;~E3V$>?-pzWzhepf?=vo{gDlOylZnmBzvb+R>`92?3+4E8$WkkvizYB$iXVh3sax(KGO2@;oJSfGeo><E;wiB6(j0i`qf?ZjIR4dxGBT!^^DnOwZSJid-a;etGgQb!QMIAOBhT%?L&Lsj}ysG6mQB8uFrqx%%b%e%$M_H2CW#a_?t*LH)UP^1C0u<=B&z4<f7mg5QB>7IfLrDUA%-T41iW7KqE~LUUY|AZ|(wu1V!=9zYONnSY^DN6L@r+~1j7<E|cXF=oN{SzC3+GEkC>w!8=pyS+1YQW3M6Ewnc9FQ=ZvJacI$vE<aCvd(ilt?g^RYGQPU`0~YKi1f2U<inWkaotA=QyWU4E1jJhZs|Mk#`vcja7kbJ+@%G%UTz(}qVjlh5MFz<17tFP;u;=`m2I@J$KJx)2FGO!AaT9Wf(Q%e5+80Rdoh;Y1pxqOoFdk#n*}W30Tm3K0UI;CULWafIyo4E&n3Kmn6oyzLuec6u7XZL{R4d4K^n@fCIJu56+)4W2+aD08R_N;P@WlZ)e&HNo770X^KMG~CjqTF@G@)I_+6`<(e#)ml38N_3Lo%n~UrVy3F{ktjDlwgXp4(uvIzG0h4Si6Ig-)~cT3z~ZVU%1I_ishtwyiYtp^6ZVu%!1Y~0thOW&WtC^pmipSDFDXK}jOa2ABXWWOz2NASGz9%=pjb&#RMc;6b!?|t2`kKpC+f7)2YhvNlurwVtIiV)=XVMMs~lMc#}KO|MlPQsD!k+2*Pcq1^6IgmWJ2X7BGDq|sbiQMVd*gJPtAGYw_9F_n=P0t<K(3lI=vNOip0bd-Gs|f(#c7-d-JBK@P|K_4BFGU`Vu<CkTV86Ougf1lB;!&)uMo!$N{~f<iZLnGwZC9KtN6uUI|2DFAB3rjHHcm_lg?kE&eW2DAkMivd*Kkfv_3s^<9H*%~;KCfuJc3Qiqdt*!=~T4LTktO=6-Ye)7|j(qK0*{v@i(9IyTmU^OW&H52G73Hq>e?7R;lbJFENCYxUBNAO!OkFoX)r6&MA44<yEzSJUZk^1o@S&;+F+^%}?6SEf6{9lAarR12D&JG2PBjyc;-x$43Bojs8p#r-_l!l1D<(w6q)gv4X7o9b}kQJ;7-X;~O22}r~Wy5V{HANj|xgTnUqe$kjU8p-+W@#ZhDaWjb@}6gx4yuKfawm=YT#RoQEZ#~Er8-2slA4xqSPn4&a;mW&I3=C)J}ZHqc7^!)&I!z$3u9aMCZo|4#$6Wd*XU`$aVV;rsW1wGM)M-!d|<0wK+-0uaiGJ79G9oD#|2v1&eGDf?eg5Gxo7C6iYJzyP_3PN5F_!M4bRA&$ke>*UJa~s#)CS~P~0rhLDAF8o~^!F^aGh2cAQ+lENVGiXj^m^N&0nH+Mg~GqBs(r(nb<AVdeq)noY_wHW-X531Zb@G?U~(V#*mRH@Tj$$Nh~a*UKo(#csD<ldDE^E=V*7aYd?8M~0ron=)`qDZ8ns)W!Aiq(rN<B(~yIM=#bL73Q^)(#UxNQ!*8krb!QHb0%XBS0zJ@tWsU28ZA>AO%T(A<oR9KWVopAq@>dhl=+XmKeH%}!y^w0*#aWWxBW(e8`keI&K)Wz<a2)ETu^q-5LA(#?E8yo-&c!dO`dAs!%5W^j%OtS*H9|lsFW+u>35C-E1OfsfDwzL8xwg}o3{Ltq-mTyT|MFMiI(AI-!)5>w<x(MAsi;~0IYUVJdp=TXyw+dGT{pCyR)cgQNeE~8Fl#t#vz=e&YfQBK|@v5J?L}Oq&e$CF;81%v-Kt+rg8WA^#4JMW_Ti=RXoRK3(vzZ;V#nuoZD_LcB<4fkW_ACj#aF0RjX?yNzrFY?+|d+^1Y0ZCGa!~nW7!+E{^Eb0^neZb&P=`^M%aWo@K+y4w+n-o{wWB{1)Y2SdBFbKg!9p0!``6@#oXz+*X!{h`_@>8Z{3Y-D4{rhqP{8J<LH^AqI2=nj{jcwW?h?El*Oy$w!Hzb`dj3Oo+>a&*#qeL}J0s$&;u~MHK*<eQR}q`3i`gDe`U7NJ0$cq|qKlJeuf#TlJ38rKR#)^Qn>3dBKz=I=x&l4x>tW?Mc5{NioMUTlN&(mZXU6IUAIFluV^WF~vB(Kp78ayEcner(G-*nSwDH#CDv;N};lNH&JZ|iXFA9`7xnxF!BkuVWNO2Z!4O_>7}GD%DRl)hibxzR6HU&Ou1b8(Gjx*>dIzR`GY~2V0W>AsHWxFWdoi4Zp&PvxZS#|Gsl%Ja}>>w!U>cmuni$ts8x1#9IZ0F5T=J=z&@;xQ8BZ>oTW57y=2ImK$))6WEF6r9+gC~7h<?oJ+tHx*h%!@68q$OR2n8tV3rv-L7Jmqry_9=9Z6nGM$Mw1FuDy4nBKE8meS*z%5pNtp32(R7F?QBO0IGsnNIHEA%V1TJFVvxaW<apm*WSME^i9uB|{yIH~?8tYRlGc;0W(E!I}A*q*@IXGDF-=B}pmqRE#vY>wy|_R5CJi*2PS>_z0|WgO&It=jr62pe-}M>0=*?Vk)7imTKWcgG|D8YXUb?9VUtft<u!I0D-BYgZk#mQj}PDCh=6vTwO{P!E<+6=V4i?nAy~_lTz8hWg$2T%z!y!YOMrueueDqK6-Z|iAGA7YWc=A36<rg+5ptG#hyGXvL~flAM&I=S}^U_e`@}um~v02Q{(QdtM)0S;X(ztM80<h*<G@fwqxRwrwDB{zdRNv@7hs{7{e=M^t=tFu%q60@vC6QE#%*2Cq>F4fwz&uy)&Ua5jm<*8p?R84DQ&>w~AqP-i5{&Ypdc}7|m(8=mPM;1{sVfbFj72<I7T#Ogjh?vSCz`8VoslCIVHLr%IjylG9ipV<1JQSM1lHsHNfhT{|y<1!V03dpitl6BBmSmO3*aQkv<5PIF2!%^9Fk+Q^u!{)9F}b7iwdId~4|QP8fmLTH&tdf0R_bJA#QB6wca%(_?D4T`f2c*%#05^u^l5Hkrwgaev$4K5<b<pOgo#&LCso+#(+=sP*hF)e9p(U5}(gRlt}p#C#!fJr`FPLWj#eRxe3&V!DT<ypNEzuOW#q|CD{Gc%`^(SkDfTZFe(L-)wKmMR~xrP4&{a<3yqAHVka_QRs3iyFADR9$|+rqKdpAM%Wsm~cv{i8UhrvdZYg$gbAMLe@Z5>nx}8wVG%zEe|YXm6rGPRYa3$v7pWQ@(P6Jqy1uwgknckb6LM(<`*Srm8>fr!YjJzzGU6hSiTGnvbq!&Tfg8+ON)|dbyQgxq@!eEm8ho~7bNqE>+laLEGbj%ELNznU)_N35!rTIXPUBcD9+iY!lP65j^UOPE2NIe;86&3X@h`n9t+d@l1y!QR4u|L#Nxf8q1>WpPJumvour^dTZtWqJySKQTvpyubZDglh@9tStEi5m)bVu`*QsRc43XCCaHLgp+O#UFv^)k*X$+JLG3cQp>DP6Lky=-jlOj>H>YBgad3aTU%Y+P5HC)g@H*yf92R#RqhY&TT=bULsmuK|6W~pCQWxQ7s<V>WiD8&$%HzbqZ3oqACsx#c{bE5()s{t(8r&NKYq*^$WavOST#bQLVXS5>{%KO9#k-mP-J;KS8`!1>~Z!hv#Upl(jSB$ks2T!2N#Y%RCKZ&DWHE(vTP##yr<4kiQ{3YDyJw!c~YeaK)hA7;ybvE;-DT$B!2RZI6hP}^Qq0K&*f>&S5boHumXMsAU^ph;nc85?IK6G)3YHu-}y3R(?<;xgIt*cV)MuSLKCE^>)(P(i#J<6ljsIALdv#J@zO{EL{<xsUJ!EZP}OfFK_?bLti6mvT@j1MXd#%n`H<y8~y@rplFRE+`~1qD24Nl{;rpePoxHV%2P=#n~~nE;(zh~>OCBeZRSuv4ZbtjhHkE2t|`!VWn+DQKgo{<?TL$91+An5@Zn`6kiDP+B9c3(A5ObnSK!JkLx4d7;~o)Y}L$@S<|0B-?J=Um|r~+ExwcEY)OI*pWhxXRq8HZwJ7<)Y>PHvubeSPCIF4Jhhse4{dfW<C@Pe0&kBkL)8hS3qU2Y-Ux$!*_O#Emm9I|BY1y_xwZM7%lEZXg-wSoY!4jdS1+;NZvoqiqA|42W{@dkR9Y3SF9|J88fcaMwX3>aN#`ZQX)1$h^2~BBrxcg2R}}WeV%!WjA=7u~(em69tzqED!lSiP!Un3j6BVJ#jM`;~RvkKC?LMJyM$RdYq*E>7u44IW=Jf9PnJbhEaq>`gvYIip#e8U;{HR6Q+Yl0C*WKHpy$#f13C34xsf0P5tFz@=iZ~@DW+u$I0u(G`JgKFiBxZnEyarb2g@_4-V!v2HGw_iR(%;0Omuk>#N;Q|ML&YTJB8YNYEI#125#KY%Vfsq$LL)EXk8)R;f7)qy;IxO=eOc0)GA0uwZ&3?|iCQO{SZg3)kxDvt1mxXWx{Q}~NFwtQRDnCGU~b{aJ~h@8xKup-wnPitBVc<g3g64iW1FG;Xa`8_o1Ee`8ZDZglIOevYD{JL202ZC`-nRNcHUJ5WdcOp(IC@vq?%@FfIIB~g$)sP$z)?siIURdhw!$w3dGejFH=`YRn_k;>7dc#al}2U!da`sz_p}+e?TMCl}e*DA7H1l#%t00{66M<L??Zj3bw)<tN=+!vVbd1Z`4~*Zdq5cw0o)}WE>ngUpIN9TEoU`6MmOEdz#`tGcML<;WD~OC5;lMrCDj6tcuT4PfI~NuXU>CeL^1b#62zbCpjFI0ELz&krs2FKp{7uKIN$;vPXFTG;ah+ZPb0^GVd+_cK@hK6Wd8%JZ=SBy&M-f+&vA$5_HYG^tX>{*sj#7qmP#~k<!%eKP-qA&oP;W4_3pL*f&LJS}%7KME%dG3LkQD8;YLmJtk)%Q}HqV*NVEX6ackKu&2;!8p9{iw)E{t<W#D7!a@y-L9d0G5+4E_M!6RTx{OQOJU)`!F3S^$`G4eSW9KR?2GO+6U1Q2cgOI@ZloEJRN_XMF>#t>_OrGc-$<`19TW-i(5v{bDyRom_z4r1C)62KFA3pZ<GW?NOP`N=sAD#w-s}F6agA=+=X$0UD7(8j?$n1b?VvD~a)5L}Y^jR8@oFdo0wH^BXH{`z--*`)7p24P0$Z-4n?jLvm3-43V%>')).decode("utf-8"))
_V5_LOW_META_SALES = {148: {'WOOL': 6}, 151: {'WOOL': 6}, 197: {'MILK': 12}, 222: {'WOOL': 4}, 223: {'WOOL': 4}, 256: {'MELON': 12}, 257: {'MELON': 12}, 258: {'MELON': 12}, 259: {'MELON': 12}, 262: {'MELON': 12}, 264: {'MELON': 12, 'MILK': 6}, 288: {'MILK': 6}, 312: {'MILK': 6}, 336: {'MILK': 9}, 357: {'WOOL': 14}, 360: {'MILK': 6}, 366: {'MILK': 12}, 378: {'WOOL': 6}, 380: {'STRAWBERRY': 6}, 384: {'MILK': 6, 'STRAWBERRY': 2}, 396: {'MELON': 6}, 408: {'MELON': 6, 'MILK': 6}, 415: {'WOOL': 17}, 420: {'MELON': 12}, 421: {'MELON': 5}, 422: {'MELON': 1}, 427: {'WOOL': 1}, 428: {'STRAWBERRY': 6}, 430: {'MELON': 6}, 431: {'MELON': 6}, 432: {'MILK': 24, 'STRAWBERRY': 8, 'MELON': 2}, 438: {'MELON': 2}, 439: {'MELON': 1}, 440: {'MELON': 1}, 453: {'STRAWBERRY': 5}, 454: {'WOOL': 4}, 456: {'MILK': 6, 'STRAWBERRY': 2}, 473: {'WOOL': 2}, 474: {'WOOL': 6}, 476: {'STRAWBERRY': 6}, 480: {'MILK': 25, 'STRAWBERRY': 8}, 481: {'MILK': 5}, 504: {'STRAWBERRY': 8}, 510: {'MILK': 6}, 516: {'WOOL': 5}, 517: {'WOOL': 1}, 519: {'STRAWBERRY': 6, 'WOOL': 2}, 525: {'STRAWBERRY': 14, 'MILK': 3}, 528: {'STRAWBERRY': 24, 'MILK': 2}, 545: {'MILK': 19}, 551: {'STRAWBERRY': 8}, 552: {'STRAWBERRY': 13, 'MILK': 6}, 561: {'WOOL': 1}, 564: {'WOOL': 11}, 567: {'STRAWBERRY': 6}, 571: {'STRAWBERRY': 8}, 575: {'STRAWBERRY': 6}, 576: {'STRAWBERRY': 18}, 579: {'WOOL': 4}, 582: {'MILK': 1}, 583: {'MILK': 17}, 585: {'MILK': 6}, 599: {'MILK': 6}, 600: {'STRAWBERRY': 20}, 606: {'WOOL': 5}, 607: {'STRAWBERRY': 2}, 611: {'MILK': 6}, 615: {'WOOL': 3, 'STRAWBERRY': 6}, 620: {'STRAWBERRY': 8}, 624: {'STRAWBERRY': 9, 'WOOL': 2}, 628: {'WOOL': 2}, 631: {'MILK': 10}, 634: {'MILK': 14}, 648: {'STRAWBERRY': 13, 'MILK': 6, 'WOOL': 4}, 663: {'STRAWBERRY': 6}, 668: {'WOOL': 4}, 669: {'STRAWBERRY': 8}, 672: {'MILK': 24, 'STRAWBERRY': 16, 'WOOL': 4}, 695: {'STRAWBERRY': 2}, 696: {'STRAWBERRY': 10, 'MILK': 6, 'WOOL': 4}, 713: {'MILK': 6}, 717: {'MILK': 15, 'WOOL': 4}, 718: {'MILK': 3}}
_V5_HIGH_META_SALES = {148: {'WOOL': 6}, 151: {'WOOL': 6}, 193: {'MILK': 6}, 197: {'MILK': 6}, 222: {'WOOL': 4}, 223: {'WOOL': 4}, 256: {'MELON': 12}, 257: {'MELON': 24}, 259: {'MELON': 12}, 262: {'MELON': 12}, 264: {'MELON': 12, 'MILK': 6}, 288: {'MILK': 6}, 312: {'MILK': 6, 'WOOL': 8}, 336: {'MILK': 9, 'WOOL': 6}, 360: {'MILK': 6, 'WOOL': 6}, 367: {'WOOL': 6}, 384: {'MILK': 18, 'WOOL': 14, 'STRAWBERRY': 8}, 396: {'MELON': 6}, 408: {'MELON': 6, 'WOOL': 4, 'MILK': 6}, 414: {'WOOL': 12}, 420: {'MELON': 6}, 424: {'MELON': 12}, 430: {'MILK': 3}, 432: {'MELON': 17, 'STRAWBERRY': 8, 'MILK': 9, 'WOOL': 4}, 437: {'MELON': 1}, 455: {'MILK': 3}, 456: {'WOOL': 22, 'STRAWBERRY': 14, 'MILK': 3}, 468: {'WOOL': 4}, 475: {'STRAWBERRY': 6}, 480: {'STRAWBERRY': 10, 'MILK': 12, 'WOOL': 6}, 504: {'STRAWBERRY': 6, 'MILK': 3, 'WOOL': 12}, 509: {'MILK': 3}, 516: {'WOOL': 4}, 519: {'STRAWBERRY': 10}, 520: {'WOOL': 5}, 528: {'STRAWBERRY': 29, 'WOOL': 16, 'MILK': 12}, 552: {'MILK': 6, 'WOOL': 8}, 553: {'STRAWBERRY': 11}, 562: {'WOOL': 8}, 563: {'WOOL': 6}, 571: {'STRAWBERRY': 6}, 576: {'MILK': 12, 'WOOL': 4, 'STRAWBERRY': 17}, 590: {'STRAWBERRY': 1}, 591: {'STRAWBERRY': 15, 'WOOL': 8}, 600: {'WOOL': 16}, 605: {'MILK': 5}, 606: {'STRAWBERRY': 7}, 607: {'MILK': 1}, 612: {'WOOL': 4}, 619: {'STRAWBERRY': 1}, 622: {'STRAWBERRY': 2}, 623: {'WOOL': 4}, 624: {'MILK': 11}, 629: {'STRAWBERRY': 4, 'MILK': 1}, 634: {'STRAWBERRY': 10}, 642: {'STRAWBERRY': 13}, 648: {'WOOL': 16}, 649: {'MILK': 6, 'STRAWBERRY': 8}, 652: {'STRAWBERRY': 8}, 663: {'WOOL': 4}, 664: {'STRAWBERRY': 6, 'WOOL': 4}, 665: {'STRAWBERRY': 1}, 666: {'STRAWBERRY': 9}, 671: {'WOOL': 4}, 672: {'STRAWBERRY': 14, 'MILK': 12, 'WOOL': 12}, 696: {'MILK': 6, 'STRAWBERRY': 3, 'WOOL': 8}, 713: {'MILK': 6}, 714: {'STRAWBERRY': 2, 'WOOL': 8}, 717: {'MILK': 6, 'WOOL': 8}}


_V7_MILK_SUPPORT = {"PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP"}
_V8_ECONOMIC_TILES = (
    "COW",
    "SHEEP",
    "WHEAT",
    "MELON",
    "STRAWBERRY",
    "PASTURE",
)
_V8_ROUTE_DISTANCE_THRESHOLD = 3
_V10_V5_GATE_STEP = 72
_V5_ROUTE_DECISION_STEP = 168
_ROUTE_STATE = {
    0: {
        "last_step": -1,
        "legacy": None,
        "label": None,
        "third_yarn_milk": None,
        "v5_gate": None,
        "v5_shops": (),
        "v5_expert": None,
    },
    1: {
        "last_step": -1,
        "legacy": None,
        "label": None,
        "third_yarn_milk": None,
        "v5_gate": None,
        "v5_shops": (),
        "v5_expert": None,
    },
}
_ACTION_CACHE = {
    0: {"step": -1, "signature": None, "action": None},
    1: {"step": -1, "signature": None, "action": None},
}


def _action_cache_signature(obs):
    try:
        payload = {
            str(key): value
            for key, value in obs.items()
            if str(key) != "remainingOverageTime"
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    except (AttributeError, TypeError, ValueError):
        return None


def _public_shops(obs):
    """Normalize public shops; malformed values expose no routing signal."""
    try:
        shops = _get(
            _get(obs, "town", {}) or {},
            "unlocked_shops",
            (),
        )
    except (AttributeError, TypeError, ValueError):
        return ()
    if not isinstance(shops, (list, tuple)):
        return ()
    if not all(isinstance(shop, str) for shop in shops):
        return ()
    return list(shops)


def _v7_route_label(obs):
    shops = _public_shops(obs)
    if shops[:1] == ["YARN_STORE"]:
        return "6c12s_4q_first_yarn"
    if "YARN_STORE" in shops[:2]:
        return "6c12s_4q_second_yarn"
    if "YARN_STORE" in shops[:3]:
        return "6c8s_3q"
    if _V7_MILK_SUPPORT.intersection(shops[:3]):
        return "10c4s_3q"
    return "8c6s_3q"


def _v8_economic_tile_counts(farm):
    counts = Counter()
    for row in list(_get(farm, "tiles", []) or []):
        for tile in list(row or []):
            if not isinstance(tile, dict):
                continue
            animal = tile.get("animal")
            crop = tile.get("crop")
            if animal in ("COW", "SHEEP"):
                counts[animal] += 1
            elif crop in ("WHEAT", "MELON", "STRAWBERRY"):
                counts[crop] += 1
            elif tile.get("kind") == "PASTURE" and not animal:
                counts["PASTURE"] += 1
    return counts


def _v8_public_route_distance(obs):
    farms = list(_get(obs, "farms", []) or [])
    if len(farms) < 2:
        return 0
    seat = _seat(obs)
    own = _v8_economic_tile_counts(farms[seat])
    opponent = _v8_economic_tile_counts(farms[1 - seat])
    return sum(abs(own[item] - opponent[item]) for item in _V8_ECONOMIC_TILES)


def _v10_public_money(farm):
    """Return a finite, explicitly present public balance or ``None``."""
    missing = object()
    try:
        value = _get(farm, "money", missing)
    except (AttributeError, TypeError, ValueError):
        return None
    if value is missing or isinstance(value, bool):
        return None
    try:
        money = float(value)
    except (TypeError, ValueError):
        return None
    return money if math.isfinite(money) else None


def _v10_opening_tile_counts(farm):
    """Strictly count the four public opening features without throwing."""
    try:
        tiles = _get(farm, "tiles", None)
    except (AttributeError, TypeError, ValueError):
        return None
    if not isinstance(tiles, (list, tuple)):
        return None
    counts = Counter()
    for row in tiles:
        if not isinstance(row, (list, tuple)):
            return None
        for tile in row:
            if tile is None or tile == "LOCKED":
                continue
            if not isinstance(tile, dict):
                return None
            animal = tile.get("animal")
            crop = tile.get("crop")
            if animal in ("COW", "SHEEP"):
                counts[animal] += 1
            elif crop in ("WHEAT", "MELON"):
                counts[crop] += 1
    return counts


def _v10_should_use_v5(obs):
    """Select V5 only from the corrected seat-relative step-72 public gate."""
    try:
        farms = _get(obs, "farms", None)
    except (AttributeError, TypeError, ValueError):
        return False
    if not isinstance(farms, (list, tuple)) or len(farms) < 2:
        return False
    shops = _public_shops(obs)
    if not shops:
        return False
    seat = _seat(obs)
    own = farms[seat]
    opponent = farms[1 - seat]
    own_money = _v10_public_money(own)
    opponent_money = _v10_public_money(opponent)
    opponent_tiles = _v10_opening_tile_counts(opponent)
    if own_money is None or opponent_money is None or opponent_tiles is None:
        return False
    first_shop = shops[0]
    return (
        first_shop in {"BAKERY", "PIZZA_SHOP"}
        and opponent_tiles["COW"] == 1
        and opponent_tiles["SHEEP"] == 4
        and opponent_tiles["WHEAT"] == 5
        and opponent_tiles["MELON"] in {4, 5}
        and own_money < opponent_money
    )


def _v10_v5_route(state, step):
    """Preserve V5's sticky step-168 low/high public-shop selector."""
    if state.get("v5_expert") is None and step >= _V5_ROUTE_DECISION_STEP:
        shops = tuple(state.get("v5_shops") or ())
        dominated = (
            len(shops) >= 2
            and shops[0] == "ICE_CREAM_SHOP"
            and shops[1] == "YARN_STORE"
        )
        state["v5_expert"] = (
            "high" if "YARN_STORE" in shops and not dominated else "low"
        )
    if state.get("v5_expert") == "high":
        return _V5_HIGH_ACTIONS, _V5_HIGH_META_SALES
    return _V5_LOW_ACTIONS, _V5_LOW_META_SALES


def _v8_route_label(obs, state):
    label = _v7_route_label(obs)
    if label != "6c8s_3q" or state.get("legacy"):
        return label
    shops = _public_shops(obs)
    if not _V7_MILK_SUPPORT.intersection(shops[:2]):
        return label
    decision = state.get("third_yarn_milk")
    if decision is None:
        decision = (
            "10c4s_3q"
            if _v8_public_route_distance(obs) >= _V8_ROUTE_DISTANCE_THRESHOLD
            else label
        )
        state["third_yarn_milk"] = decision
    return decision


def _leader_opening_profile(obs):
    """Detect the leaderboard leader's distinctive public opening layout.

    The leader opens 5 COW + 1 SHEEP with an 18-wheat field, visible from day
    one; the frozen pool and most public agents open cow-light/sheep-heavy
    instead.  Only public tile state is used.  Returns True/False, or None
    when the opponent tiles are not readable.
    """
    try:
        farms = list(_get(obs, "farms", []) or [])
    except TypeError:
        return None
    if len(farms) < 2:
        return None
    opponent = farms[1 - _seat(obs)]
    tiles = _get(opponent, "tiles", [])
    if not isinstance(tiles, (list, tuple)):
        return None
    counts = Counter()
    for row in tiles:
        if not isinstance(row, (list, tuple)):
            return None
        for tile in row:
            if not isinstance(tile, dict):
                continue
            value = tile.get("animal") or tile.get("crop")
            if value:
                counts[str(value)] += 1
    if not counts:
        return None
    return (
        counts.get("COW", 0) >= 4
        and counts.get("SHEEP", 0) <= 2
        and counts.get("WHEAT", 0) >= 12
    )


def _leader_aware_label(obs, state, step):
    """Suppress the 10c4s milk route against leader-profile opponents.

    The 10c4s route ties or beats the frozen pool (mirror-like agents) but
    loses badly to the leader's tape unless PIZZA_SHOP demand is present.
    Routing therefore stays unchanged by default and only demotes 10c4s to
    the 8c6s default when the opponent shows the leader's cow-heavy opening
    and no pizza demand justifies the milk route.  The opening profile is
    cached by ``_select_route`` during steps 24-96 regardless of the current
    label, because milk-support shops may unlock only after that window.
    """
    label = _v8_route_label(obs, state)
    if label != "10c4s_3q":
        return label
    if not state.get("leader_profile"):
        return label
    if "PIZZA_SHOP" in _public_shops(obs)[:3]:
        return label
    return "8c6s_3q"


def _v7_legacy_layout(obs):
    seat = _seat(obs)
    farms = list(_get(obs, "farms", []) or [])
    opponent = farms[1 - seat] if len(farms) >= 2 else {}
    counts = Counter()
    for row in list(_get(opponent, "tiles", []) or []):
        for tile in list(row or []):
            if not isinstance(tile, dict):
                continue
            key = tile.get("crop") or tile.get("animal")
            if key:
                counts[str(key)] += 1
            if tile.get("kind") == "PASTURE" and not tile.get("animal"):
                counts["EMPTY_PASTURE"] += 1
    try:
        money = float(_get(opponent, "money", 0) or 0)
    except (TypeError, ValueError):
        return False
    return (
        counts["WHEAT"] == 5
        and counts["MELON"] == 5
        and counts["COW"] == 1
        and counts["SHEEP"] == 4
        and counts["EMPTY_PASTURE"] == 0
        and money <= 12
    )


def _v7_sales_schedule(actions):
    schedule = {}
    for step, action in enumerate(actions):
        sales = {}
        for order in (action or {}).get("market", []) or []:
            if (
                isinstance(order, list)
                and len(order) >= 3
                and order[0] == "SELL"
                and order[1] in _META_ITEMS
            ):
                sales[order[1]] = sales.get(order[1], 0) + max(0, int(order[2] or 0))
        if sales:
            schedule[step] = sales
    return schedule


_ACTIONS_REPLAY_1 = json.loads(zlib.decompress(base64.b85decode('c-rk<O>Z1oa{McT&U0XYuu1yHk$OkMazufmwy_=%g8{sY1&sA!?3>~LZc$`+RaZr3MC5x-X@NPZMK-J6_sfiojQr()U;q8L-~aiy-(UaRt6yG!y#Dm*^}`RZUjO5_|N4*re*DqnfByN~@BjI?|9Sl1FRy?6{MTPU-rc_a{O11kmtXDPZLc3cELLB>_{-~0+nXEk<M@vr{_lrZM=khpdw2gXZ-V!d^RK^r_x^7C+WPePxa$w^f4=_ut~a;4FaIpTZ$7=-Za;qg-K;O4Za+`^@@0tMzxng$kNanSec*o7N4-D#IQf&~@tD1J`1VuNChs3Vm%R7K&+l*E{`%!x_n#j}MSkzo&`;hwd6?Aio9j2*pxb1=r)%U~T4~c)hK<~9KixlldUHJ=n)bHspYKfE(5Bf6Xl&ko(SO=*-#-54=k3ky2fXBGvrK#NWyC++4^NGMHeFsP>eOQ1sl%dx8wxh|(7oOD{q}DD@#|dmUNwJu?8>BdqnC~vbyzCuZa?MlK5d~%vxmi;u9VUDCX@7XYaVS@c~PJ*KF#BcuJ1`3j1@Hcb$k}?8*#X@!6@#ZGk*8s28HY3aL*jIC)`>}BfwOmrHCeQ)|#vh``K8zvq2UXnwIIG^qe5LILHJ&{YkMEa|`vvGqlv&kk5;>^_hKzdJcylS_dyO>iHUYZjRChchpC3QAZt`5j{qI_S(WL^5;%JwOHoU*@(R&&4Pxu1)O>9BAvHA_#xWTl8H2G=l<8?(~#vdJYxS_^<lR+H`_P&zy4`^cmMw8{lCu-+u?!uyROFu{nO~t2m5OJi(pspEt1jKACH#AQwMk9_Ikb|MmE9B`%%$~#Kw<@pN&A=3^*3*5qH?@z=KXsb+Oy&8|Opabd-%AcjAV_1ENP4hSTk7X`ZSBql2i!9TM&7=1r5o^*UXq<$JKlJf7-~MyukFrfHUqX~q2TYAwOU-~v)GV99h~2&T4Fkr_e28gl6-W;8c5$g3q|27{~Q!P1(_r(uc%bejYW<4G-cMtpDZ_#+OD=PvD+7k&=H^cnF!mNaX=G%h&213Ped^1JK1zq9~U`CJUEr|$5|vvTN4JG|gb*ccL2F$T%6=(AanlQ6xhGJ`T*B=AaGhvCY_3<S<>xoKRI9<b#l#x4g4I7_2Xo(uy}&kIVO*L-wP(<Q?z-*zt#F4@M|s)#B{wik(qsvip%U1og=W(Hs@xB;-zdkaTw?>Ay}5M7G#r=|&mN0n_$pt(Vv7>(5N&De6?^I4l?DoXSN-`3Nmx_YoD6?8o^8;W57bafv^fur8e$tBL6MPlotkLipw-2!u8X*T5WGCPSKhI=fpHrJY_>s-6W^|u5tbAu7MGG9yiBG4RMCFWo+!y9|4<)IP$nHiQCSt=p!WA3%#)nyxr7^9;%WRyVZRn9yfW&lR#^B0%R8EC+YFRk0O37M~G<(_x3a@8eDqLsZdM`i)Ol%?5VUk>Mlj7v$VDVm8a5ZPp3P6NlM!N4-pz6o`N51v6&1$zs^TUFDtbQ=ycgRCxYR-VT2M@Cl|@~azT*fe1=Vke%M`*Xwevp{mwnFKMMbZNoP8PJ=v?vAG&^AXq@RIeYjxubOjnVQW}{v7Ux?-b!Ym8d`->~y9U2XcFsL)+-N&9juh^6lO2$C~v8y{PkMFq7iwT^J~BjgfYvXMU>hfwMU?gqI2_WAyq5!MI+ARJv)tO<M>Yo@<BaMtzM=zRuWkkGS>l3^atj%=nn;s9((aRA9iXll?m!g=ml(;!OqALL=LchJ!4|__P_DB%ki@u6I9f@9zGJ_X+l}_?x?Q7Gg|1=Il~P5mG)H7sC@mofz)EEErL}5p)8=$aA6&($T80Z8E2y&Rb<#0$MFS(X%wCV7zjg?6f?N(gt$J>)bqJ_p7@LRU`nj%lzE1mtAPU4Ga+>!`;tTmkmBOe=#tEh{=*9X2d4jyhWq+5`_7btdMz|hl^fID=BQ@;S~uc2o2fjTCZ&OqYanXfF8e8IslOM0|y2Dn)iQX;NRXp{<{%9m_yWK|7T%y#u=@Fu`|PCNF!6<a!{4{a%8<#)F(y{sd#gvDT?~XjlAI@VIZrX64d6S9>P5^WC_ipoUKKsPPNydJq@yYV6zdRf;2TCXtF%fbvwd#LNGF=IvOdV3+qw~vPCEHz>NKS{6jF*raTI05Ih$}_ElLRWi^AQnIDLn4zI6S){<zFA;ANw6>wLx@R=f5prt1U9U|MCAHR4BOix_Hor;1H%LmsPXJ)lWMDw-~I`!kE$jk@9jV)(LL9BwEEj*hioY0j;?B<I!oK!-m%Xj(MvMxBtOmBkt{3aD|4jf-Sm~#&gBTVgLTX|wWF4>XoEQd@+L79IRh5rWgA8qr@VYjJ2%agh6E%DgcC;s8pMJyzDY{2rPXo%zF$tIJ9d-hNdgaCUUd9uWo)Cf1$J&c3#`Op@^ASgaDKG3$zig4U&4dsn&{E;vPu)TyoBVIH!_R*XQ!IB2=7a8FhXp#H3t%rcou*j*D<Ej)*B$2CORic|SyDrg~3LIxLV57kA%sm{rw;4q@zr*Q-!h4SHZn)FLw0|%30$~fzls~j89Yx9JW~Kmc0Tav=jFOU5r4Aw4s{0!RC-o)*CvK2s>1(}FH)nqMPcfHL_84*Ca0^E}+zW{>TJ37wo+QU#z)M<oaxUX0g~DNvy3i&}WFgBzv5`f0HiKb+Kb6VBT4)DH^~tpKkP{*RDf}U|DqIW$N=xfrD!3^Vy)$R7YTl~4q-^)$G!f-KE-O5mnezFBcSu9Mok(KGa00n>;qQm7m!bV_Bqka?IO+x*bTp!cMh&(eZpbJCzc&niet+}lLqJwxm!&y8&re${vxw^^Kr#j`|3XX>1;bH{8%8RCXn*3sjUIuuqUGow<=}GngNHLvfOyo+*?CY8$Y8?)ZA+3LL-1OGCQvbfNO&D?t|_(8j$yBwQxcI&PonH|NqriLY3B<<iU%A@go{XcgdcCM<pWtHT+}ak9>v1*YSVKdGrE!V(iW`;gpt^$_&|&i*a>(YH4srLl_8uV$MrEpTkD7jlCh}60o1wv1}<zR!NM6#5~eU-*?ae(+^uL4MEv358&C7ppKb%)ADt^5Cfy0ENwc6CCz@<z?f2aT4`F6;E)uE9H7p;Ri0DzkH@nM88_o78#XlnZ)NP5(Z^s`o8>*Ll$x8;PTiE3=kSNi_(_}m{y+EFB$~uqTzY--CZEmq`OTwZDVR~KQyp!GUqys{edgS?sQ7Z1xwkh}r@(tX_<&_uePHZcj27S}5?vo>wxL~)cO@k0X<P8jF<#fZpm~$KIoUz!t#i2J~9Q*8nu)#DRVoi0q<E1?z{alL7C8DC};G328N_Yw|Ylt&hI@J4H(W|M6FqX$@_{ovQetVV{V<hNATSyNDN_dSM*w@Wuw`1MbG{4Ylf{V>yEi<LD2oUm@q@)5kV$p3x>>4-6pt`(tQnqqlp`laK@J!60P*9Mu>IDejCHDu3rw-dBmo?T>4AN+~5$h*FA<JDflSBllU|4s9QIgw!l1ZfJfF?Wvvi{}rhHbJJ6jg9BtM4Tn{dC0l{1e%l)P&)+;eWcl{j`;$#w)jL1&w=(Hk_BM3I#gDuqg41cN89bCP+-ExK49&Ofq3|?kA{OOfeEsAn9B5t`pMZQ~7~rJp&;G7JomwZJ=nA(%wA5K8)OLbH@A3j@7V*x+D^#;2SAz1e;Y=c`B`pvi}eeMGKwoD?o2>5>CiKI{LF{zpm+Jah^b&<9CF4x~Lay0E0iHPs8<Kj1-?kx$Sj+uY_j9x$ZrouE3*!4~%{n5kH%a%VKG>oiNT2bc7{w5aE{D@HOp@bNM#YDVa}Jn$%Y(`34ah4_(v-VM1M0Su0Y!EIx*x66fFC&IRfOM+gxYp9fepSk4`kjp{*7JHyv|nr{K=y8`k+1f;TEASg4CRlsRhX=XMClh8t!)LWW%bt;;%lhV7z8B5MGRh@XuIEEL^=o}t;F<r5&k}Sl<c&~^@_uTfY)<h??I1c?EoxFs{5v1|M{O73e<ALp%`~!VA6w?m12#`oWfMMeS<mI|r)77>a|23$vlAazkGkrRO9cK)lc7i^)fVV+nz;#gsioDDJ<fgTk3;lo#Nibt$;BQrc5#7X5jQ6I|ux31z>ig{xM1^={i+9l!4;XI*KO?nuO4^@g(!6FkBSOc~sSM2uO<Z)9XQ(OJtSRHGKqh4gp*bICbWaOs_*B>LWa@K{l6x%ZC^8!0p+Kt~v~s*hGU4blKtlURekWaNv<H)|lzQiWLW`p?%mf-@?Oc-GW2p~%OO({1wXpM?geNgG3IxQ~)GFvEW1J<B2r^Dfm!8le-wH-<gan}wsNaerYDz7Fwp&y*u_5~4<)IOoB8<?%k&?JQ1TUc_d(pA0WUtKbkY?i9vZU%5NygHhhHgIW^@ayD-=WQ#q?B`M?ZP}r+nO>*vX7#$l}sy=kC_u`-v|<;PKgF(>PUt26n8PiNV=`YTz)~72dR`(QiAkZ*=btvQO+-IR(jbfB{#zhB&q(cEGfQ&T#B<=HD3BcHdzI&TO(5%`CqIKM%FR)rsyIRL>3Y&=4GEfS{27;IU#A+*G?UYA^IKi3NNaT>A6DG5_xy{+boUTkBE|@FRb!_U11j<7s!H+2v|%C${r%bAL3~bFp6q@ncReNAaRt5W%^h~G8YpcBpW`=@M3y4P$LGcR`gqwJ|FB2=+4nxTtsHu^{ve2EK0%ThZe!qZmJETuoTI;6V<hI{FJ;P$4pd=osTTCE0QMacfEXcN_V>977L0cnMJ#8J71lu_4EMiZ=3TDz|1e=V<fVa1=kL;gwcsbih}xrlW4@8B^%SND@n8`Tdi>1RK-xC>P*kh@Mr-CoHQ5sH2J<T;ab#vVcJX$vc%AAAh77+*N}qVkc;B1SQ5%?a`?pBI6@wswZT%_3*jB_4Faj*FmwtbOpj31pB_|Z4;A=6f=`b<?@f0vU(?n?M2>7rhR9*W{*bEWOqSqTd(B8W&k@Jbl5VZ5bQB?Tn(7;|`O=V#inYyB9(Y1m%+YAG{z)PjrUlbmLLw{Xg2s>}4#&w62zCkp$FwiJU6q^3s=LBsB4lZHs~&>g59EmtL?g6b%f(pZnP3_pImwB{&vFV)L1#569>?G4#AJz5n0B+(c-N#TLQM%wUdEheLw6JlccD3J@>FyV39HNDEa0}|LN6O)jI7S|Y122RnLI4r-b^<~yNiT2tuWm5EbCj5!YhXw|0h4!3dj_RwBnjp4M;0d%4$MZ_<V0GOG5*P3AL2S2+&X(9XG-ACtIlaF@tnEZz5GchD9sQl0kZnsUCs<E>V4ESiek&U)m(_a>xV=mO_*-`l~?GB5?CBG6Z0pFBD|~E#*wwV4;)2VZvd#G*<$(O~P|4$qo=o8tn*s60tFSw=yq$u)|j?LJbLMr{!p@?D~GGp%0fk@XjRXN-*^a6$~lGK~y%+z?@MRHcj<SM|#Af1i*oe0i6^hQ<L;-)hGZ(viBe$6~vP?9L}k8f?}??3OCB4=lMOE)0!JMDrL~i<(aPT)9g0B4)smi5hfreIEfrnm9QKesYD3z913<=PBMYOcNyAZb<K7a0*S6|D;9012Ebu7<!uFrv7i@jp;sjAZ#s=_JRQX{Byy$@RVJ||X{A>5jg!?tRxbQ{!Qo|~Hc!wrcz#wjv9=r*5>{eFexodwd*}<G*RU`pu}JYC9W9u+bbEGm<Fq;()spOhlO+w5{*W51p%Z-UA7|Mf(AehegzZm19SrmDD)%5~8^^rm*gcX(jVb7`Mj^ke<EcVZ>zaDx-sD0YK&Ds^>dO*tOxW2GEaWtFQYb=ICs7KS)=R#Mq<O|vks6iPcSW!U5}jf&@BAQdwh{$i0g4nNyjid^>*d8|vEhp36s6AKJDhUXmaP(KQs|7a(NmR{nfzN{vmO(!Qen%9S!|X@>rn)gS(fl^R#ME?GNjOcn2ZuGU*92T%)u@CBk+vH5IbKXr99n3Rre)d`FTPzuI>xxlOTPgA@HZd0u%`J&59JIN&|kJ0Xo2W^>pD9u|N}v?R{1O#jRS8yA-3YCki5)%Mvns`~D}mO=UU1vK7XT5CZQA60a=^8IGFVWaud4lA(?urtxiPDwB>ujxm|BHi{ZDy~6FUV@-km$d9~+U=X<%6zYu-Rm|~OY9Jp;`&>FkvUN+<_&v0al}D?ACwz_sEl+|31!NU2$l9JCp*~^$b4BStN(u?Ukt?c;o2%VUy}WauAx~~>f>K1IHuCONRHtz5t8y4RWF{mGm$|c4y`B<#obb8ZV2>CGV_opF^a@m_3dFTMD<V?_&0ECofrT>$SJAt5%z`EwBN;O4jRNihn@oxgF{z1RMk2DQRnfsw-pIp7%KRVzglTf_46rOvte`7^`g^UVn@La`&KajFQB+C`lEM}Xp;4Z*h>nkZ*%mEmmCmj+k3>d@swULr3(&xSv;&;O4ldCg4tb8tE!GwLJ_xLnGk_UigU>V6$r(E-YoS}<51;|Md@#kqB<+htocL%(l0TekcWnv`R@fU8aC10xV){f8+(o^qh<FlZNA@7OTTnY6uF*5-&usjxe}eDeEw#}cbDTo#ocdw^HxD|+ChfyE&C27I(6DPFm(7|t$uT^L`VCEjWq}#XL~g_JaG(s|7X$@5`tkw2CbtZxb_<CTsZ4Bs5x`oqHnl6kmbdMsudYO{&dF#t6HqE%_d?*EBN$6iC6tQ>2v=GfTAa@Ggm7+R>u7^0Tx*Ztb`CGLrG2rfTDnWg#$=(;IyDvMndHc#sDyJK12XmIl2Bi8Vw3M8!qQ39MTv-lSPrMb5udN@3m<}pw|12zVnwD~a76?Wh?)X%kdcVgGzoUVX$U|KA|xOa&NIlhB2sPTilGstK%0b2dr`$j48E-j6`e_)#<|xFmRwO`Rx#n)lq4grlvhqk^x5>q7@f=HsAXXsqEb6MvpQ}WLFY7Pw8@E%f{=zf);Q1vuLHU$+!7Gses9qof(JZ-FQ|Y?aK7c6w6W4zZ0&@%d+g(xwUkS$^3>L0YGAmKItZ!Rd~+WDqm^QqK8qPgv$cYAkTL_WSg9rCJm6!Y;kMp5fEDU%tiVfR6k!Sr5-xTXb>OgnwM+thN0UPi@kK(S$oaL$ja)XCTtw3V1>n=l&Vp>eLh^^8l)?ByzZY0?hd&!dmr}9gaU!5VGh)=O?+K|wn-*d!lTcZF+*nCwZoTY0(s#@XJ8K}6nYmAl^q`chVZu|ZDqD<9F|)05o_YiY%|AA_l1SLG`Vet)x86jaOBGPNEqzQl^fb%t^qdgpJjz10GIxrS*l2`310j8x%bX@v;Sw;lP|LR@3<6^ImZ~IET9>yzSmn81O4*9m2`Q?}-Rgj@mMgtBrFJkr3c)8m7im{gg_SUJlD5L)IS?~aj#A3*Y)V{VdtDgwP{@YFkIDk#e1p?!MphUjO87p74pY=hvWrN#c5o>Y<3ynbS%uHV!$8ZHjJ+%ejILLrrs~Pm_(Yz2m^*D1-<+W%0V?Z2@rpnK#MWzM+mLp(_9d*O47P|72oEhRFiDU@qxi&G-2WwFI4mFfNYh6Iym<%-aRw5^DoEIr(4;e!k3sGRUr9cr(?wO%ES&5NO=c;*{>UGrfkSfaTFKey7;7nQ>wuRUr?;n`c)~V<d-p&=5<IQ%32{?Okg3$A2qmJSvD}p%;hg|EgA=ya6~0!LWLH?ORMYa3wJ0M|<_3rb<$eMrmB=b%5#wO)RT=w2jwzZ1M_(r}ka`wn;XZ~DB`5A>r({wh4#Kb5z_)ekUUdrc5!nz$=PK)HlM)u8d<pJ1yqaw$MT@$yQ$1D5WU#Z~;*8&hG+&Y+9vfhF`!Y|b*2Ssm=8kzo406~KP$ZgPSq5*_tAwCl*F0)7t2!&EjRsjlio6Xue5GxsR+#`oD_oO`i7{`*YM=S;t{0ndBOW>I<fWLzF`>y6Jg7zLkN4`9i#_p5Gs#?4XhcWn2Y?5b1?4nSQI_!DC*VRMfT|bLgO@SJTn*en%`>IB+Cj#eu)qauwUvTNPLiB=rDnlm#i0%&O&J0Si@Z><1J%2AR?Wsu9aMOr2zL(>pMa2}m<2?n;7I{_L%pjlOaT028QfXCB)G%Mh6gCXh9~%u+VWKXd};k$$`fpthvylFmk>f)XAqL2*_c$#2?G*R_Em<ttlI?AR$AaM$f%IyPnZNDBWRQh!3r4|0ihx`$PoR<1aCrzB2@q6!AVM(PhlIL&YtK+z~eqHeUd6!uQH>z3Z^sxJi9zmhE4(8IFh`3N1urk^%PZBmLIh1LfOpKhvTIr!8U<4ol|;5e_KMJc%n(}Qtzm8na74~!kQdt-Vz28fP<FmZ;XIoa}n~(KHw+xEL%uaT}WOPyBgEtTCQZxnJvr^FT1=Zk>m3wkf_Kxl7)3*&YPs0BxaDS>@enX(qw6wBrPboaU8>R^~vq+NxvTjE3}fCA(AImKe)`)ytEYv3mEG(J<dR4MKuz=yq3c)kQEkG9}ohP$pEH;xh|%2>1Qr$bx^HSLZ3fT@rlM*r4TZSm1HPfgEp(P#jK>rBCjj57SI^WY~VJh%}A8=0xW&;yC(r74&fbV<-yW|%Wsn-$!qa(`6iLS)FSA0;r5mIbUC`8mc&z%O~mSXz+2<0DbR<+WuJ)(IJrNY%484$34VUdT8<Uy&XnY85U|m)3P$Bfgbk{CT}^s1!EBMjV?F9YId5i;Cbm&q1C#mA#ykPQN%RdGNjR8o`18IMbErQinlprxqtbh%eWmW8Dhx#lNJL0T3yYHaDhd=4LC7R!eRdyp+(<>57Ap^EvL5@_Un9pt6vsduENHY0D#OA-XO_}hR!R>>VF-E?!B|1g=TOhU3X4XkgVQybd)A_p0?4&W=1W?|+Pr;smCC2${zp5eUSEO$YpM1>DP3^7%5z@oGOaF{36ZOO=nJQ_lwN}K1UJ%!n&%<V(fT?DT5_HxE9Mk|%$2P84jyyD_EXwPF0fPuEpM5n(je;wcHDV^9l>LUq$bCXIA1(pn6s_XvI|I^Ch?O8xn0oos-Fhg@kU*}BzLY<ol$35t)%QOhn)p0xnS0z$%`A;8x_*CsZbJE6I1j*t%9Sw_!_N94bk$J5GL5FNq?GOh&WJIBNO>YBQ?>Hzr(-NaNj)2Uhw^39Ku)Q$c<Z=4NxQVu%U0g5(R_1D)Ao;FwWqpq-sQSJds>qr*~nVbWqoji44S$ph7ghvXDH_FiOv6mg)<CAB`syC=P2cYb6--?Sk?UNN&$5@h*3(SqgiUnqt`2rNmO|kJWK+0bdHdTUXyH=jm`lZjk(ta70RY)><{h2#F~m$Bta=u-%wu5>tXS`~Jbs2+|ez<Z427qcFg+gzHhLx+|3vs?)+&?X>_Y`758GT|vi3InGu-ZpD&Kgh@J}BJm;ECnpX$8j#nJA8w?oP!lqv=$m2%iwPy2Rf;ib_+yS&TuzP)JmtxiPCXx$zAnV;;^K}|15xWFTZdBOgj?XEDDPD;fi)-gyd&(SBuGhh8x@IqPs4p3<0y1fJz+(cd;kOtO0(a#V%fs1JfT&FF4P>;E*dPUs7h`{hB0|SInC2AHH7q+3?(RC?Yb{JEDxMQOA>PAb!J|j*`C+&;gv=VVdG?zOfTKmiua2Syo6k<E1b#5U`PC&rVKJ(M2g!0e8TuBw3R!ibvLp3i?-O|n;s!k3#6@BRr`iqUbWsfpG6NlscpM6u~SvghUNV2EN!qp*^7i$#;1sh{>)qzUu+JZ2cvOAY_B|`M1|Pgo9QYRzf}d{Nnx#=2AbheyMkoCK|RoqlXajiYaBAPkSW@Ph++blZ3l+*(sg}nG>}>fXbf*u02U_P<ky~KxvK?*^yF9ZfrCs(dP$r7XjVKZFPnDYF}UZwgd&)-8rc;9fE4FcWHpQ!v4F6W)H>mkggejrJDf;|57F*577E!LV}d4vu~flear7J{FO@rBnkX!@<Liy=Lv#Y^%deNfw?zZ`c9_Q(<bCB#J1(BKiZR)d$rCc25=<z=Y!3B7Lht&j0|jiOBA1Xn$CFf{o;(;`Q<`oGGcUrgd1V-h21%@Xwo8-Wgc=NqiV0mNZa2cYQ?xIk2`fQ@4cY<-y218}uSOSKZEd(D08rx<!_#ksZscW#pVvwwav)HHShzJU$aWg&0J8QbvoZVcJVZI3$z!L+uNbxe>80#Ba=Fu310MT2`KLkwf!uv0>AgE63AHH<X(T_X=!e^cSkwxttMk3@(i#~Z9_PGS^(2YbPQzW0^LvFz55*)*Af=5-kL3mw89KyEc9$adQO5oJ^6b0YD1U0d<)6PKv506PYrgaYjKj;EUCd$6tgqZ_p3;*q9mOmmr$BS=)#AOZ=H+Cug*j{C!c{3dS1}H@IBR1O_JEOD9eZ)_v}4COEFHS?MArZ=JL%w)I_2nT<%UB<XPq8A<?370gQsrIttzJmyK8B*F1ioXq*;^&#v$l4&a7j66ZL%Jwo@SNXQQWZEzN!?lAh_HO)B(tqvmz{ScqM~j^;n?Q-&eK#5%C})>RhYGOtL*D{Ep%v9JcwJ_ki2#Sx-7<I>Gg5<sckQc9~<F6#t9u{d*}4M*tPG@uX<3$vyc>XFWR3oBrPa3V{~ki?bEBu%bw72F;J$&ceHbiN$mQ1>$wf<1Ju2`S)Iz)8aXn=MWAa0toF0Eu&Um*Fw;((Y%rm@oP?;-T_n6G&t<b>t6Aa9JR)2nh|*2Hf|~3@{iq4;PkOk7CI6?g28)*s8SBqF&%oNtw<{g3eBoax=WirY#0tMYP9AWlP69<U)->4`Wl9PZmP#k*XZDDCpgMf?dX@%SO-vbaS-PsBATK`qB_uVr3s-fwO{u3J;D6b-Ez}m-h$qAYo}VowioiCm`;4R0$J(7p;C?`d2%LL}g!=lgcn3az4Rs%b{QnyI!;d<6bdRRtJRrUg~hakc=W3K$Jc#wm*ecWQ3K*X&@u9cG@DgJCB#!w`CDw<u$<gNkiQ!1$~8`U#XqX(A05LjcPXY8&O9|g}>2~eHIL{YO06xJ>aR1JfN7edMXlS2F(i6z`Bm!n(!&}bN*>pt-HXOB(G5g(FhT5rvipM1xHQ?)q*~qfDYptf=m`f#Sm~@?3e2OTJ-Ff#aDm~G*)oiQsfgwwg`FBm9>KHo?WKZ9zdaa=C7x8pd1wtE5tapGEw3X1_F;+t0E(>12SY(!K~_;)i_BmezcT5a+V|(nfGofnw09=S{DaqvJub`8p6m2pM8-hvGn1Fk!l;|+_s$p@~>ihe2GAk3x8?hTLWB&MI*kpb;Q67FX2P4KcmKq<|kY<RwBnmx||g9+|@+-OiiGv9#<gcYPfq#&$~=~Dt2!e7R-v+$KtRlGLiSUaK*$?O=Nlrm=PD3Am*p9DV&$`VMFR^1v3y2##gKj!%Z{ltI~pGTT<~%&6|X(KV+~dVrsxu_;_s&ol49^A$OJO0p?lT4%-%IH|D3TnvP8#1CO_Q3im0{tAapZ=wz={(yYY=JWVFCS;iDXF@b}xpf)<_lNL%KO0vfe_$9V+12$m+M;lU%9ULaF+sNzRMqI#V4kC@0Q-)osVk^lPp@qu3l+2J^VTfb`S+SfMC8Sw2Nwgs(2>mQX1prpls)dD3<gJnJ#VVKX$}~WjR?wE&BG{3FH2XM1X;w;wD$kQ$@ceMEP?%F44%aQ9*;H;a&GwUAjgI6*IdwkeHM6X^^SYiiDNG#a$<cb;mI5KuiOY4NBOzAsRbH&DCo9=i4M2O>-T(9w9#yj!_B4=UQ%XPU#a$&J(#C?I;2PPhW0yovrDBe5Kh_Y_3n+eUxt1xF&kLDR<?6KlZXpkta1NbuL}#v}L%D3C_b`Sst(FT@=hdLcewT^`MLCEG>3+sdtpzSo+lG9Y9;$%iQmSW=s0p@&KdDsMWV!ktTiWIDotxiZH1Nfc+XJmpm|6?y9U^m3OX|G3KwZ1KI;O7<H_h4ES*vP`o{%kx>J=Fsj~zkbhUw2q*XNMN#xK_T?Q6B>yp9aP*%;qFFUyf1&)ot+Y0F^VA_18mgEbfOL<12hvJeV08tN+5C$Ow?rW{fD0{Bu!xuPy!13`(pY(IW}fAjX&H@ExSm=p_{nG}VqKOb9_QlVi<x^z@D3pq0y(leHtdB#i`Xf(&Joshg!0bC;^Fk2KM9cj3cl3&+oNsjUgyJ$U=R1)pqG|>^v5;!C|5{`XoPn^~88V+DG#RZlvLT=K*bivwUM=0)P!%D+uJpvmJZ=D=Cz)KL0Dk)^{=I!r9zY$)PzN{l5DhLH#cU>ey>2P0NZUPD@vWqEsfn|P0@gT4Cja9lQ=$qjUpxCvr{=6Ewf<kb5R#!Vm*i2$k@x?O1GV+WustwoLL%L`Q6Q1Rj=IBSBvxt<2s{Mps4VjS?EKPtO_}J4d(4w3vDxWiJg44TQDQWR!ixwhB$GFo|r!hbR@A-@r=`v$ZxTa~TcQp4;JMHj(xPf8+1;y<&4O8qoVhq`NCxNo+QBE7K#(+K@|9w1c#eF}4EHA+jTwQHSnzDzcji7oUE{{G9e-S*=+5I^<8IH_ot+td7*>eRqF9}5MWNCn{Ylo|nbb~Lk0>gS4M+s0j4W{0cDYUYPdQ9|!Ds<^ef0-ApE#QSc-NdwV%&=XYEmq<E(qJxODe>%($+c30h7{I!jZXy)2&t(YYm5A#UG6Aa<S;Fw&sal-uDU>8VYHXZLS^ycU{Z;Jmwd5#p-M|ZU5lwEtfF9(s4^`s)G`Fn@UrZ2YP7-!Or<v~B`V+ovLt$fjwX<2M|i9&yhj=eY>0KiH{;7ZFJP<0ZCe-=W;JyZ;USxMSi-Pad|8SDml7Gvnam{D=VZp`7I|#n$T`HZiHzw!j0!11b&iuLS<mg^J1qP2O6D3FEGFoI+_5~s=6Kmt5A*)^=j;1h^e4x)pD!oD)9uae2ja9T43s@^ntH`WP=s+14x`KUkzv%cbt-1R5$9q)xc{P)K}vZ2F%y-U;CV9WDpG8Ud3^KGz8pdlW1c!P^e;R;&=W(_@(_ow&czg^{9{&f!oc%0uxJjspz))!_zMA`C!ZMXF3;DuKmJ-~EUnJ0oJTF6Osd(~rGEH-56@Kp')).decode('utf-8'))
_ACTIONS_REPLAY_2 = json.loads(zlib.decompress(base64.b85decode('c-rk<U2j}ha{McXp8YVK8IH)j(bB9fENvPTwS$d87zTEO0Kw+L$y<>B9#PcH{i^P&>T`xt7Jkx*9Nv4rPj_{7^)LVP>fe6*{U3k-{nfvG^UJHBZ{ELu_4w^Kum1hF|NPs3J^kqEKmYjc_y73&e?R^2msj6?`0KAf-`~Cc@aEyw$6p<O*xx*TxY&IB;xDh>?{9CxkK;dj{NHcCnY7@iyZeV9@+NpMx%~9YAKu;XUs<1?9(VK8yB}{pz3a{0;p0DR@SFEP?Ds!^`rV>0@9#d$`|@#!-@W<sho6tn{Pe)%sE>L-`8fNN>3A&OI(+-NX|wl_pG)5R-G_I#Z-4#xt%na!qawfedFW^FojpwI_wCJ_eb8+(-}5zcDXp~mE5k+}_U|8_KfSqG4o!R8j?Z@{ZfMhD1vEDAxai;S_ivwm^W*;Z?kBwD7qd)z@NvX{dKjJ>|7^az&eW-kWv5Py0&XbS*i-ioHxK*!<;PER)qB<a>8UHT){R~|YSd||sJs1~!~492X3ZWJbGlMS-<wU+%dL5|S>;86zW6+kFS@>GZ7^2Q=-2UCcx=S!$_Ar&e9rjYryCTmgVQ}TX-~MdltzH5L`xA(;G#8I8;-NFac6@pEHo|iKj}F^aB+|cdj6AQE0z}OnP+INwIQDuY3nol3iTWgKeP^BWYqID@VPlk8{APJy+s{$Xh!rH^~GxougIS}|I}ic&u1g{iZlxv+7@u;wTpDw_TYzTOG_rwsGY}Oi%&zA%kYTfZ`Ft0-QMosJpB5n{r$tc+jsxEJZy&t;_td18}v`3N1yDg`7eT9eY8kMUw=AU5>Fl6h5MW3iWu1h3-3ooD-s(&9)30gaWmjps7KssufKiwJw40C&Zh5K4sg=}HhSEd8xD_!9$gsDwC4qRt`3ZjpAI)iw3C~+O8(a2)a!ct^_a(V-OOlJ{LwVco-u8gZ@<|};4rv$6y#Sj7#MD;EmdSZ5Qv6cwTbb}jSKQ>$%Mg>DtWN9rt)c+d;i@g0fTo^i=7canmPW6LzB5n`{jk7Loa<sypR3NnlFtD4(h-ToSyu{&HZ0mV5xjAhSgJdbLCk%b)_9ta3*XF1ggk_<W2P1EXXyO-&C1FnJyA|rES9?<;4Q}&1|`OG?E^$<t4^02M9Auqfed;!%m+Ulsd2Z=%A)chF8ArULI1ijj>G;OOk9a5(QO17B0HX`V!0xz)^6+UZwXIj@aIB#F!wu6yr}#69$he+m=9cgE}!9sp-wwa^3S;TVg6o%md%n^QF3Zv?mpGJu(}L;6J*$C$ZnCw@XTib7zr=`siaiBTcu!(pOpxIlRoyVu#@#%d5?`rs+D@u5tY>0l3^?1a8dNQkDob2RDg1*vs(7UTS%01b=3MB}SG?i2Im(ZFqIrMk2=O=nWYWP<oX!kEa=cG5P$(Wpf4^u;NSWHf=)TD_XgiU94PniINy)Z_JTdfG=ffHrSWLIU(ax5^9QOA`3q@*_ZQh@p&+?%(QPp9pQr)&{V<Rg78+=v@G3*!^|M7i<_0_G5nFy6^8uk#uzqDSd7?-C+7a#F#Rl$+;k>E3@2S$uyY3V=B&Hvv||<mTZ8KLgEn`xt{^|NIm(~I-SC|voTm~M$b+5E)Z##H&vIxRJ-2z5@>jmSzx%mneL*kkvKh>zIC>WbN?T*3-RPO0>U-d9E)3zdLdqDu{!uWl*CBy!o@LV(0*B|?>A6u~qm!>Qw%j9bJv;*qVJ|a2<~QmWb3PRq@akm$4o4vxq=tA?0kzO5_M_n-i!nZJ#wN-8hx?nucl-PMzv6v@JuLp_E}exK6OTE&#8HHlkH*FDgit4jyDtkyRBr^GfH3l$sDm_F6}C<0^wW8(OiMtkr6+opW)h57PLrLM$5Glq?s%P>XY6rxccF>|V0M|G8}_mb4Y+|JBILFEIqI^(r)Dh%Mi4Psl5~vNWLvgqv|fTRpOOo*Z1Zr@Ysn;qEj+v;!33cp8(r&_%|6+1i4ExSOQiz<SwC=4(64#_M+W}g-P6B2(StcfJ&u1CHfNm28W=kZJccwf^(_Z2iH}FtTSaqX^pJ`-H=3fTf859$9ufw!>WM&YKI$pl14EY3EXvthWa?CV4cgN{4FfhC0V+sI1A->&GhMeMY$pUGQ>vqp2zp^%YC(?ZEFPG#f2ThLLv4zpfCj;HQDk40Wl=T@Xqx$fsOj+fT4XJWCK-}BkXiwEH4C39G6h;vV$dP7z4`Hrm%#kQHQcEv7_okIopEMXdqgyE3!zgVj4ufe#*Hm!NI|TEoh>|@C!ElYMeOE_G@MjIr^|Qw*s?A-$V_E|`1~dnZwVY<Kbmt74<k(NVq1A;KCao3?JS2(JVBX%7KQ%;^B-;V%we~wKkKu(>@D%w*eCw>o7b^?+|+>ON6`?+$&*cH3wQNc4}<`F9(l6FmedG0);)}a@%hje!XPL<F+R}t%!+W_Y7OO$Z2XZN1+cw@KO<f=GxpJ(3c->F?-v>28EBFFx2=bO(Xhy=l;f%tO(c=4VO64=GrKO)m<k+cGGL>?@4`JCxwjcbH^0N_gu;7{?ryl##I%1e^a5cE&Xhm3Djh}1=4Pe<ZUK|Y6pWIRQ>6|e*{a7I1Sj<-0w->eW$i1xQ8#CK_|GwyQuY{e;BX5^JKPJ2U$olQxIIaZzkrvt?Bra$O$vp>9(AEjn8-qwgJL6#?ra9b0DmfzgSF5Oj_Q+X=^-aX08;ovYE`%x1{9Rmy;N{hCMsvnT-Cf)bxGOo!+9dgeOy*}G&8;P8SjvWdOMNCrf>qebm8xZt(T$wZ6qcdJ(zR@4mujqLZb#-4>x2Kfj=4sKfb&D^C=*!u*=dMp3hIaSZ5K}U4Uc^3jT$dBnpP37&nYm0IB}Ofg3#nD@4oDJ<7r5?gtNNpaAixn~U?H9+1I?1=^M*KZfA70!^S|0+H}K++1^NpB=;AG^ZpYm!3q~mqPk964TBXgcJ`rln57*@CZNNTFVErNVuq9@H~p;=GCU>KxT9!=>;uX4+tZ%P4R&kBd`<jI%*)IQYu5ZK#uEUh_=>*2$Hd=!vWN}{st~=CBecOOcJIrUfFy1pxmu!5k&mq;TzBM)Sqqx-5;GR9VXogt4Xt<87G=-WbOCe1P@_maV`?6$u+DWn~3O9z&E?gNgK`fC?!84`_yfT%x}jZF&nCve921&s9V_OFpwzG#M5LvGQB{aZq7Q7-M<ng6>V;@ZEM1!2Vr_$;JlOF@1z4llX~R&hfyl-(6;IJ2l5Tv$K~}F>P~DcoCbZ<z3!7El(=BGs!f9sK;#V!X61atznF6y>YTCIy2YV4U>y7Gfv~|mA7V>&x#OihBmG>7%q60t=-```^-6dOFl&f2Svpkt+t912i7=MOY52*J#eRDh6k{alL|aG?1xk308`#&)WVd78)-=D+YJ!W+U@bGHu?P_Im!zZuIAYOlMC=+j$Dq2rbW*l*UZJ5=((p{opioATvFZf~-zE14iKh<RB$qYTQVh~)w-M_nKq1RrG?PRGs9;!kgHe*(ev(O~=YS?W0kZz(qK0j<7Zg=+F{`g78~uF5_xuytn$(2h72&_XyL-QvqQ)DyYXyyaiZ)!9s|p1=!>|<bi+2<rdnQOssJKpZa!fK|avmqBSxhk!Q6TAC^sW=q<5T&8W<3KT1Qvfkx^19nlhWQi!9I-K?Q_Qa!j9Fjg}NjXqu?7UZ3LTDRe36{jI#d_5Jk(I9_v2ua1u_)K$`qnv|qRMvbanj&hb0KJYCcaHh{sO(Wl{hFh+{csmS&=zgI%D;ZpaWP*>nlzz0UZi-@1i#^qvdvz;)`5OjnkaS-8_#qc%lj!XGA(<zzHR+`jTC;0{u8c$u+24O~BR9P!hyevM3pA+Zb+${y_1V;!F7e5cMXs}#5C>zy-ns<h;_cY%E(su>qfe1)tyFgH8Agh4WtkTSE3?`w4E~&RP?dnuC;~=GXi!+v-WvV*ym~jj*n$bBt^kTkZStVJBi}79&kM48ZuUiwH(Be4te{}K^9!HSI5A&b%!uQVu+cEhE`fezu9cmFEk$wQf#skR9b+x9e?KA#sP+=uKJ!oe7{8PsngQuOK&n@6>kQi`N6oDe|@;|w0?GjE1E+4^UjX}Om0Wx%xL@~CTM!uS{Ppaj2L<<#?kuB6k(>Y*l5&VqQ(JASCmI?Bjk&MV2lM@)45SozaCeKDwGFMY}SAjUnl0S3q&FD@R&g;2`-`SMr9M$$%yisH?z(avnG-%~>k0im-!H-1sCq5=!X|xBkt(1D=e)5W=Cd|YbVx3%)$zv%EdP|hloV9TBoNy<xFbZVD)-)>U5@SpykOMMKOP7k!A-4)fX@q2;5R~7Gf@w<Kfwo&zG^Zib;N_eVNg|BK!I6@9JOmq|<$2Mut7NJy?vQ4Z*}A0Q7|FxZorZ2c?BRw7G~c1k`lFOzY3;&1AlsTAM>36~5S2_Jl8>1)>D=(eh{7LD2Pmm#o?<M9@JP4Sm`g3FQXrMmNlHLID=|%rJIcAF&8jX3rMzZ%fh3jQl_kY@kV|J)E5u7*$R?|xYindhBmaxlyvRDH-V|L#fyhE)g}dytN2}P_EFC26`r4@@WnO)S9KzRC$MjMmWr-X+{B4#p?nggKffrU~z^<kXj|*f$M`SA|`(zIh;tKH;2N*H6zD#byIA}P^x-xw%BXNrf4U!EXW^*y^8mI>YRxA3gNtF-w26X3W-Yp`o9r{*ba~7pw@<WSYZa3A2P*{rO+=*(~IetoBd}ARX#?D6;#T5w>Z{L0IjIexON*B4|3k#AYnHjrpJ5-&r^z_u~Z;<m2z|=0{SR}fW1%D3GfYC8Us($*4l4!)7B^&dpD_OE<Tdi>1R7p^wtW3|&@DKq<nKZxmJPExpqgoVpVd6^-y2H>`AXw<>*N|i0kZj_tSQ5W%^76#uH$tMEwZT$e3n3OCtpKUvFkTAF$a;*S{`{XZJ?K1+Ja)Ht-CcW4JPWZmvMm|Hg%RaLDu**$f~)qTka8j;4xT05+EzIzLTWS>Fk<ti!50;4o8>g{jIEfM(PsUVOfSs)rMHB{M$8q9AqyOilcNCaRQQd#UU<7IH<MLZg#|*$((G0q1iK%|{T|pwXuX!Jt;RFKL_Bh46A7B-yqSWKYET`HztIWA5-Bk4W~&jaN!5dz)R(-BIk$%HC>G;FbJpak=)@6Lc*9x1ZO4UP7sMD@o!-+XU`$hWSU$a(PmXpMiDz1|xA|Gtx8#IZ?==2Tey$aeDH2}AMXN-3Rl?OeA}f5p_m!ogfy0DPN^}Bf{EUv9;Q5m+RQ#AhI-NI>DiFg$lx9sJy@*tgXul8gtbN1!W#anMCV`hjrbw_BLVM9)1)>#!oBujP0LDo|QR>fHPL&N7IvE_M43=weB~aTeCbyC70HJ2lflww91;ckM^U4MXe6=FfkbrhtV#dZU;FlWuaJd8TOmeOSQ=jm^kQ5w5W%Crv1z%y;RKRp3I4tJ)pBNa>Nik9}NxwFY3Qr_u4+2s_JW0dhoI)lj=8DT~qcr)Z)L~-Ws60V0foHzD&$HY3I@C95N0@+^;3RTPWx#T5q!J;-b12whIkN-;-(_fv6)rne2qe0Atyq<v8UUx!l(!We#)2TYg<g@czv(o#@pKf+km!{{RGGw<q?K9`FiutjS-J4*1&5b`+B_@MAop42!rBs7NLY!n_l>$&?x8P$Uc<ta)F8!!bhKdN+U(iUjdSU2R7<i0&Xy@q`a^24hEDL*KephAt;9~)fB*f-F#oC&4swcdOjeHFBU!bWf(~00^1Gf+Rp^Vz^1i9`?ObOAC=To4ds&T*X*4_9gPdhfYCfpqBT7xudi7S36VEs)Qls)xtq8zC`cVwfT^`xZ_MpHZKrumtEDQEzy;8WW8(dM3q9hr7TT^!0x>e0g3X(D2c`CxPP;%>Qz+-Avs!=&JfXymrJ?dF98xp?F%6ZvaCKK8Zvr)p8=sTo@IS566tex={VmB)!kEeU6>Zs%^KhHPDg?iz95=?J21pZW5&;j(dSw<wKbmS2~lfRW0LKiL(3m%bp-Kz@xZIx|2q-b<K4-na0mQL9z+ibQ?WwpMt6~>Mb0^|s4tt|o=j#%7m=qR_6;fo-8@nr}pvyMSFF`2P8G8!_y!tJl4N`d{zkGzJk54jf<l8q2Q%#m1XAWxKgt{fxTx}|DN9$JzrCD1IrfUS7y=Qz;%EI3d=RpA<}?b#9P6P7<$g#4qFkN_~brc$^@6>Y|ZC-*hMD5CKh`F1L%Q@He1tqUD66B2{V99b$uPYFCunA~l!M*xH|EqGOWl_pbp;aWZw(IA4xEn@M&3K)Z<=-oMHWfF~f44LyrC3b-|CdGi5j>Iq{5vkNF&EUvt<l!M@eh~b@1UC-`R2C>x&=o+vz1AAcBzO(yj8l>*CZz>KVT*+jD9=qq$49<wi}tfhTh|#zBJ)F)3TpBMXn;T30nT9umuL=#e2%|eY%A7%5I`qq05iS@k7p=&Gj>t7Lbt#lKvQ%5Xexh68W)N3@MJ}jKb#A5?Fvj)*c%gWbGUM1nnV%WMZKvgbQ0M{_8_@iP#7Ps(G?^x?ELJ0g6`lgwbR^koGR>``eFZfk2;km?ZZCJzT+j$uxldMzgjlQF+7OM4NZ1sVHwLrZbR{Km<-<+1Ou9U`Gj4QTLx3Og@lMy12(@1U{P3`!j&M)`*w0ySHf23q_aYL*+E9`CiJ5hg6<rJSb{X6JTySI(o)dkRHkQqa~E4oJ4D~wdfc{4`&v_Fa@UfD$-<y@0xHZV$#F$d@8&XwV?>#5TjGu+%k!8F6zDjwm?)7?5UbxbxaP}of9-?P@E)&{MyyD63(|-{15r&N4muKfnkK0ZI1K^JK_moZs(A*&Ry3)tEHN~K6nc}eYA?!o5yNqtLa}C2mT~DvgC$qgmQ{?pHVw&$JLOeR61_NmF-GSyIciy8hv?HT&a94GMo>778E$flqadN7jx`QF!Rvr73b*1zxZhh8hu{HE01YZ#5}a?0IM7tsEVg#S+dcOB%reO(5qWCsFdZ;lBOL_UZ2mb92-3nZOqs=utl28TIc%B1S*)@Wawzbz&~RJt90&{bHP+rGQHwC81xXgWS~_spKUpRL;-d*6hlnGgRpflzX(QK-6&BGnK<W3ikh37zuaN#BOl2^@(C-D--09Co@upPfc$@+#(8?HX>ubWP(58hr%Pe>nA2(LgnOhz^kNr&<VXK~GvOE`x(IAxSG)!`8Q{|75DQ31+&RdV5pykKLRub_#Rv98r>(-mdbE^WXx222;hn{Agou4JboJU#0R%TOCS{seIXCS06aG4XQD(nKL6KeUEgi}Dw-cnIyO7!y92P-t!OCwuRIUzN4xmz6&*m8~6rc@8cP$BrF=OP_Sdax2kPSRLdj0a*y%27)Bo=u4?Y_AJr9!l7dm{M6foNsVi$H)p}L<!*MP+*E$Np=wl)($R3Vw@;sA*;^0co=Beld+fOfYJ5B(^NN^8lT8>4|A!lTAK@WBtT^yC|(gvfY^GCej5_8w!V0kl+hM(1mU5Dr6mb+Xq25;#r<C+e#82)k0^aa$y<hy5RV{1tbzni2~Aq5+DYVY@HON!f?ZS}&BDo6XfjLb_7i`M1`f%wYb9%=W2~i;tpi?aEZ?3=;tAIX?%fFiX}*S~^p&p(hf_+DsU)WeJE8%z+`%28pa4&U)3_BCzj&f6EL5s#d&w%4ksNaa#DcOx0g_4tm9czrFw3fdeIe@<O@gDh6BtN6%dv1D!-$d-_p(!ZDG>|d*KFY1Iu)-v1^I}Kh@yLyb+kzti%`A<_Zwc#Hj|=7SJ<hWs^m7<d2w+La6{rRNg0m~u)2MjCs^yU)O2&lydefT><K6m&95wrx9L?pP_JknwVBnMl@m#Wydg#Ih8(`qHdE_M0O1v`QN?7K_hOyTe0SH&Ot=w`9Cq@OPU4u*YziLL^7PZay656gyv9s2R}~u3<op2ez`CHMMrz3t-unz(C<IXT5_<45#+a*t8>pG5G<!S9VG|a(fUUMtFv&@h^RCpqSgbbWF||055tDHZ(iW<8>#Ulcn@p(iKoRa9BtrpVMKO_yh`^K5@rIh06(%ULtQ=_P;w7OSRzy5N26jB<k5rnc66tH}=ThciyI4HWIlRgigQDP=RLcp&5mN3|hPZ6oq|rp3{2-q~l0#vFgp8h1E&wa!Uj%fD*c?OT9}~I>-HA{Ol!qoMT|NbEczS!H9{~^hxa3KyYrV-#-YS&R1n(U3G#NStaN|f~?;SlRPSaB~T3L3`p$lO%*CLLWk_6fWwscPD5xs2*f8uE-xkG)RN@gAxvI%K&fO$(OM1T!is=hJ$fz3q7FZ+O<(6d}2QF$R*RqSd^i)y(NHY;1IAzpTQEh5L`O#o4maU=`v#EdsdM@h^dSGi%#;iRe3GDTWYbmJ(7>FAT&+Y^GHgetUBnIVoR)k3(+)V;J72n!eMBt6bQVkI^b{k)dLEsz-&G#?QDk;ww40=h1ubLHnPYxPg9Q$n9VQ2~lZSfv0miIij*T!U7tv&F2G$RevNvKG)7%Us|#r_D%{^ujBR=$*v)xs(9BX`UV|Gr0aTS(Ch49~XHN8BHw$U$5Q15<f4;`_rO%O8SXdUk`Y2Tt_97)Dluk{8sWRfVq4GKfh&d#|m_33UW2b*XURUBXT6N2357LCbgJgwn!PW9@U|oH#0{Q+o-K!$$S@MmH=QR`UZ_8B+M?k%f9t<s6Qr}GlY?&l6$0mrS70A3`OZjL`FypijsOO3KS7R$RuHXarboGNJWwsD;8*S9{X2gBgaA%$3P4$XrK(L!@@zAmMs^nZLKTS38UBqy`G>slv6y^gRw%a(HY`&Vdn03{YF)iVbVg^=9P4)6h{>g1+<OoMJNc`mKF#gJE`;K8b+E7&MLu-fm*prk+x7b$}YjFgFES#%~KQTXnh(3Enm-48bjNX*B3&@0pG!6n%HqlJ1Gd3N~Ps3vxFODDZ!3AFEB26AdwXAI1rDFrw|JT0zmdf!1FY@pgi*JBB|H?WXYx*b@P(cxl##7oqDyA622VD7A*IINrxsa?pS`*S4rYhVv6{uRcZ7PUzio0AzJMcq6B+2<4<!75e3R>WTO3O<Rv=VcldXO`?Q`BLx3h<iX%5;VJbk4%fp7g_3{%;>#DwgG{880qmri)4C!2NeVg8TdB#CqKqfK;Lw*Vo_{t*kJiRDAn^~T(uxT>XRxG;g`n_no5Y2WXSKJ-$a<`f#uSc0Fh811PDy5!R9rhNGq`;4L#hr4R4(H<rSq=$Bq=Z~;RgoORVG6jhBWF5nH)ff{j3CXDf3(wqbh$mblu+F$3=k{fdK8NAO0|S6^p{h`HtqESDIqMMwL?MKM>*p*K5WGjP=uK~fg<tA*e6R4c^{Blke_&@&QKFDqbQzYO^X>#oz;#psrh5x7fSWIz>-g9x}{U$N2Rn2F}%0{<lJi1I?2|dluY54yeJBO73^Zov%UPX6&n?KdQZQ78^b7c`#gg}SG>~#*rb_nd$Eim<5tNf=t5;Nm!L~UCiA;-ip%B?C?|RPWrk?wJ#GYPO4oh4VR?iU8j_G9&p3EJc<p%&A3nZ@sByAM=GSY%cbP4<b^=1K(-qDn=VKlUl3!|N93#t1n=n2KR`FxM<|a0D(H1*>)1zam5i?Tbz9ExWt-j4?(SuHE+ioRxs_MhAjK71W3)Uxhk&w#x6fwb{g;U}OaN&6{8aKrC$^%MNgw4H~u43U^RSX{MS!L^=(nYp0JV5f6432?;zFANStyhZn8}j7g3hh9JUc3HmjoMMm^^7r#3TlFHdk2Qki`D6J(-UHuppHJnPQfnSX{IB+q)m1-D;$)UOpDu2&U*<jFhw=8D*!+y&Z)@i7cpJ|p&zL=!X^23p7VD)rcNKCEp03mZNqG0s7_0h6GzX%>{77<rijAwIzGw3`(T{F?(%CT@NLn6vrQn^7b1A&lsYbwwu#Z#5qB;mIwhD;hS|W<1GAWVJJ)L`^5J;mDO8OI<7kS_tzm{m_%*NCBGDR&)y)nm_eiLzkf@cA1>sAkgmb4TTtW+00{<E`1Q1ArEfZgLF1W<n5J(unidGEIs1dr67ZZ-x%AuNEOLc#USYf}ycg$!+^t{<@EdIL;JEBjHcpP#muO5BiO-#XLdLZOep-e#TJ(4uugOP076k0U$nN*y^Z9*(w1vS+9-go(njNy*c*sQ9Nm`>P3PbMew3NalDNtif_$kcLl$R)WsL_l_zBKAhc{rvds`@5*(=yA(`{*uHDqUEaj(htxKPm}Rt32<h8<^J)UhkWHIV+qLvnj5c{=w+2HXNxUNLkkzKny(DybgmN^Y}Ljg?13V)687STYR8jtR66wJiKqcwi_&Q*b;=Rb%B_ir%sM}f%7wS)r%~O++f<Gcb^+61U35w6$+0WB7^0W<qaIM)cnTE!Y@igbo5c@BdNUogSs}h|e7kNRd##TAhkYt5WboI^Q1jM#i78$b6XS%1)i$b>87($rR4913cC(HI{3$nz(lV6mI;&5twj6M)2>Y5w3F2X4;j;@hipY8kOIm^$AxpK8^pefQOD<Uz+!F(HkJp2t^W|WKx=W$(<DoV!3ICr9BS|QIi=}BE4k1JN)aTmnGMqzRt9@nDe`Cy0%oTy`L{l36v;@}$nu?H*5N*I?@61?&QN-}V^59WmxZXWLdl}o0R#wvs94aY&S;?<CNa}3F*T2dpta;x-uMllKQoqu11i2t%(8Jgg<}-*8d!!x*%?x^BpJD5<>9P@YfYMBMAC;$uK3^I_OHA(*0<bD5rSRaGP>mZRaCv_qff~B>DnV^k7a}0ucvSBaeHX2MUf@?dheQQmmS@V~9dbUwZp)!yj<9aqfpM?oD699uelK<SqFYEt(FP!r9tN*}!%-C(Or>!e$UUr`wuslx<K^~kSp-vgtuKDkP#;U`=%&Geg3U52)GTj59S{}%#_=Q9?d5E~29z|Oza{HX%sD+53o-*-1rc9e@oq~9k@@jW3cXs8B}q(F0W-p{JE-8`LBWjELA78`CrraAgr|*<SO}QG&PkBDLW@6je!nal0wk8PYT1^eo+y$<IFYU_6>Rt7j;!_o>clfQJZ1Uh&VH{lDOgek;FBTcQzhC7gFN9*sFu1>*|I89R^uOuQZpkUQ}w=CK3HVRyX9q4T5D^q8(2$=ppMY!MgI2Ui##=@4-bq~&?slD9Tb#*6K|X~0z@|c(!y5>xFd^3d~NH9js-8vL+?bRZi<%b-&$Q97uj+W!*jP1=_@q>q<Ub1l%V0REIscs@u=82XSgpbOdl)0rYJ<--@+AhD)J}UV*)<JB_oJU>I((u<$2hUdIG=<u!FG_Yr}ARjXJQj$k?7#F;lZ4p_UIBEQ*dA&=fvin`5UE;ZVp(WqN*jF1ACW#hHxxDXS(~lgGg0t)7^D4oIsYuorsX8<h)d(f-bpA8eK(h4@V1^(#=0js&IE4~RVM)GNP2HtuU!`eDA!G;r<M;GG4|<h2-i{o05O*i1sCv2jYVD^+17xgoUpc$YdDk}C}1O&}JQQ=^3Ji6-H-5fd=Y1`AOE0N}JLTwxP=Z=`myYNUrU4-jSxv?Z(vcBG)UKF&s3)JLIm@?;l$ez;fX%PH=LixJSwDK|%E|6VR8M^c@f+MV*6Sy$Y7T@RYnfQfVB82)u(=?XISw_Mjbl2-*^<+a9o(vn?;0JL}A{m&B$hide~o(8IGN;zk}V5<Z~+E@_ORwH|L?2_nNQ_Rur#}H!L0L70j*D|H;d2uwVN1c|>E#&+XexWmt=*)H0CD*GKDi5P5(_*(UO<oOpoC;`2B2pZ~gv>tUqSk_$sBJ?&Ob@9)aV6C=NYsD}p-L+CF<Dx^M~q&XbiEx0nmrXrThJIq0-4$%pnQlVK`njr`ZZJnxSldqhl^&lTD1za=xNrHQeKhe@zfDCsq>#tyADI(N&(iLUx4+?*I&&UAQ`N)GroISRvw?uD6Al}4rVh_km)g4OU+I+5P>8M;V`42CS&Gt&;lDQC)yF+uK_tgoL^l}%_|H@f_Z^+_uYqgw{L%ab9cPBNwJWH^--`A^08IP7aHoM3ra<^kaMV^SjAei<e1e1&Fk0+6jFLB&}?KcW{V;uE<w`foat60FgemI>`wNqS4p&g*F;<}OW=?^N;vkVJ+Z1GI~?j{;tVW@gj}zKm4g+>CV1~v!%D**0D>h>Z=D@Df`lbFs-)n$o8o^ET}*gU`eKiS(je4xJ#-NgrNe!FwF}6i$a|nP2bK>OMUK4EH&*GMpl^oHgreNS`twTU3cA7RSzYZM;XR2p#V^(g?2+e@QE|A|9@0fii1aMmGzUuZW3SpL=+=<YPa)I<|ACJ^&tfbJnxaxUizYa|^Tb5XzCa<MG=-y{JB@J@c&BGnNtZ9Pj<1l`HBGC!qq%?P=A7OSH!JMFVX$QNq%SJtfwao(6qP`5b&?Z@%Q2u&)4z|$vUnKG;LR&A1lQLkR{PMj5v)I$t7)%?zlgXo#*vT%nc>Kc7H~`LkRz>d_mc4BK~@adyN0+bUpF`t8!)U%H8<2vgVa~i`(#=eRLx6Q1<c%NZ2@1{(@ktE#|}HhiDeavFpc{XLK9CUncX!tY)B!9*Qi&}s*sw>!M4Z|I^>?B#Us;#|BPT{$gK-J7simOEL0Xt4kndYeaRP_7pk-r)U}xE$11`$Nj1TXom!m$8eW!>PAysZfVoU(rE&#aK$db((9s0*?1+zb#rH@<feo=OIBa~G=M`*~Xl`9_d*hZ<Cm|lPd50wotHqb4EO3PpB=dYy16cANKexyu21gzv4o+mG_+eD6lBm$nqypE<@ST?ZWhKdt3>FgvLGD-{VRO9fxrh01_v6jO9r}~W7P`Kg`S|<WyPt^Drm$6x$Z6^o7m*UiOgN1$*HRunEpUTI9IP-G%fbDBIvJ$0*B>)cnF*d!gRUaQrdS3zPwmSgq<ne=!rDL4^gvGx$<RY^zB(5ur|pkfi5UZ*pMmvt$OVlbl?7!806qJ}az*6%`trwL%Z#Pvne+1~-)=2)0IQV+1hlcA{rG?LCQJ4')).decode('utf-8'))
_ACTIONS_REPLAY_3 = json.loads(zlib.decompress(base64.b85decode('c-rk<O>Z1mlKd-%&OVUUO^VzbE%n&K(569A)0i~~!@$m9fW_>=ySK&u_Z3BTRdrQlMnt~Xlm_rgEwWklzF%f!WaKaZ`|9t%{r=Ct{r>9TzWL?V&o}Sizk2-kn^*t%?Z5uxzn^~e^q+tJ_WOVS?SG#B_sgsAKK%99pYQM9et7fn>f^8WKkROvKAdkpe({%A?{~Mi;K%VFJ^tUf-yF5zr@Q-yAMz%6FS+>i%OBp|?_OD-o*sAe)4LyUKE3PB-Tvc01NhDRA9lN+KmBgim-lxcmVNm+#P8nx`NPkLXMTF%Vbo{6Kl-@%ljHGNy><HbbJG^@pFfwp_qz}8Zr}d;@mmico<>D}@AJ?v-n)31)bHDyH@l$QWWJYc<U(3$%U6bt-0$8$Jb!v~vmToEwjG}DOx)C_)e2~A-eJ+d-|gN${pQEr?cGm!$**Ra_Tb})|MW0DHU8Ohd7Y?J=j%?5ivn&a*x0dq`<sW|{rcmlx$3=Y{`Az9MeAlSoi%D)D(Y@O<?udlp+&Q&#hk8`+4mNc^m1z+ZB}_vpf5hp<BP8EMH`G2H2ZaY79JWgUfEz256_vud%Qv6IvDSnqxOVbOKAj{O0*Qw1g=_>wc#)u8+SIy!a~!s{F9y&1Q!RHpyxj+wqk9eo_K}^tqu9SNL!!TSE%Q3_@Q<1BBP$KfzQoR+Tf1*>@Di3Lo=essIOjIct!r)<);?Qd^sDjSEO0c(6)dxuU(|;wg*2%TUs)aX6-!uT6`L^T&71Heycw0?)G-~=Hb^r?d~7m-M;(x^<g_b5P#S8*r0zJJ$kgSmcIyg^}!;Uef{ZZNj!CM7w&G>D`I97th^r;tw?PAc=*`}#La+Xp&oJLUI!j@a;l5nPT#m5>ZYS?_P7%_93Buox-gw?&r9=E9he<N9qy25Pd9Ix{H-_XGA-YOJ?8OLcQjfRe>6?AY)mWW+i$iKObjj{1p}5$2Zms3OBI<B1gs&KZem7rGlRTZGG;KiN**k&seBriI6${az%ZWFVrRq;29H1D(0K0BetF^NAWWYT?_)``=1b#(!#l78<CA~5x&KQGK$XwMw0i0euRJSbSK8qPXTs)?po%d_enp?nf}DiqO_dpx=^}ww+BOVVp07aQ%$8fmCFucMUSjNWfPk|!`sB$l0QGr6sq>nT4r;n&c;(yf<-sM}7~2$4CCT<8@lf?+;iAi|FTu<JYy~#}R(fyYi0%DGj1HnpG5*vvVeqK3Z3#3ts1vi1I=&fOu6sUfYfMFne&E}Bxl}ig_N0QYM`lAY41ligqbP9H+cmkwxwA-YefBY(k)~T<?JKQ@9A0K8vBPkW<<;g|({!C{*SP+c0A_A50ypMsDPIJdgPX)0>}7akFSR^0f<Lpu5+h3`#C^=YHodxRBN1bC_J)iSD80&=$8iQ=bUuG^*_?p}toYKpO`DMUidODL7b{m?q9j_`8*^k9;7eJW4ff@9PRO{Fgqot6$O4f~_T@5gd>RZaGwqvDNBH0sG*z&-AiPyIElaoIG&9KR;%4P(41Z*Fg(1JXF@{YO79)1ziMc;FO+O1HH=Rik!%3GG?3@9;IqU9t+A$x2twHtrL7O{TSCFaM9Ocj9Zum|S&QpmB<iSp7YH=X9XF0Tup4&W2`77Vv-~C*(zMvO%(F|r%9K8zzrL8g2ZuHDg^*wMlSBCJQkTPbke-w=CA*9kR^KIHf;P6}<pBwcxI{7+d%RS=O(=*Tz_A=vRrlWo_=Tm_JuTJ*wbQGdNYKS)#Pz#N0KN}9R7~|7sZj!uzxWCzdx4XapE8ZvA!{Tr5(piWx@tCtqAw@{}Y+MXa2z6q*`?6p}^+wPM2s6)#I!H&W!nVnremZZJX$fex^hD3noPznvX|mJuI7%DH9j|lqj6JOGE>w{K%r5hD!(Miw0XHy2gba5-TU|Ez)cnQ32qGp+l9&;jZ0i=y)=LoPQ?f$VZJsWAEv=-mg{M~}m>@J{qiemg*^f3{Vgq{oQt1Fd)(;#M^lRS#nSp<I_w?_j=)sIpkHepZ&6#Jk2FA_`k0FgrealHz;^UF^R#BgrJ*48z&88^oA2;%*hlGKwdP-26k2;2XV8{}hMLAoGOr2`4L3<ix^}uE$Km}=PK+t43(RDk+c0w>Rr8*iZq37167G#Sq;(;0a_xOiks7-kk&>(m&itMYhK+0wXO*20bH631GtE?r_BtwD+QY+xDX5lkMus};s3_3)%H$Q&y5?G$NhC3AnBZf!U8E0m-M?~|s5IXhaq{z$%!Hq3vNI|TEoh>|@C!ElYMeOE_G@MjIr^|Qw+_Ek>$V_j7`1~dnZw(w@Kbmt74<k(NVq1A(J`U{2c9ugXqoB+`i^6|_`H!}F=CIq;pW$RKdrLev_KCm!=5;J2cWl7&qiBlb<jE$Bg?si`4}<`F9(l6FmedG0);)}a@%hje!XPL<F+b3D%!+W_Y7OO$Z2Xxp1+cw@KO<f=GxpJ(3c->F?-v>28EBFFx2=bO(Xhy=l;f%tO(c=4X;q?|GrKO)m<k+cGGMd7@5()#xwjcbH^0N_gu;7{?ryl##I%1e^a5cE&XgZpm5!ohb2C!_w}1&|3PwrEsZxiKY}LaJf|Gg^ffF~#GWc3=)XiBR{!7fIls!fqINZY74);Rh=dE@%ZcmcqFW@CDJ2{telS1LJM_p(WCbE#_pxDTwJDb5Uz@N(GU@f$Rqxxi8ddLY8fE50aS`{va0i~sNFBROBiQbtrS2b@{T~fCDaGHp6AD0y#%}n`x!8@d(-cBU3V>p3ay72eY*2~cTHWCw!9vpQ84mujqLZc>I4>x2Mfj<}qKfb&D^B9m-*kx%B&*!I|4_U<ZGC(pWE&oDH5(UFij2lKOfM|c>z|9_kwW8(d9_8S2_k)KsP=I*W&DD8O56ED{0&Po@A4Bk3fhJHffk=2AZmuP@&yHblno|;yOHZQgYe{_?iD~BxLW&0*N`#9@c!VEst>pt*BwW-lcpk;V^J>#`ATzp=^wJis2ZWK>ruaaN5!eZMoiz|qDU~5yA;<MGL|f~K2$Hd=!vWN}{st~=CBecOOcJIrUfFy1pxmu!5k&mq=^M}U)Sqqx-5;GR9VXogt4Xt<87G=-WbOCe1P@_maV`?6$u$g*O+@r4;G5m$q>W~Kl;R(eed@ME=C|XIm<`oSzT_nX)Gh3C7)X?8;%PD-nO-1Iw`85i?q7+LiZ-{{wt=wdL6}|_IPYZlJL!PXq@H>HVU&tHv~3FhfqVn^ae3v1x)a+9r$OIzr~BjxB`(;lYSSPD5P1WWS-ITsFXr5aI%h1lZgJ=h7{@+)AZ)PAhuBhG?s#c0NIzF1bBU-ZI{0Q~y%L@R%o^fMmJap)HuP$0B8=s68h&zQvEQDh#TW@X(H7D}ff8Qh2KIF`+3i@jHO()yn&4tHSj$XlECPi5B`K)@j#zXX5xd6CF{mytos_MdS7_*zG&~bCC=?WAta<^$cgg)h;;F+n$z_eT6oWL{ZN&NsP{?u@%_I>4Dwx*YWR&E#pJWp0IiLwofUJMHykVQ{1w|EH%<5~&Mn4_#J^w_uCN*JrZTRo+?%waDsPV?_T0!HUq74`2szQOzFf2;^;vI#@o(U2YDz4L<9Ft6#oQDZ&7E_Ew6iE6Oz3YVZ_*8zNS<gTSfyLjCZW}1tq_j6run!}5yPWa9vST%Dp)QHUDELN78^LB(Rh~*KqwGHfMA1U0hYHY_I0+|YARYZ#v|qRMvbabf&iOmSJYCcaHh{sO(Wl{hFh+{cSZ;fp-z%ZnaG`ros4MU&-~*%IMa0i$<8nUOY$uE}1RY^X97MQfHGECG<3hg8bV}y4l_vGoNxngZ#<7dqAS|ehDr-fGm&M2MbK?A)yR|@_;0Ph&;^zSt4VDWBWutmf%g*rip5|LX`mTUH5CN%d7YND>WEF6lRhpTN!6dZMCH0o3U7d<%?4|T>amJFfOjReIGmha!GdqW;UMyEEt0W6?G2ScU(S2_Fb!(y%S{!5lXD2V=aRh1nF#kE~`+Q(KCjUU+4aKxWEdnIc4`A4M0C~Bt)^xR9#(xbetfZ$0%}ig8V8<DQr=6hBE#PgC7;sY*fg<nnKe=h`<w8H;LK4i_82H;1U_>`@6yv>VG^`m9rTTsc1W_R#+2UO^#RJA0!Ouu-os#xvnKZ8%&WO-)bSgu$LK7F=<QZy8HfzfGDv(K8LTJv%ncdUE8NSr@JDK{NqvRe7I*N=2cqq^+2dy0MnM^pk43N<Nk>5#I8tuViE2ZAKpU~nc3^Rd-SUZ<w_gLzK-V!BsXf5nKC*euVi~<3%HMI)5$rxt|B!Z07(xoSK$hU%#8zDg`1nPI9h?-K1pzRhFO>BrhczI|<rU)Z+aHJ$|55Y@l$zF8qD%mTmJEWO-Hk4EyBgt60)6mU_z25ME<~y`mlaz8UtzDQ0X<Jj~NcK?_wvuT@@-cHF?HfU2)G5)ROdY9kp5iWs7)iI)n9DDy@*tIRN=lGED?3dKKFax}%}OtOrQ~LKfh5)6l_kY@kV|n^tHw)T$R?|xb!%iwBmaxl!N@wM-V|Mgg2+N*#k}mZN2}u4EGH!G`r4@@F+{&YUg7JiV|t+wwM5<>{x(Y^_amaD=nJbnU{~0M#|5&WBLWtag0hDQ@rQWY1B{|tUnVzU97vpHVwpack<7)!2g!yHGrX9d4b+GMs}=p$q|XO?1G;lG7Z;J)_I)d}Ig3&-`JqLyw3})}C@e*C?nHI%96u#5$gvU?W9K7_?24p``du#{ozk6dxW$5ENoLXR+Rj&}YCS!``rGEb12FT8_!x;SWx=(BEMatFk)oi!;3OI`XUWEN>q-*s$yO^IH&roIs5;ZLGdx<r0VmA`K25$aOt=<xUzj#igDf#L8we~q{u)xy8*)*c6-z>yO%9(}8%M~avo=^tdm+5zgFzrQ9EMIIgy|8A`qP8T?4bhRNAT&f=Y84T%h$BE5RoI>k|A;!u|K40Ig2HD)?PDG&U3_Zw4__xDjh}0oTmClY`!!kqhf8dln0*B6>~J&tbdXShH1g{mXOGbxu7v5iNkSn1cIFcz%lI$Z&&4Jvg)p|m<U;#-KvLR_XBz26VV8**K#q|cqW*}M^17g@w1#lQ_xuripTLcIx$(I6sFy5HQqHTicnJmlb124+0Y%u!d+<2nmiSqL&EBEI19M#xX{an7$d7QecJSmX(kU#w>Q(x(e5IlO)CtyJj?o4r0~k2#{bFBwE{9lBCWWlRRhvWl(L$T6+Yj)%F@ulVL~k>G6FP|M#oL?{K*z7e#{`9&YMWpk73bDvt*E7W2#5sze`k~8P+co;+HlFyc{yYf<cJ#MSm4&S_E$X>kI*y=L<zyK!cn~8!U7(I7~P!m*z^KwncbuBiR8$NuxbsPa-yk?^fo85BB(KMW`VG?X(<?ja}a_HT2<f2i}?FTnVN=p@Jc$IEc#T8JH{T!evu^)0rNzC;>2%F`$!TWNMOrZ5jojNcJ8Cq=I;ohQm2^PEgDhSK&rk^gO>Ob6RubMx_jTxjf6&eVX0IGmZ33+7TuoCOC;4Q<bnB8>vJH@f-?vSWYs5z;_wiVs*{-6#|K_Z7UXSrv|_{n)0@S!&uM@x6msR_BWlzHlB`R84@{Dh$@rVlC)AQ`o_s>AS)Msz2NXNP@5-c8azL%niwz(TGOmZtckJvjapgmO&}m)(`uCzB*oKpwu<6<?%8>cbM0)XOEL~lmPt_hL$X|x*!Z#2oTY$33!GCHcHe(LTI*j`LPAbKj>*ii&m=1yQzT-G;(*u3Qx!TWvLtXSm%G&A04l|LOkY-TW4g|cULj|plR6QqIEhlnv|jO5<jgaoiqxpQyemRAkmeLadDlmFvymv!3Q(XB!Oen^S+6cGYYkTvrzmp<-`13}HaMw*1T;2PqlrFhtp3*5s>gh*RM&E06`PgOT<ZyKTxLVUw^=zcJIiE3`(ZIkxO#nulraak=nud%5<~2Jg^coa4^=bp^Oc|HBje(}a6SppHyZ+fDl9w!I^Zm0lJY$AFrZ25$}w8u60tB7iR^t=!NjdnkNXs&uICA&yUEfqd;9KtxJ_j>zp@p^ju3+G2nw$)0vV2&++ye`;gW%lAf)kSSSpK-L5eY%u{MSpic^N$Uq_V!`;i}c4Y43{FDT3#A*h(cv(!L7QueuWjAZMUs?mFB87q%f15fxI^BGQp`2<`QuE*M*9-%&A{c}a=KgtOSz>#Yzi<^tx))JFAQ8cfcEEMdXd3P$RQ@Hk3H4Ggx6Y_=2)LANCPkB8~^xSQ*#|wm^E_hjb^(j*U;#!&&Q7Iw?9biY0tLWW2W<3*)kPHd+M*VhyOeWzNOle}8k%((*6?AZfH}U|HGCv3aVUnDC11t*!E9eR!(WCQioNw8ZYDFU5a3(o_iDFe+kQBC92#xYYMs%p;i@9i5s~mTojwI4VREeP`4}r1)qJ7~UfpCfDAjueVE!>kqT%8;Y%p#i{p{aJx+;iCqy#jv#t<vGq6bzH}FcQJyqXkL+aH;2YSzxuo-k2zy!>bchDvF3N>P<!1lc+ti2g%)ndirpUo<S$)(pLf?pby?smzuYZ(~6x#KkWbIqt38N`>;zh^>}qO?61hBwAM{>><*%cLla|Jw8pZV+rT{>J;V2fL)sc4ZF0+Cy0?%#kxIwr7Xhp<YcsnNz<Jls`RdB!>YSiv69J`yb}xkJIU=$IYC`#GfN!Oxro|~v&#>oZY#m)92G`c3w_Vs*n5v{ZNY*5agw{EzMB5r22BHqmMU2PPn@b{n!EsBzi}*?>(H12V3Su#w29JAfoW1rDXm~$YIU-hIx&>B5Sb(S~5XTsaL`{=i2b_igy&y6IvXPP@t`&)DD^m=OAjR1vVA=~Rp2sNLrclqBRB2rM$6(17^<@=ftxZQVqDpziltk}LUyRYYOpaO>#UUECt23+PmJw7=V?vvp<|xQ$sAG-eOz=9Oi^44c5$^XE)ggGm6QF|1mjvfqzDXPFoW<5oc)Q2m97?N~E6%hPW+NyG6MjGuHJfhEqkptc3{z(@!)Ufra1KXiFcmAbgq#O_EHvEKmku<Q<2k6#Y7&g#1t1cHRt?FnEt3Gr(ZrBLB$03^a(eA?BZtO<i)b34{Cis0SrF|9+QAz9WDvg4?*)?F_-C^?QYv*k&-g1P77kx6CWSUF#8ehRvG};La?IRn*?COwm=t!_z$Y_PpBU#sDOST|r#4lx7@1;bTjezM2nt$%Y-}YFuw&IBa$OUxi9D4mV0K&Tm~iN6lG*9WAIy1_Wo%{Y6y>ndSb7FR`XZM(ORB;eU|OM;Z%McU#Oy8ANT#eVZ+)=3bG>x36{QnWQkT2c0b4ECd2Pz<V9XPOPkJuWzN85&VdNxhg~f9qW~3aYl-$`wRAYNx81qoZhQyD`^5J}g(^^JW7$eH}K7|TX)Jn38NMLqyDH7v^khBKGPR*GjL;Zx%GALu$%R#8?#i^;FGPOvNJ0Ip#E7O#vO|MXt0KIh}dqqb9V(>NgZAir0`a)MyqFclfgohiJp(F^SQKI53?*D)|4`+{k1neV9UZTr@axqZM4d!)9s1v3h4z>uUuQ#6&?4nv~7M^w{PA0!kj{G(nU?eB8mBWorHi^=`ZPbFrA2s4{Pa*Pzk_5MNJk4t-?P~(-l-gw~>nQ@5XjCotf@e@E0Nvn(ZLtbiC$KfBbE>I;$s(4KnsWm>gR({e2ut*svHEc^_p1JVAv+aKf}_k6*i1dExp4Qy2(S~+v{M=?krm-LZ{QX?1+zNE2Z`W_qL7t!v`IsYu*C$=9p2V938O`p7;Z}Ct)2&x$2V}Ua6^JHNiC0UvbxEcCt~ZW)^u~nlp}^#><FF`&95w=x9L@TP%nrcwK*?1VIX!vDv=_LLk?eQo2lg~fJ6&dvtokHJF!e?zPsyHD%@a64o-P_C~-JxF$Irmb^GJJy5llYyhKehR}}`*(fI)ogQ1|gMoQ5V%KQRvD8yd%3ViS~#&E3xC8)`$G@m=DmLe>00fB90Z<3P)iVjbN9x+uGYZY~ncgjFXSRICf9jH()E1UN0;a*s&u6fd-!Yf6PeUL~6Y9@(UMMOiMl%qGqz}g}Vz-g8dpYxYQd{`0k02;XDsez<YJyla5te;C6hV8oYJU1~d0<MTXCe?Pr5QUVtl|e4sHf1$YQa{MWkQ7pwb|Is7lnclTxf=l$Beut&Fs+B(g#JV*8_FY?lxm-%Haz7$(UgD(dt4nQmB8L)Hg6S6X~K8*d5R640=RJ`UHFbJ6Q}qoa;_}1Xy1kGDf440s7+u@=VTz!-If3-o}!X_)O#v<=J6<-pe6^Ix5PsP+@Pgu9HS)I?1cQX4;TwQ%N-Ks7m|_1uEw<fmMd#>W=lH6%Pucl<hZ;EA}SJ-WbvJtEhlL!iMi)0uZ%gDG|gJ3R|_g{9L6v`eR6wyn(;@m3a!*;2;@m+6RtAFFKq?F!pAz7k8_e(HI776ujOzH^oWak5t&qAs<hjfVVh;zE2nXO80ga^ia*gvsuU<D5s|Et0Ik&#FRO4TT{UJ+771OEQGmu+rVF?EW=1BZ7e?s|$UVcO9Fsdv+k>*c!<R{-<hA;^zLUsOYSH$3?e>+pZaIdZmdsPKQN-$ch$n}mDomywSA`}j;oWKg=4ulBtd=DlD`=dl&()x2qr(r3oRO#;RK>fR#AAZlB1Oo0)P{22%zQ^|cD9BZ(JqGdL{XCz9Wu^gN;oMDM7`)+J%_qjqUl0dHY#C9+E?lhsv=92QbbgRw3ueO{3ire!&5Ln>i4}jQjvJYN(Guc#{RX~$gvQGCJ?I%8Yq*vuyD{VVvkpugJNX%acV;pZlKo_G>3B9hI%ko$TB+Xn=Z`UwXWZ&N`gyT=GwfH_Lb78;-P@HQN7dz0npMq0JIjxsY=s%$<4I<U?xhg(w<*Couz~koFRBA-LiSQ0UfPRW1ywwS;AvzTk_gM$T;9TcuxH~Olc=U!BUyDyk(Y-gRCsrapwib1&<Aq`W$=Wk?~AnPO3)5NduI@<ahF5ww&!crYUw)DLdY%o0nw6mC85jY^sfv#O1KCU{x2)BQ%+Ahk~TOXcAWzQ?x*>+N1mU!mLD8Xr)Vt671A0KFuvetR}0Gi4>%fYv@Sf;olXiE?eOO2WX-q9Htoy>HRf&4jcN`%TF+^t8)L*0OOR5O72B4q)YkrZF=kFSp;?Im^gDRpqvoBuPn&UQ-;#BndR;Zn<hhT#WKvU-;1^jk#HyK#ogg9cdJ=ydz5TqSka|SQR;csVQ&FR3jA1C)+uM+aEfh^xR9_uO32k#)xsgPBqFPowHq@^Vv>($$v@iJJi7WGsVuZiO{y4$0b(Uwk3y+kskD%V{&M!$roAj6<#^?@wlAplu*%C$^%rLRvqTeNI!B}=J}&!Yz9E+c5)SfXkkle-LTeONR4iVRmWr2aH!8$0EaRkUJLM^qP8A@Px-JCv;^L1>Q&LN2W9v{#nsCcv6qUUS#<J$_UUY<_l;kL>uA?Gs?<v1;W5k7Ss%QM@iVuK*OKFzgPAqoFXjpRbx=?P+<?T}0$^05UhEDPalv6zY0!6fDAFrRGX=L}Mk>$ZuXmdh-JfrLNV72Gff4Dtr$RQ`2WO?a|>#3cPkZW;;)5ZCj`+}^OS~$l@<kA!g_$aj1Jf<Z%v5kxN(fCb|o~cF9HmtOLL$a<~benHE4@!~u786k3*9zUTsWqyiokSQ$Vp3{T#6*2o{)jIo2hW4qxFPOW9$=zEYwq=P9gEwlvhY~5DqH`QKC+GB0+O?2a1PSr<k(bhb9i$~1#;iv+U!7z9$Y83M)Ig7a>hVK1uDrh!fLhWSO#jHta+Ac<AeRV(JVuHJ)1mfR#7OI2p_2n?ny6!1g2s}cK8FF#5oUHVI%B>!V(e%z;4mQ=1jlwm>NGsTiRGC+J*`7IngmvN6!K3QY8Z>cfv9}KHbGW0w?gi{Nf0FTQq=cN7(%fQN40<9alix#E|PO$QDwb638cmWR7?aL3F*H^>rDTJ{n(+C#FKBcrd!AzT5yaFd`n=a<18KJhvrBVv#eLS_@W9SaBf{Es>b*?VSr}S<%0Q7O;d3HYg7ucn4cHz9e063AO>0FzOYpBc7WhbR(})97n$P)ihly3Ph9)`&HCqMkgZrEoNi&-*xFA^fO0U4(;8mM<22ilR24+2>Ik=jl}yT3Bh|KZM7*LX=FyJ2#MQ-SlJ3Htn<C^G9ejP9w)?E<tT~ZPQzW0Q-Xz%4}~;L97g1PIV$Cn79FB8yGs#!GxL6aeD?iaRA1?^<v)K(;uz67*nH^+Xox4+c)o^4v%YfwddX<Ma%8iFGz1L>P;39P>X?hg7ACZX3s=p2-kRLE^RqTKVh{W|oXvpl7c8=NJQ@eBLnMI6BfzyNorY4U95K7xnt)_6a2l1%axG7zx{0@`93|`mreVJ5l1$TV4|!uExP6qXmb$8pjiMe}+@Qipo)5mlwY2)7NS>xOCl{srx)JxfeJoUhg&oa**ryaj2B~%6_zhK#-;jFvLdi{xNEX&0+UKBpq&PwprX1W%CjqI-&8M`S<xr;w4qEzCK++=QZW@n>hlK^|&ebEG^%j=K1kp&A-XX~@o5`MBCM&o-CJLZM*uwMWpozNkq0sMPksd-cI2D?b&<0ma(>xqPsxtuUoZV%(k-QB2nav|cpJpsoo{9n)kfy@?xCDm+Ax21dh&JG%cV^VVD28}$`T8gXUGE+s*vzd;E0gL44waM#t)%blB}F)iVw1R-P5Tb|k7(nOI+%{j$VDK79>(@DpFxD}BgHysX3z`!1Y3_ymyNXpJm+ZlQTc1=38ule#PlAqg0q4;3lF0SRlSqkVvkjc9DS7vcUBiaAU=9jHxqpqt$sWb{y8M72D3C)1_Y7w33gi!8jt!=VLxBDL+D=VQdTyE{T_9=SENP}A0V0`MxuZKtjHKE4c|aYW9?`~M0p-Yx39(`#>(r1@neNLR0{qIJHNp-3_Lt_-c+N~&HDP&aZ=%L97l3!FN^avfTytsye2q`*{i2ZZ9X^ASwT-&7vI|wMrMAEJ#VXR7bG)@YB)F=A?WQ@%y6$j$?2e4=%*9YVI0KqI6yQ8D3301E0-Wh0hem*m&Id%%rsVa+Y<K^^|}bD(pAWU?Uq@)tOroCo_XgfO(@3zdR1(}LM{Nd3^}7JQ%|8rKf7<90dLgJtm>uJ2uz~D%?#gEopP3t78(6+rJIx&+gf%9YH|`V5}L=z4PSkc=f?CQl96H_<&?R-0{(B}jWdXvLu_f`s|4JUMbo~vb;N)TuMkA<M5Ba@sxr`49}n02a&pph2NbC~HQ}auyn$51;Z83-?=s1%*o|j!Fe`f>i_fNbMc&`S74x}=7n(gLAW2-Ug4m?KW^rCAhz+TyMa*zK7-F$D47b;)154|j?MOj2H60Ub1(Cs`ps4|3;p4SAq$)8Mg_KyPBA6$GJ1ktBG?|~WYL+*73_RZInc=4Zx(c#>q369($+Q+n@H7d^W<^wp&jen-0_EsPP+EwADAgW&<yXkYeI2n33*g!$spx<+d09waN;l#NHggkc$ec3oN(Es_atSSM-lZgm<O)N06X=xXj42`gqDk{@nfVz(Mj<Ky0Gw8FEo>t1jNC9*7<FH!2f}oNwu~3SjufQd=jlwVQY}>3p6r6p5BExrId$f6T?CqX<tEwe-ph6ENUoGqMpRxiL&crfRj5fhnmDPBs!>>yhD>-aSCfw9TftX(*|VN(WmjSV?Ok{O^NhsNEKv3|kbP4sOY5~`B_Ptqf}pq?*{gGxL{G6|j&48V5EB<Der&mxDVxuWqfx!<w32TjX_(LsopD5Gt|M$YG?9K7bD7rNg?aXB&|}PJmQ<`bh6xFO#zn0KGf~^7G?^Y+gW^i6Czhzz0bx)or8-$&zsHw$iG3GXRx-|?Z%D(*72=uPA)tJSbV4oH^ZGUF+V%A@fpxlQ&d$zS6<+i_ZAq%H$ntpV2%6O8&q>$Uh{mN~_4Ugaea*QZ8Gv(XeD|U(Z+<*?FnxXq<}DJN=`mPqc~CSEfqDz!HKU;>W9G5V0&6R$)DelW2_rx}V8WuWvzDmK_T7hfw{L%ab9cCoNr{n_O;Nb}^Kn!u6&jYL>r6!}DCbMVl2C(YpD|ko8qKk5C*<!`0N2P0%oasRM}kz$C4a3sp@J&1u$$JiNu??PmrZm8vv3YcnuKFt+7o9ryoLjqOo;(5Bn~>QZ5J#=c7)<yHLNsj*CViDeCy)C5tJ>#Q6+`U-F*JN=s3bl(bs?^L<ON>?7oY>C>`$WtIL1_iVR~)USRoPQ9Q`2rDN3s3i@Wa11NSatUs>?uOKI!p4HXP5jK-pwETQXz>GYPjB3WU_K+@GLXT&ur8)eOAA3lFsM=5H){q%V!O{fjfsZ}S0xfEvqIx{5COEy@mr@x|wrC-AbPPN_cN!xk@Se{|kuEdlgln3Xl1Fp@ywk?_!wn4kZx}IS#aXTnsEr4r5!uNofi~+=_8YGJfIc1neLR-M!(ahqUV$OFzP>D}(vD4=0r-;%oA!G8i--kd90@sO8IH_s0k@PXIS>dhUlN|&%PImp*Em=8>m~<d1BUe~21rmh4f<Y129$|mP&qGM7BF+IwFP``PdBl*9NTOkr;t_1z%;^3s7pL$WO3Kj@FIl@UL#pSt3qlj2jC*-XrFtJ7Gq2c^D`=uq0BBYS{N6mvQSynIG9vo^(9|yUZ~PiP}gEAAgf6EWU}h7Rk>Secv(g|wPfJ~mO7o4A{TH0S!zB(M-v>hBWBhW^CJxfHpI5zu<>P{m&sM4xh=d3voJde`;g5$En!%9zARdSi;>KQPgX@2)(pqbE%GS9k;jMw78(708WrMaUT{AX_1qr5aoJx~(%HyhG3gKFj^$A|$ID)Nm=AY9-aOo)KRK>2eYNoMcei&x5vNVzr5w=I)GIC`C5)LcjxHBd#)VxQr(*RRaW2+_`!6~fqzKp_Gf|ldo;-uDBE_ay2R+C3<q%RnJ@G7r6ZbDXJ<t<FI`j~nug(R^Ui)KKViv*YXJ92AazW!qWkDGNKrcSAtPpv=zWnjmGGl2a==?m&w_D2`z`|w$DQ)g&KmI?Pta2p')).decode('utf-8'))
_ACTIONS_REPLAY_4 = json.loads(zlib.decompress(base64.b85decode('c-rk<%Wh;>a{Lvc*IJPEYSKHZyGCjZB?@fz6vhG}2=EvNjPXMD&hWpx*<{syMP@|gIYspVvr?(6c<*_i%*e>dU;g*azyJ38-~aaen}7M{mp4D(eEj(4@!N0S{Ks$q^>6?E^iNO!^Y`C=|Ifeu&(r_?^5(lwfBp66`@8p_-aWke{MF%y{ms*d%k}3U{_^JI{`MC9bNok-|M%@TlNS7RcmME1-URO@+b>`K@Zo;{#`^U1xSO9o{CM-_UGMG=pZ~K0-+cUGzyJBmcZ<G!y!$lo%jY5f@b1r_em*|)%L9+2KI;AC<LpnS<FR<_@ayNM&E7wLE_v^FpFZ5a|Ml~)9zH#diu~T^p`X2X_Asg6w>R(hLAS|#&)3LST50oFhK)SzKR!HvdUvxNn)bFGpYKfE(5A%-Xl&kb(SO|U-#>lx<No&UC%ohrvrK#NdBlHu7@ivc+kAPQsZ*EBPMsD7+)%Kwr|unY9`^Ukk6-4h_p15RQ&(oK8@+VYsMAtWcl$Yq_jwD=nmsJ$bft`bH=Cr_Tk~kM%8LU1@Od6zb$!p;V633g*YR0+Y{cox2BUa<&iLJ@8x*dC(>*h3Pq?*|Mu4eAOA$@rqBU6?j<d0LXM-#(G%fQ#={Z4gagYgm{*z)WmKN%nXK1ChA)gm%>ofZb^&AdAv<_Zn)blm)(j27??x>I6qK-N=BYKSb;<bfW<j<XdYO&1cvk`kmngtDQ3pn%IMY?Qz@Q-LqOD58&oyV`mry<K_c*OBr^<j6nxBGVwzy4`||M21V!@n*M+u?!ux30$q{nO~tC;MvtMX;-n7Rl)6Pe)7Qse`+4f3sW>Bb#91{itX~V&lid&qg3_1{@3Zh&%0d;6W#+y4daXjmx2KI?6_mJ9ER~0nwui!|C?CG|$z6(LvPV4vF@3^QOt)dXp~G@;%sN9?x}0qgC<GrfHUqX~lf|%|?QW!3CsXz>?{}5KL{UA~S-3HRRGw%xG?AkXK8_3<g)pgQYc<Ps1Ds=r#!$#*<p?jQG*u@kbmQ&t2LtFZ>*Y=`-SeENRw!X<Tr42X^4}<R5PC|Iz|b<#REtp1Q*;&&sJQ?eKy#VPi;8#TX>NqR(bQPQv`A$_&bMk-#f$6NW1<7a(wE%gy7G^nfidF?KmXz*!o7@?;o*dRb8Fyyl~Wnl2e$`L=s~aLG2t)<slFvb{(=RQ*`E=rZd|Ff#yK!3}_w-di|gd%qE*gXmI>KQ&DlJgRJ40?iHT#Au|ZH)G3n&u49ksVLD8d|S_#>iW^1RM7RvY$%2S(A7PO0!O`Fl1rRBi^SGPAJZ9Wx&@ZL(qhQrWp)-j4EI=GZLT#<*SU6$>u(8Q<_05hZN8TBMW8vjPRzkxhBx+7%R?jhGYc#+vQ$Fc$J}eftIIYLF-Avk$S8r*tDJc}%>azf=PxdsGtht)Us|_m6Ea`X%H4Lca@8eDqLsZdM`i)OmZjNXUk>Mlj7v$VDVm8a5ZPp3&I8Bi!N4-pz6o`N4_-i11$zs^TUFDtbQ=ycgRCxYR-VW3M@Cl|@~azT*fe1=Vke%M`*Xwevp{mwnFKMMbZNoP8PJ=v?xxd@`3P(cs@D(N+|jy%OwHyfe-3xUcZzVHN>m^Zb~;mw1GzoRp>6cs=2^;L`TqXy=bH5ey{K(7m`QQ;E)0~m#z?!-Ge6b$z}Z|F!YhT8F?#)@U|g?4D&0KarY!^x&$ZKYqrOHbUuSH&N8EaN1{%U%W_-+a)Gy|IDlp*H$^IRVLNrJX@umW5p^@!J!$B5feA<jnl8+DfH;3=`_xFFr`viMf{LNiD3o#}hb9O1D2q_<pi{S~OP7HTn7L2Ig2s!~_<T+6XX|gJ8o6PB_^H!ObfL2RS^eoLO7_XcrJ1vi+w1M35IycYQ<Ld506$!xXGCw!$WfvN714Bf}aQCy-WrI)6Ukr>OVzMNO8L`Q>Y|&`F1YtfUD`eT`;iA{lN(x(ectwH<LPIvX)+?KRvf&aN(Bqd%2LQ5u;Gm$ddH+WS{@vZve|Mq>bBcN#|150IIHNT%b{2RHX=LhK4yqELkF58K`o!oV6>n}dMN$8_kvBXf3}n?)g4%r4Q@96)ETLJHv$e?7srDMQr$JT^Y&HT^kfsI%O;%^RZb#To2u7w<M<XTl(z?`wY|&XfFk}Bt{}BweDUSjg1kXj0eN`4nSudbz<_Dst!|Q92wIrHkNbo>v1>Dsve5ME%Xz7VThsgHk$1h$2^Ap!_r=noQ>d|$^nOW@-(Y!5$PW?D3GV?)jW6K#*5UXHk3(w{WCv<HQyZIswCza6Y@?Ac*tP2h@)0-eZze&Yg0>{^n=G?=>2vfV*R-T!UD|Tc%%OR6dQ0AXS;s1d7kG6T{u-nw1)!AJ3mUwLJ6My^7+gM0$YQXZNXo%zF$tJUfd+}HggaCUUd9uWo)Cf1$J&c3#`Op@^ASgaDKG62eig4U&4dsn&{E;vPu)TyoBVIH!_R*XQ!IB2=7a8FhXp#H3t%rcou*j*D<Ej)*B$2CORic|SyDrg~3LIxLV57kA!aW?hw;4q@zr*Q-!h4SHZn)FLw0|%30$~fzls~m99Yx9JW~Kmc0Tav=jFOU5r4Aw4s>d4yC-o)*CvK2s<!ilBH)nbH&oP%$_84*Ca0^E}+zW|cw%XOWJxPwgfS0uF<Xpy03WdWSb)ij|$U>HbVk3+0YzD&s|5YXjYoQ$+)hE-^Lr#bQr0^f9RpDY7P+D5|Qo&7`=$$!pRr6NWC1tx0=ZPryaarNf%#_b(yh9r5?L-or!U^Qkh2IZbFGKs=NK7<(FzE&ybTp!cMh&(eZpbJCe>4n!{BZl{Q$SW>m!&y8FHgH%Wf9k1fMg6>{)Lz%3WlQ?H;hyO(f-7N8$AMRMa$7W%E9IC2M=eU0P(1si}Ro!kimup+Lk0ghTydVO`u`|k?=a)Tytul9m8HXrz9emo<!M~lKM0f)6N%!6c0F*2p5s?2tVFh%LlSZxTs(7Jc@<q)u!h_W^^Ozr7c<y2qUpg@qrj4uoLh)Y9OLgDnqzHj_YHHw$_9QlCh}60o1wv1}<zR!NM6#5~eU-*?ae(+^uL4MEv357tiz5pKb%)ADt^5Cfy0ENwc6CCz@<z?fY(mhcL4^7m3v58di@@MD!@&o89H4jb?k4;vbQH>b6AYx8skP4b@A&<TV4-E$ng_NR(*eX)+#}ULa35XPw9HUx|{6Hn-Te6=BhXFug8t-pTHF(gC4KJ@Wj+C>3{T+Z6l*`3COe^2!T!C$<$%gTCor_sJ1TT(Dc!ra=fG@&*R8a=zhT&AAPA&RA^S;?Nr~j(zq(*kGOyv7x%$@zS1=ey&935>Zif@XgA4B|HU~HN=@L9qRq9>DAOk7|Y`{{N%`DzdcKfF%op5Eu@D6CA`KB?CWN-+p%tInqO!&!Nq2<mYLF61PJ*{Qc?jNvFJ7;c8!~3P+eX+DO)+O(9kJqcqV30C@9ES^#X+NlKX?iQ-^Jm%NlDb25Ge0i1ibokmW9#Ng@JNFs!@5D9LR<$t2QqKogz-S^si*!#3FqiYmC6)z^}Zem>%R{)uc&YQpf^@ZaCvecVe?<F(thg2p{X8@A=DLV?aOEK2<99fil92@(@3uG5?xlT4VL#|df{Q;b9uNctAN>xA_9RDPgY&p-%)#lMek8z|bOv^P(%4<mQ`obkS}V>N7{E{Vh__(n<_!Ddxeo=PjD>^}rV(L$%k3eY>8gcCB5CVv*~*A2Zawh6>Jen*(6i+aHZF!(e2G+YnHNbxz9+ur2&N@zB0b?*sv1s(-_VD!6)_}Oe+E>||&3F8bwM_3XE5pG!wU(@c`%D0(L$$Ylbq`o@IH;B-9>Y_FXGwPzsT9M*q@iF|IIREZ$DNrXkLWsEdGQgt2vUN~4ss}ai3}5eQz6GT33djQykji#}pv*v40jF7|nb{ajLJM6|Z)w`qsc6PQO79kDEIG?mb>cDO7+y4^b9m^*e8sX#vJe;Jy&@jnOWUto6P?iFIQ4&Y@)90Lkj4-5pQFBy2exDK5A@woOgq#fKqCDBhK&c1m+NXxSKDX&*Py~mdV0{z^!W&OoH2OX3Hsau-Uf*QH$@RB@-F|Ao7P?~^aCy=!HkW8zjXmdbQ4E0-kV0ln(<Jo?{`EH72=UC-bGV9V7w9h8>y{R(*7)y<~73^5jrNPGBhhRanW_2p{8WBri`xwnUp1j=6sydJuRH!b6vl)sn0n|?y;bw$Y_9v0<Ch;%JCk_grmy<3GGk(PP)=)4`y2__0Ii-7Dr*22{gpoxg@*CQXlk|D5*nhVdpssPhw^i2#BqzRnSewI7=WAWSo{RJ)uLs6^z^n2|^)IzZXT+lv)IBx2R}hL-fJRLnAUp7@>nBC2@NQUP4RuqGMOdURm5B&BU`+N!2lujHNpb-F(>V4G(C(Lz^{8Dd*DKg?W&+HD!)uA4Op+nN}npGiTDi5hO;P5)I1KkqYN2?qZ0MbX$$N{DLYEQYojT1nIM~)3o5DoL}0k^m0&2ZiW{~QvF?7QhW!w6lb++y!3-?vI<(aMy53KzgQiNtYhj;(M2eTEF@OU%RYOwDvr%^Lej3UojMXj^ef~QzO6c@TZO14^6v1jSsJ+?5hX=mSmgn`!Y({6kOdtPu$UB-Jw%8<#M2&N6xI4Mxe4Py;wTf#^s$U&E+#%mHhh@j#q?~TMhsZ3=v$LMAM6e2&e2?4L}okmt<2^uO2OoZ7Qx(ZstuvA6v??0)wOf{l)NCvLR5^Mk1Vn)k|yeRy?k^^ce>#g3yLL~MZ0f1U!AJ;^Z@H`oAVC9%rD|&B(jtR*AB9T(TPQhg8G7!XvCZ)8`G^TNwjBMt#I5_#ZaN@OwZ2nXaNVDG#B_h`MxmWTGV}E+Dr|y#L#RYu;}S)NI`GNMR8Uv31v1pd}3`JA&<`5U@7f|@Q#lLfz)sqI)xCXM=0t~4=S^V3Va{Ir^lZ6uDh47X=@=ON46zH<S=4?NY!#?OYow-W~7|wh~sEUw>DKeijX-?^^MqkX-G!J+GZ&aJfSP*XtY`XBoPeLg6S<Gkri`6V@MK*<KzegI|YDa+85rg%FSfeU12d1vNXF@55evS^27(C5n8Y1Vyy8@FpZC#<V50UIfbU6vl<kS<8O3gvP3CNyV+{IYf==UrUWK0V@|W7JBo$7(3~}SDmsUR)#Y#&aNBXAmklvSR%iOO=^N8b9+qxzrkkVPMM9fa7;b)+^{q(Zl|zmHCqLH;$P|gR;+j?sNGnmwYC=}{eD5nuLj#8iwUo#R&`=s3H^K8KTd4RkgLFD?B2_<zMJvscL3)j;9)bTZQGI4uzfOo>+9dFD$OH>kLX<E1t3cBtaP!}02*5aBD9Qp_$(gjlLMMa6gu`-at^{hEh3D3i9Uzo6IuQ0GVq^GjWnTE;fUj1B8WPY>%h6cd_5D&qA1-&`ok`A>VCoYp7*dLZsBE5rxu7oWn(CX5^oT_XfD;)5Iw?k`Ch6C@Q2>f$??FH+h$m?{oKxon#awX}Zj?pO^LsL<H8*Zl%Al9aGhf~3*=>9s>YKD9Oh8O<5;>+SVL3KZi4fvB6zs5^WCDTjGPK3&njI<x5?$L?EZR;DfYWHo+X@b2K`-1wuSnS6bQ;@uI*MgT<V+!|OkzvYO0DP{C#!+1T=?^X!^=Qzo}g*){H$tXZ8<C?ti*`?Mp-QP&=)|jVPQ&Qk>Wu*S}<|x_U!1!X>~TLCD{RIOByKsAvIV-CwS@~XW1Um*yikn{rBIW4D+ul_aJ8*$Gqj(J(5L@Dd@04A;0VCRH3PLO+9jNav=^NQ>+K|WeGPX?Cb~@avC}*6rrk<D1}VRf?q0Wo-tLVM&<Qg5$J+Mrx?t;Jjk1^M1fa;B83QV7Oc#Ad2v~6xFR`41MT<@r<}D_s|1=9I%90~RHbDh|JK*6$Aqg?*m7nTo2Aiu6v1ScC48He6tlMsDYPGEqlC-XcgPuYaEty3JYzA$&R0k&PxnyOeaTmTo{)^I`@;DoNZ)7({Hd@21p<AuB1NgvK*dMTOQj1phJ}zw)b0`jZWVSsq=0liD-hvzmTKAi58uN*DQowYO)hp`5G+T~b8V5saHQjALr3YA3}OTUj6a5xGV2&56q6Zi<D(%vE8PA%uoM`JoafLG`5~8p!m|-Vh&dQbt>KA|&y`~lTUSzz%tMP-c^n#e!soEh>MXENz)a!ltL@1U>Jyg#uE_dF86W`?a!o~Wb7|YTOIMH@AU8IFB*IY}maq!p6mS()`$EUZLL+TH4sCv$QzDU+T~ebXeOZ7oaS~pZUNy>8Zn&0IMKp<^d5fq#uu8_@7kamjS-nJ~A4B@QQLSB|j!A(arYkYbNW?6)$~Op#FG$|F3T-g8&4U4h1zHqzy2-M-XfDc3!qsqsI0=d3O<MR9wpa*y@@zzOR^)56XfCTnb)8cray?X?peDnghV-Ky;GAr5iRReHOT_JRQ!(a)kU2R6n58v1I70=Tu}88Ix&{6KTAQm!Q}#<zwMb-#Co7Wt;art#SKy|?-k9i`!;TXZBZ{ys>P<zSlV~=w2g%(^gWZ!gdI6o6ouAK7z#P1#cA6KClY^a8KkWbRQ76x&eb}e@cD%+J_Cw@?Sj#3kh6mBLq3NwG<YL*wZJ-?vf#LgtKt7WnpP*`T%V5&>!YVWcVDpOrR*AJqTM3Z7Z>Mv0rD%0dGqX8<(s}zzNSz}EOCThaWd^8JT7p@esPqhH?qcg`hsaqQkGZym7u#F=VpCOeSCWm%f}C~IDa;_rVMI~mW*eg~_2#mgTxo_*sQCb>NN3RvCGrSjp_>LryuPy8tzD&mSYhZE5D`HHqFO*4Q6%y+O;Q|i8Uj#*NCe1K@(f?C$WL2YU}yv>&?dpqUI_6r2H)0&TFs;a<I-yeORlILtC(<Y8j%qT$}5z_h(GpXjLv0p)Uucj(VtzMSsk~GpkNwv)#MaLK_WvPYaCUA*8yD=ZgGcjzqcp~k;Ha}aI&?Pp65OLkytz7?H>DhW|icUUOcsRn9dh2kq+W#Hj|vk`e+Rpro3VX&1@Cm9Hh*^D^^4aIS=?)Xt=F+4q%1)8f)v47)6+zf+Fj#Rt_BYFO~_-05MRFTxdWROPV%v)mTgsO#_s6Pir;{g8T}7AA(W_y$gLWP~uL1Hi|B#GRET+zqyaM^?6!f6H<jXEyPr2p|be6vC_xfO4xa%Z%P5X=*%8lKbpBtj0&NYr(r@<>ndT4Ogyu=a;ka+5G_A8wvtHJv3d}>l8M$to;ww=yDdFTu9Q=d&FR1t$-;n^aIH+AqC7Slch8_nU)C~LeyA`Em^!HCaS~nuF@{T3ktx~BTOX{_9MwAOsBJ=u=yGQ}AhG4ju1(n;jHN<QOV4pSlvH3P<eX%#uqY2ik`$c}O7LvTU157&81qoLhD4Rhg5i9F)9OW5a3iXXa1Pz2sFh?Fks$8iXe7o7aSJvnfn-%b477yF*!OZE>U!mAs+LTRPvp;sxzbj#%>`x>V6_fFuLvSQ#Jxtr4ary=U$RO{VvBf!@X*47k_1mQicPHI{;v@4VWl1Jyv%k$%UcGP5R)Lmv4WgU31h<a!<8*(=_|))Bs;4ZRvvuhOj&+UOk80aP9(>!m7k4{v6fP{4y36ueS7MMCmbYL0_#Lf5<IQ135Qckj;VyE2qmHcv)q*(p`ZXygA=yV6}_%1`L3`$sixf}YfnZZ%ncCBNXaL|SBZ==7A+3uUX`scs7s(paP)Kn11S_euZVe3AH#^96Zf)HJ}J=$;n!^7+vZV`js)*Gt1!ORLtU$^qfN?Jga{_M-|%X-`4uf{!cMhRCBMPWjf<0h)l6T}y2P$TCLU$kmw86DE=El^cg!YYki(vUBGLTHvUlrVB?I+3=24qjm03BNG{_xN6mH1jD{V8isszwlnQfCxUwnBlR`<+zcfGiT8}Z0tCol0NjtR}C;886~Ki#W)uJ^<%%OrDEAs0=~4*(CW3gT&`f-GUf&%lL3097xX2QOocxf-~Ente($xP#EGu)qauwUwAjPLiCBrRK(B(V-4HO&J0SgXa|NK=o~%RkL#w3Ke!J!rg;(C?L}#<^~bzcTzCk5b$aX69E5M26rxB6Wn2C!UGgw$J72uEqN+;zOw#Z${uW&gXejNS85_*Bu{1#wlMS_%AP?WA;VlYZ5nB7E$|oQSxBNNOofmUG|Givg}jV_P@!<@AxB+lYUoge0-!uNNon+y%$g^;Cn^%~xQ|Pnq{`Ln%;>FxDNO*+Ay1#7Qvf%PB<J4IXW~RX#o}RELx(Pu&0K&uUP=;d6IjzZrAPF)B?OA6pX4s}f$EugY{(|8$${oAxex(3XsPzb2naS80RU-{51)6fr|U&{tdv#((dbnDv+BVUxrTVz<u!;LpErR-Mb42dw-a;TBsC>5uUut^F_)93P|GA~LD!Ar7^bUFZf{TheG;tDN@RveUXBC2SVP-P<4aqCuwb!H)8h;zRzxFF(Q7%};D(p9AP@qQi36sZxh|%2<>xbNbx*BRLZ3fT2a3j6r4TZSm1HO!6#|aeo3q8NRLLT*E3y{Q7|U$nHmA)<pY#GOeet{J1Cv8|(_FnxOz3>|%t>B*kBd5q{G}F|ueV0&$s{gJJiQ$APYdHIDJbN=GI^^(WQLW4#|5E@WVqP!QcVpaK*3LXSqriP@|lue4FWhis=-Jfi7-M{@2g2~CYUW!lB`GZDCf=0CB@ckYX}qVY*<|sHA#^!<J_o(>%untwr_bI>bZ%A4`J`9L?CHjsXM3&SW&7H%xhmP>$YMn3TP35%_O;faUXTuNJT;yD;#L@Bl{O?BgaA%@jz@XXvhpI#lk^n*4<iF>J&x+3wjel_D|0IP|v^$-$o~n(>0j;;G#PNcD<4#lh(I3Z=XY@CaSpq(T=ItryvkqT04N0J~&^QIxoqYmLklA%vI*J1;tS!3eG6pNf&CKu|P-b%NS^Be3mSkQ!z4E!s0u4%pN;VX(zeCQpvQuWtN_UtUK6o=LL2Ik1mp$9tYxl@yudgs0=MTMY)GlM0q&eg;%fpX_!qn>iRWVcBN8|Iv;B-<$*aou1R(9oS$ei=*GoK1;IKhsl;{16#Y=EI_V+4Mk}I3v=%0W3HEAwpy(F@wv^S#L_X3;Vszy5@OOn<)`~U+)*pO^uiKFuw=i#@M*Cqy-+Cnq26weYKs3NO*Q1iu5zX;TvVD`@g?V~HU2P^Z5JM^pQ3K0@_dFLVJ)2olF#J9mPbP327HZZ?IOf|0QFBQa&^hrgcdJ=ie3Zmu*w&>KRO*k_ac==%3cOoa2`XpwaO!T5CXuj7N_f^rRn#GLC!)lawHuxS33*7f?;q{lAzhnKu0~Wh3IiNVxE|#cCL-A(@m}EAuiI-0QkqykL5G6kk8+%?ecXzrr3jOBLPg?3uut|Jax@^<AwS$mRiY+jMo~h=S{F0&dVKPr@lYYp?Lu^DVk>efs5}kRsRyJI-Gz8vTpV(4AZndt>rhIua0_G<g}@3Xu;#>WJHk#2e$HjJ@S~z}@5#MyVjzX?s%Nn1ijRN*LTLuvUaWhV)i<>2*oE?BE}NHXQs!6Y6cNcEP|gVTYZakDsUaGr3uE`Chvkt|Xi7ply-v-mli>40Kzw`+4di5#%x~R-_W}xKv=I|>S+8&=Ba0moc$$*Ucoiyc1aNnOk3w6$WLmfr+rMawoqp*tGSx_0!smB9p0q+CNxceradI#_PM?;y-G$hxs%yj20}qyrSf4~k!Ykub#Pop{zKS2%h3CO&+z{O>4=GX2Huq+_j&*WX?RZj|E9Ze`K-8h2u5WM;4E)VPP-xLpwBHb&1g_8yZ0MEi=GG`52&3o0u^7szfGJGQ$*)t#GFl6|>B(28xW8m2()-xtLbH-Wd5N{S?c`{e5Cc<eBRlN@XyP1ztg;a!5fBEFT2ovScIUZ(rxWS)A=<shLLqx&OvXfzl`11Fj-G?sr6LGSDTQTme7SsmI8GpV`BfD7wrD`wPV@MR9Iu>J$0gO)G5$KTZbDX50{>+2%&BTf=ty68pnKt*v}=(l$5U6K$~+idQ?PCYvn(R27_0RrBvBHzl2{+@kS4zg)fy7L6S{QVZiMrxsANL3Rzd_DR0t4qgKZdJw=THu+F(h5pT;YOr{4(O$jcPJtd&OKK%fS(aBEt+?L5c<WbMsnWAVSs5anD>&y}AOE1Lu>io=AlT0HiD@=t|Q1G!5{(t8g^5^7Tz(nx+%!4J0yvHTU(Vds0_r8P1-JkEKuDo+wso`$<1=l2SM9x7mEf-53{%h58I1nUql*<Fg*ZyERV^Rw^oqWr1jmVfz?#3G_4uldpsa1SqY_Hv1OW_{(J^qii2<!EaOIR%=-ua@~`)iGy_EzDU97p_X#*~Qq{<wYBdum_6FD&C8GryWnmQR&dVC%Oi3*+~bV)G0@KD>ob<9Sj^i<vLySgQsrItt+PnyK8B%F1ioXq*;^&#$o9-XVx*giF!V9+bNI$v=LRfmKOgglAdW1%2_SHZq&SP9}Dpe*wOqS`xI=*aIy|8zD<?Hx5{f*@fw^MW-P2hw9i2~NpXZI_PBC0lmt*Jx0KTQma97dZ>6Oz1=ZCEeVYau;$dOd)TMf)v);m5nIOc-(lR6&W;02X>stl4$H4KkXjgc?9N<v*GZcb7bgl_e;9S5-LjDsf)S0Q}n-Ga}c9-EX!dt8)C5s?MghU9*CXmNyD$bvl;Hp4q5fU1r4S4LG8DKD~BVJl=J&G&Wy9Wp|W2@3ii+Y7aB_%p52|5Q!%FXa5o3<Eq7116eH836TkP9^iJ&a9ZK3NE{N2+qrqM&#48Fm?)E*n7y(9L9{QGsjd^ra!R#L7Ow0v81V6&@TDDtagBzZR<+7E#lwY-N1{;*Li(GtqC+>gPp*wR1>R_GLM#4D%u96YRDe3g!hU-nIkdUfEJsF@$}OI@~M%qUZw<Sr3cZPcal3PNhK^SpKVav?69Z502+o<E9&&%1eXsV}<%o3e*Zazs6MxJm_@XRHMkv^7_*uQQ>bKpK;Y*5$9{bNn>YsNl+9sQO}sCYyz=@5U{SAw;_zm{2F`SR+}!MB}rmbAu~d|gSvNlmMqIDjt12NI>p}CX_F|!1u^6VEEoHxdT%e!-&>2x0J&+bXt$-+C(3UTTBR#^1=}q%bXgCe1U>WQQ=$-R<ifY^S#J{^0hntz<+F-hy$+a>QAx9^bXH?4xyaH=_SIQRS>y}2MQTzKY-`0FnD<8DNN6=9?|kt?p7PR%HAd=ilr!ND3jDv0jrSFTPu}`V3*Q=mvskqFYg<PQ+3?~%^!hWZuV`uko5pJ9xO|tBTb}!+NV%yAPSqn0q>v5wh3R>h$x_9@H$#a71~N-FW-vzH-@+9WuRvsa2>=sUogn6?uQr?)`C&uqsR%Q84@O?B4Z}?{>etdzWqVQ!P0g}|azJFTD3)qqTljcw4ysC=MIqCbDFx;^-VP5J=R)SEteU({9s`fJdcyZP@UMb&U+8+TRXVN35<E}dagu?IPIm~~1P;D}@aO<hT0((n%uXHfD{SKiJi`L!Hp!1~LIJXz+pWkFY-T6YNIK=-m1?<?OcGk`yh||+$rXmQEuc4+bEbp@j3(_i#2i8Y7NP<Gt7#R<!Y1<GNCaawO%G*)AWS%D%Xty(NI|rHoV&CrvO+cK$u4+#xK~2VsT+qY8qho|H_c}MQLa-*vZb5~pz@koRor=9X_}NQjx*?}$b=<L$OPna#pp<(75tQ!G3&`!cJ&0%-gWmsy@ZpZS71*A;Wnixv|jdA0wQfJXtZ8gF&OBQ=t)-0(e1}4VoCzVk1f|SCHZ+FGb(AFR^}~a2opA<GmhxYbp$F`Doqxy6UJSpb#!4;y&Cj5?$V1#x9)cUVnQOIaZ_u7OVqX@Q>KT8ptzK(@nE<V2#HcDv&j<nJ<7Dp?c4GcT%LVu>mQ@2A5$y@{0@;(sAYCuzeQcUzMkR*!=-X@anUN>qGx4GYI{ZU##2Yoq|X1HbbX0l?EH$Ye|*8#oWhZTH9O<C+p;A2bnY$@YPJgIEmD!`F<485Pc#sLEDNDFqoJ;z;(-yB6X=M{7l4v<j&_}QL_M+ZK7F`-|LeQE<0VUqgDfnC!i}Dfqso-fAR=8WDq1Xz9gX&uW_2+O1=_-~$0lU!RB+VDw#ybp$TETy%lX&M=@V3Hg<Yzir74N@@0wT!X2~0p4GG7-v?nfVFbu~fnZyDVvF2FP(oDf(ViR!os$r#J6CPm*r?<`y96_BD992>z+)dO!i0&Y~6nz~>!aooyxE{J_gwo-@zS;%MPGkd9P6EsRio!fzsT-?QPtZ5R@<$<QVf}eUaRo`>^sKISj*yhZD&m)`1ftlBi5euHUhN@Ww1nW!5=nEUBR}?#v{1F5(1Rf}l476<r~@B+o&{ReFGb~Y7EN$^cPJ$;o^8=WlxT`EJ$D*|A@H8hxQ;I2<&0~Z)^<m8|Gd*q?}r;0_TMmKpnR0rbwmWR(@6p;)k#_#F3EsCP5(X~w&K2@!IM{D2(GVpB@x+E(?$q9$dyB%hQA0N>FoX-hzv(&v{qZ{ha4$@yVnFA53)SK-nGM34Z6XXSc74`iX#Z9n+5^z*%Vq^{5z&{K_$6#X}`>i))w%kJ>A5#a?G$poCH>(^U@eCAs_LikJ+_SgN76`ca0_m4G5{J9BYgGphNB`TAVK}P|wIfhLF0zNnvc3%0gvf-(XUSftUQSd7(;6L0yZf2yCN9&*fXS?f^8rEPI?9t?&VJt<6eJ3b=qQnVz7d3FO%k9_tG4k%j^rVpH(V_%hE6)+#aDI$L7xR!=7p9<q6dB@Bzhmvtv_?U1pe$wFg&$x(c1kw@Z<oI@O&$O!DisF0ddTTDw~J-3JNwCuN)gfuc(Os506V|jqh@v`S0=EL2OHxGB{Po}k=uV%s1{q5aP#A#F5CP&~j^@@w22;&=^MwbgBV_})bsaSj?&c$+Y|3N2%)a?4_OjKrqr@x@9NU<rF@y%2FatJA(o_H3*iTekh9_Wc7EqRE;SLXsL5&d&kV#2`7Gq4s8xuEf*viJ)Dpl6>bV_coDKmPb@nX$A)vvMA_d@`wKW0(5z{{e^KT_g')).decode('utf-8'))

_V7_CURRENT_ROUTES = {
    "cooked_ep107314414": _ACTIONS_REPLAY_1,
    "cooked_ep107310411": _ACTIONS_REPLAY_2,
    "cooked_ep107301740": _ACTIONS_REPLAY_3,
    "cooked_ep107294852": _ACTIONS_REPLAY_4,
    "10c4s_3q": _ACTIONS_10C4S_3Q,
    "8c6s_3q": _ACTIONS_8C6S_3Q,
    "6c8s_3q": _ACTIONS_6C8S_3Q,
    "6c12s_4q_first_yarn": _ACTIONS_6C12S_4Q_FIRST_YARN,
    "6c12s_4q_second_yarn": _ACTIONS_6C12S_4Q_SECOND_YARN,
}
_V7_LEGACY_ROUTES = {
    "10c4s_3q": _LEGACY_ACTIONS_10C4S_3Q,
    "8c6s_3q": _LEGACY_ACTIONS_8C6S_3Q,
    "6c8s_3q": _LEGACY_ACTIONS_6C8S_3Q,
    "6c12s_4q_first_yarn": _LEGACY_ACTIONS_6C12S_4Q_FIRST_YARN,
    "6c12s_4q_second_yarn": _LEGACY_ACTIONS_6C12S_4Q_SECOND_YARN,
}
_V7_CURRENT_SALES = {key: _v7_sales_schedule(value) for key, value in _V7_CURRENT_ROUTES.items()}
_V7_LEGACY_SALES = {key: _v7_sales_schedule(value) for key, value in _V7_LEGACY_ROUTES.items()}


def _select_route(obs, step):
    seat = _seat(obs)
    state = _ROUTE_STATE[seat]
    if step == 0 or step < int(state.get("last_step", -1)):
        state = {
            "last_step": step,
            "legacy": None,
            "label": None,
            "third_yarn_milk": None,
            "v5_gate": None,
            "v5_shops": (),
            "v5_expert": None,
        }
        _ROUTE_STATE[seat] = state
    state["last_step"] = step
    if step <= _V5_ROUTE_DECISION_STEP:
        state["v5_shops"] = _public_shops(obs)
    if state.get("legacy") is None and 24 <= step < 72:
        state["legacy"] = _v7_legacy_layout(obs)
    if state.get("leader_profile") is None and 24 <= step <= 96:
        detected = _leader_opening_profile(obs)
        if detected is not None:
            state["leader_profile"] = detected
    if step == _V10_V5_GATE_STEP:
        decision = _v10_should_use_v5(obs)
        if state.get("v5_gate") is None:
            state["v5_gate"] = decision
        elif state.get("v5_gate") and not decision:
            # A changed same-step observation can only close the gate.
            state["v5_gate"] = False
    if state.get("v5_gate"):
        return _v10_v5_route(state, step)
    state["label"] = _leader_aware_label(obs, state, step)
    label = state["label"]
    if state.get("legacy"):
        return _V7_LEGACY_ROUTES[label], _V7_LEGACY_SALES[label]
    return _V7_CURRENT_ROUTES[label], _V7_CURRENT_SALES[label]


def _v5_is_shed_access(position, board_size):
    """Match the engine's four orthogonally adjacent shed-access cells."""
    try:
        x, y = int(position[0]), int(position[1])
    except (IndexError, TypeError, ValueError):
        return False
    half = max(2, int(board_size)) // 2
    return (x, y) in {
        (half - 1, half - 1),
        (half, half - 1),
        (half - 1, half),
        (half, half),
    }


def _v5_projected_shed(obs, action):
    """Project same-turn shed stock in actor execution order.

    Kaggriculture resolves farmer and hand actions before market orders.  SELL
    ranking therefore needs the stock after executable DROP, PLACE, and PICKUP
    actions, not merely the stock visible in the observation.
    """
    farm = _farm(obs, _seat(obs))
    private = _get(obs, "private", {}) or {}
    projected = {
        str(item): max(0, int(quantity or 0))
        for item, quantity in dict(_get(private, "shed", {}) or {}).items()
    }
    inventories = list(_get(private, "inventories", []) or [])
    positions = [
        _get(farm, "farmer", [0, 0]),
        *list(_get(farm, "hands", []) or []),
    ]
    unit_actions = [
        action.get("farmer", ["PASS"]),
        *list(action.get("hands") or []),
    ]
    tiles = list(_get(farm, "tiles", []) or [])
    board_size = len(tiles) or 10

    for index, unit_action in enumerate(unit_actions):
        if (
            index >= len(positions)
            or index >= len(inventories)
            or not isinstance(unit_action, (list, tuple))
            or not unit_action
            or not _v5_is_shed_access(positions[index], board_size)
        ):
            continue
        inventory = {
            str(item): max(0, int(quantity or 0))
            for item, quantity in dict(inventories[index] or {}).items()
        }
        operation = unit_action[0]
        if operation == "PICKUP" and len(unit_action) >= 2:
            item = str(unit_action[1])
            try:
                requested = (
                    max(0, int(unit_action[2]))
                    if len(unit_action) >= 3
                    else 1
                )
            except (TypeError, ValueError):
                requested = 0
            quantity = min(requested, projected.get(item, 0))
            projected[item] = max(0, projected.get(item, 0) - quantity)
            continue
        if operation == "DROP":
            deposits = list(inventory.items())
        elif operation == "PLACE" and len(unit_action) >= 2:
            item = str(unit_action[1])
            try:
                x, y = int(positions[index][0]), int(positions[index][1])
                tile = tiles[y][x]
            except (IndexError, TypeError, ValueError):
                tile = None
            structure = {
                "COW": "PASTURE",
                "SHEEP": "PASTURE",
                "GOOSE": "COOP",
            }.get(item)
            if (
                structure
                and isinstance(tile, dict)
                and tile.get("kind") == structure
                and "animal" not in tile
            ):
                # Matching animal placement never falls through to the shed,
                # even when the actor does not carry the requested animal.
                continue
            try:
                requested = (
                    max(0, int(unit_action[2]))
                    if len(unit_action) >= 3
                    else 1
                )
            except (TypeError, ValueError):
                requested = 0
            deposits = ((item, min(requested, inventory.get(item, 0))),)
        else:
            continue
        for item, requested in deposits:
            room = max(0, 100 - sum(projected.values()))
            quantity = min(max(0, int(requested or 0)), room)
            if quantity > 0:
                projected[item] = projected.get(item, 0) + quantity
    return projected


def _v5_prune_terminal_wheat_seed(action, step):
    """Remove WHEAT seed purchases after the route's last future planting."""
    if any(
        len(unit_order) >= 2
        and unit_order[:2] == ["PLANT", "WHEAT"]
        for future in range(int(step) + 1, len(_ACTIONS))
        for unit_order in [
            (_ACTIONS[future] or {}).get("farmer") or ["PASS"],
            *list((_ACTIONS[future] or {}).get("hands") or []),
        ]
    ):
        return action
    action = _copy_action(action)
    action["market"] = [
        list(order)
        for order in (action.get("market") or [])
        if not (
            len(order) >= 2
            and order[:2] == ["BUY_SEED", "WHEAT"]
        )
    ][:10]
    return action


def _v5_market_finalize(action, obs):
    """Rank sell slots by executable local impact, then merge duplicates."""
    action = _copy_action(action)
    orders = [list(order) for order in (action.get("market") or [])]
    params = {
        "WHEAT": (25, 10000, 400, "sqrt", 0.8, "log", 0.2),
        "CARROT": (35, 10000, 450, "log", 0.2, "sqrt", 0.7),
        "TOMATO": (60, 10000, 200, "linear", 0.4, "sqrt", 0.6),
        "STRAWBERRY": (120, 10000, 100, "sqrt", 0.7, "linear", 1.6),
        "MELON": (250, 10000, 300, "log", 0.2, "sq", 3.6),
        "EGG": (50, 10000, 332, "linear", 0.4, "log", 0.2),
        "MILK": (160, 10000, 122, "sqrt", 0.6, "linear", 1.6),
        "WOOL": (200, 10000, 105, "log", 0.2, "sq", 3.2),
        "FERTILIZER": (100, 10000, 200, "linear", 0.4, "linear", 0.4),
    }
    # Local defaults preserve the public curve. A complete curve supplied by
    # a custom environment wins, keeping sale ranking valid when the evaluator
    # changes its market configuration.
    config = _get(obs, "config", {}) or {}
    curve_sources = (
        _get(obs, "marketParams", None),
        _get(obs, "market_params", None),
        _get(config, "marketParams", None),
        _get(config, "market_params", None),
    )

    def valid_curve(value):
        if isinstance(value, dict):
            value = (
                _get(value, "base", _get(value, "basePrice", None)),
                _get(value, "equilibrium", _get(value, "equilibriumInventory", None)),
                _get(value, "scale", None),
                _get(value, "below_func", _get(value, "belowFunction", None)),
                _get(value, "below_target", _get(value, "belowTarget", None)),
                _get(value, "above_func", _get(value, "aboveFunction", None)),
                _get(value, "above_target", _get(value, "aboveTarget", None)),
            )
        if not isinstance(value, (list, tuple)) or len(value) != 7:
            return None
        try:
            base, equilibrium, scale = (
                float(value[0]), float(value[1]), float(value[2])
            )
            below_target, above_target = float(value[4]), float(value[6])
        except (TypeError, ValueError):
            return None
        below_func, above_func = str(value[3]), str(value[5])
        known_shapes = {"linear", "sq", "sqrt", "log", "log10"}
        if (
            base <= 0
            or equilibrium < 0
            or scale <= 0
            or below_func not in known_shapes
            or above_func not in known_shapes
        ):
            return None
        return (
            base,
            equilibrium,
            scale,
            below_func,
            below_target,
            above_func,
            above_target,
        )

    for source in curve_sources:
        if not isinstance(source, dict):
            continue
        for item in tuple(params):
            curve = valid_curve(_get(source, item, None))
            if curve is not None:
                params[item] = curve
    inventory = _get(_get(obs, "market", {}) or {}, "inventory", {}) or {}

    def shape(name, value):
        value = max(0.0, float(value))
        if name == "linear":
            return value
        if name == "sq":
            return value * value
        if name == "sqrt":
            return math.sqrt(value)
        return math.log1p(value) if name == "log" else math.log10(1.0 + value)

    def price(item, market_inventory):
        (
            base,
            equilibrium,
            scale,
            below_func,
            below_target,
            above_func,
            above_target,
        ) = params[item]
        if market_inventory < equilibrium:
            value = (
                base
                + below_target
                * base
                / shape(below_func, scale)
                * shape(below_func, equilibrium - market_inventory)
            )
        else:
            value = (
                base
                - above_target
                * base
                / shape(above_func, scale)
                * shape(above_func, market_inventory - equilibrium)
            )
        return max(1, int(round(value)))

    def score(order):
        if not (
            len(order) >= 3
            and order[0] == "SELL"
            and order[1] in params
        ):
            return float("-inf")
        item = order[1]
        quantity = max(0, int(order[2] or 0))
        start = int(_get(inventory, item, 10000) or 0)

        def revenue(market_inventory):
            total = 0
            for _ in range(quantity):
                quote = price(item, market_inventory)
                total += quote
                if quote > 1:
                    market_inventory += 1
            return total, market_inventory

        now, delayed = revenue(start)
        later, _ = revenue(delayed)
        return max(0, now - later)

    projected = _v5_projected_shed(obs, action)
    remaining = dict(projected)
    sell_rows = []
    for index, order in enumerate(orders):
        if not (
            len(order) >= 3
            and order[0] == "SELL"
            and order[1] in params
        ):
            continue
        item = order[1]
        requested = max(0, int(order[2] or 0))
        executable = min(requested, max(0, int(remaining.get(item, 0) or 0)))
        remaining[item] = max(0, int(remaining.get(item, 0) or 0) - executable)
        scored = list(order)
        scored[2] = executable
        sell_rows.append((score(scored), -index, order))
    sell_rows.sort(reverse=True)
    ranked = iter(row[2] for row in sell_rows)
    orders = [
        next(ranked)
        if len(order) >= 3 and order[0] == "SELL" and order[1] in params
        else order
        for order in orders
    ]
    premium = {"MELON", "STRAWBERRY", "MILK", "WOOL"}
    for index in range(1, len(orders)):
        if not (
            len(orders[index]) >= 2
            and orders[index][0] == "SELL"
            and orders[index][1] in premium
        ):
            continue
        cursor = index
        while cursor > 0 and (
            not orders[cursor - 1] or orders[cursor - 1][0] != "SELL"
        ):
            orders[cursor - 1], orders[cursor] = (
                orders[cursor],
                orders[cursor - 1],
            )
            cursor -= 1
    first = {}
    merged = []
    for order in orders:
        if len(order) >= 3 and order[0] == "SELL":
            item = order[1]
            if item in first:
                merged[first[item]][2] += max(0, int(order[2] or 0))
                continue
            first[item] = len(merged)
        merged.append(order)
    action["market"] = merged[:10]
    return action


import os as _os

_ENABLE_WHEAT_FEED_GUARD = _os.environ.get("KAGGR_WHEAT_GUARD", "0") == "1"
_ENABLE_STRAWBERRY_FLOOR = _os.environ.get("KAGGR_STRAWBERRY_FLOOR", "0") == "1"
_ENABLE_MARKET_QUEUE_V16 = _os.environ.get("KAGGR_MARKET_QUEUE_V16", "1") == "1"
_MARKET_QUEUE_BACKLOAD = _os.environ.get("KAGGR_MARKET_QUEUE_BACKLOAD", "0") == "1"
_MARKET_QUEUE_PAD = _os.environ.get("KAGGR_MARKET_QUEUE_PAD", "0") == "1"
_STRAWBERRY_FLOOR_PRICE = 100
_STRAWBERRY_FLOOR_UNTIL_STEP = 640
_FEED_GUARD_UNTIL_STEP = 700

# Strawberry prepay: leader replays show strawberry is scarce (price rising
# well above the $120 base) through roughly day 21, after which combined
# player supply crashes it toward the floor.  Selling the route's scheduled
# strawberry volume a few days early captures the scarcity premium.
_ENABLE_STRAWBERRY_PREPAY = _os.environ.get("KAGGR_STRAWBERRY_PREPAY", "0") == "1"
_STRAWBERRY_PREPAY_MIN_PRICE = 150
_STRAWBERRY_PREPAY_PEAK_RATIO = 0.92
_STRAWBERRY_PREPAY_HORIZON = 144
_STRAWBERRY_PREPAY_START_STEP = 240
_STRAWBERRY_I0 = 10000
_STRAWBERRY_PREPAY_STATE = {
    0: {"last_step": -1, "prepaid": 0, "peak": 0.0},
    1: {"last_step": -1, "prepaid": 0, "peak": 0.0},
}

if _ENABLE_STRAWBERRY_PREPAY:
    _FR_ITEMS = tuple(item for item in _FR_ITEMS if item != "STRAWBERRY")


def _strawberry_prepay(action, obs, step):
    """Sell scheduled strawberry volume early while scarcity prices last."""
    if not _ENABLE_STRAWBERRY_PREPAY or step < _STRAWBERRY_PREPAY_START_STEP:
        return action
    seat = _seat(obs)
    state = _STRAWBERRY_PREPAY_STATE[seat]
    if step <= int(state.get("last_step", -1)):
        state = {"last_step": step, "prepaid": 0, "peak": 0.0}
        _STRAWBERRY_PREPAY_STATE[seat] = state
    state["last_step"] = step
    action = _copy_action(action)
    market = [list(order) for order in (action.get("market") or [])]

    # Repay earlier prepayments against this step's scheduled sales first.
    prepaid = int(state.get("prepaid", 0))
    if prepaid > 0:
        for order in market:
            if len(order) >= 3 and order[0] == "SELL" and order[1] == "STRAWBERRY":
                reduction = min(max(0, int(order[2] or 0)), prepaid)
                order[2] = max(0, int(order[2] or 0)) - reduction
                prepaid -= reduction
    state["prepaid"] = prepaid

    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    inventory = _get(_get(obs, "market", {}) or {}, "inventory", {}) or {}
    try:
        price = float(_get(prices, "STRAWBERRY", 0) or 0)
        market_inv = int(_get(inventory, "STRAWBERRY", _STRAWBERRY_I0) or 0)
    except (TypeError, ValueError):
        action["market"] = market[:10]
        return action
    peak = max(float(state.get("peak", 0.0) or 0.0), price)
    state["peak"] = peak
    if price < max(_STRAWBERRY_PREPAY_MIN_PRICE, _STRAWBERRY_PREPAY_PEAK_RATIO * peak):
        action["market"] = market[:10]
        return action

    already = sum(
        max(0, int(order[2] or 0))
        for order in market
        if len(order) >= 3 and order[0] == "SELL" and order[1] == "STRAWBERRY"
    )
    end = min(len(_ACTIONS), step + _STRAWBERRY_PREPAY_HORIZON + 1)
    scheduled = 0
    for future in range(step + 1, end):
        for order in (_ACTIONS[future] or {}).get("market") or []:
            if len(order) >= 3 and order[0] == "SELL" and order[1] == "STRAWBERRY":
                scheduled += max(0, int(order[2] or 0))
    scheduled = max(0, scheduled - prepaid)
    if scheduled <= 0:
        action["market"] = market[:10]
        return action

    projected = _v5_projected_shed(obs, action)
    available = max(0, int(projected.get("STRAWBERRY", 0) or 0) - already)
    headroom = max(0, _STRAWBERRY_I0 - market_inv + 10)
    quantity = min(scheduled, available, headroom)
    if quantity <= 0:
        action["market"] = market[:10]
        return action
    existing = next(
        (
            order
            for order in market
            if len(order) >= 3 and order[0] == "SELL" and order[1] == "STRAWBERRY"
        ),
        None,
    )
    if existing is not None:
        existing[2] = max(0, int(existing[2] or 0)) + quantity
    elif len(market) < 10:
        market.insert(0, ["SELL", "STRAWBERRY", quantity])
    else:
        action["market"] = market[:10]
        return action
    state["prepaid"] = prepaid + quantity
    action["market"] = market[:10]
    return action


def _placed_animals(obs):
    seat = _seat(obs)
    farm = _farm(obs, seat)
    total = 0
    for row in list(_get(farm, "tiles", []) or []):
        for tile in list(row or []):
            if isinstance(tile, dict) and tile.get("animal") in (
                "COW",
                "SHEEP",
                "GOOSE",
            ):
                total += 1
    return total


def _wheat_feed_guard(action, obs, step):
    """Stop the sell-wheat-then-buy-feed churn seen against the leader tapes.

    Attribution against the leader's replay shows the route sells its wheat
    harvest and then buys nearly the same volume back as animal feed, paying
    the market impact on both sides (~37k of feed purchases per season vs
    ~2k for the leader).  The guard keeps a three-day feed reserve hysteresis
    band: sells are trimmed when projected stock would fall below the
    reserve, and feed buys are allowed only to refill from the low-water mark
    back up to the reserve.  Disabled near season end so terminal liquidation
    still clears the shed.
    """
    if not _ENABLE_WHEAT_FEED_GUARD or step >= _FEED_GUARD_UNTIL_STEP:
        return action
    animals = _placed_animals(obs)
    if animals <= 0:
        return action
    projected = _v5_projected_shed(obs, action)
    stock = max(0, int(projected.get("WHEAT", 0) or 0))
    reserve = 3 * animals
    low_water = (3 * animals) // 2
    action = _copy_action(action)
    market = [list(order) for order in (action.get("market") or [])]
    sell_allowance = max(0, stock - reserve)
    sold = 0
    for order in market:
        if len(order) >= 3 and order[0] == "SELL" and order[1] == "WHEAT":
            requested = max(0, int(order[2] or 0))
            kept = min(requested, sell_allowance)
            sell_allowance -= kept
            sold += kept
            order[2] = kept
    if stock - sold >= low_water:
        buy_allowance = 0
    else:
        buy_allowance = max(0, reserve - (stock - sold))
    for order in market:
        if len(order) >= 3 and order[:2] == ["BUY_PRODUCT", "WHEAT"]:
            requested = max(0, int(order[2] or 0))
            kept = min(requested, buy_allowance)
            buy_allowance -= kept
            order[2] = kept
    action["market"] = market[:10]
    return action


def _strawberry_price_floor(action, obs, step):
    """Hold strawberry sales while the shared price is below the floor.

    Strawberry crashes to the $1 floor under modest gluts (linear above,
    target 1.6, T=100).  The leader only sells into recovered prices.  Sales
    are released when the shed is nearly full or late in the season, so stock
    is never stranded; terminal liquidation handles the final turns.
    """
    if not _ENABLE_STRAWBERRY_FLOOR or step >= _STRAWBERRY_FLOOR_UNTIL_STEP:
        return action
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    try:
        price = float(_get(prices, "STRAWBERRY", 0) or 0)
    except (TypeError, ValueError):
        return action
    if price >= _STRAWBERRY_FLOOR_PRICE:
        return action
    projected = _v5_projected_shed(obs, action)
    if sum(max(0, int(v)) for v in projected.values()) >= 90:
        return action
    action = _copy_action(action)
    market = []
    for order in action.get("market") or []:
        if len(order) >= 3 and order[0] == "SELL" and order[1] == "STRAWBERRY":
            order = list(order)
            order[2] = 0
        market.append(list(order))
    action["market"] = market[:10]
    return action


def _market_queue_v16(action):
    """Front-load executable sales and back-load dynamic-price restocking.

    The environment processes the two players' market lists by index. SELL
    orders benefit from executing before earlier supply can depress the quote.
    WHEAT/FERTILIZER BUY_PRODUCT orders often benefit from executing after the
    opponent's sales. Unsupported product buys are stable no-ops in 1.32.7,
    so they can occupy unused queue indices without changing game state.
    """
    if not _ENABLE_MARKET_QUEUE_V16:
        return action
    action = _copy_action(action)
    sells, fixed, restocks = [], [], []
    for raw in action.get("market", []) or []:
        if not isinstance(raw, list) or not raw:
            continue
        order = list(raw)
        if order[0] in ("SELL", "BUY_PRODUCT"):
            if len(order) < 3:
                continue
            try:
                order[2] = max(0, int(order[2] or 0))
            except (TypeError, ValueError):
                continue
            if order[2] <= 0:
                continue
        if order[0] == "SELL":
            sells.append(order)
        elif (
            _MARKET_QUEUE_BACKLOAD
            and order[0] == "BUY_PRODUCT"
            and order[1] in ("WHEAT", "FERTILIZER")
        ):
            restocks.append(order)
        else:
            fixed.append(order)
    prefix = (sells + fixed)[:10]
    restocks = restocks[:max(0, 10 - len(prefix))]
    if restocks and _MARKET_QUEUE_PAD:
        target = 10 - len(restocks)
        while len(prefix) < target:
            prefix.append(["BUY_PRODUCT", "CARROT", 1])
    action["market"] = (prefix + restocks)[:10]
    return action


def _terminal_liquidate(action, obs, step):
    """Top up final-turn sales to the actual same-turn projected shed."""
    if step < 718:
        return action
    action = _copy_action(action)
    projected = _v5_projected_shed(obs, action)
    sellable = (
        "WHEAT",
        "CARROT",
        "TOMATO",
        "STRAWBERRY",
        "MELON",
        "EGG",
        "MILK",
        "WOOL",
        "FERTILIZER",
    )
    orders = [list(order) for order in action.get("market", []) or []]
    requested = Counter()
    first = {}
    for index, order in enumerate(orders):
        if (
            len(order) >= 3
            and order[0] == "SELL"
            and order[1] in sellable
        ):
            item = order[1]
            requested[item] += max(0, int(order[2] or 0))
            first.setdefault(item, index)
    for item in sellable:
        quantity = max(0, int(projected.get(item, 0) or 0))
        if quantity <= requested[item]:
            continue
        if item in first:
            orders[first[item]][2] += quantity - requested[item]
        elif len(orders) < 10:
            orders.append(["SELL", item, quantity])
    action["market"] = orders[:10]
    return action


def _baseline_agent(obs, config=None):
    """Return the V9 action for one Kaggriculture observation."""
    try:
        global _ACTIONS, _META_SALES
        raw_step = max(0, int(_get(obs, "step", 0) or 0))
        seat = _seat(obs)
        signature = _action_cache_signature(obs)
        cached = _ACTION_CACHE[seat]
        if (
            raw_step > 0
            and signature is not None
            and int(cached.get("step", -1)) == raw_step
            and cached.get("signature") == signature
            and cached.get("action") is not None
        ):
            return copy.deepcopy(cached["action"])
        _ACTIONS, _META_SALES = _select_route(obs, raw_step)
        _force_route = _os.environ.get("KAGGR_FORCE_ROUTE", "cooked_ep107301740")
        if _force_route in _V7_CURRENT_ROUTES:
            _ACTIONS = _V7_CURRENT_ROUTES[_force_route]
            _META_SALES = _V7_CURRENT_SALES[_force_route]
        if len(list(_get(obs, "farms", []) or [])) < 2:
            return {"farmer": ["PASS"], "hands": [], "market": []}
        step = min(
            max(0, int(_get(obs, "step", 0) or 0)),
            len(_ACTIONS) - 1,
        )
        meta = _meta_state(obs, step)
        _meta_update_clone_profile(obs, step, meta)
        _meta_observe_h4(obs, step, meta)
        meta["last_step"] = step

        action = _clip_seed_surplus(
            _copy_action(_ACTIONS[step]), obs, step
        )
        action = _weed_repair_action(
            obs,
            action,
            step,
        )
        action = _clear_passive_weeds(obs, action)
        action = _cow_place_alignment(obs, action, step)
        action = _reconcile_scheduled_cows(obs, action, step)
        action = _guarded_demand_cow9(obs, action, step)
        state = _fr_state(obs, step)
        action = _repay(action, state, step)
        action = _front_run(
            action,
            obs,
            state,
            step,
            prepaid=dict(
                (meta.get("h5_due", {}) or {}).get(step + 1, {}) or {}
            ),
        )
        action = _align_hands(action, obs)

        _meta_front_run(action, obs, step, meta)
        action = _wheat_feed_guard(action, obs, step)
        action = _strawberry_price_floor(action, obs, step)
        action = _strawberry_prepay(action, obs, step)
        action = _v5_prune_terminal_wheat_seed(action, step)
        action = _v5_market_finalize(action, obs)
        action = _terminal_liquidate(action, obs, step)
        action = _market_queue_v16(action)
        _meta_remember_market(obs, step, action, meta)
        if signature is not None:
            _ACTION_CACHE[seat] = {
                "step": raw_step,
                "signature": signature,
                "action": copy.deepcopy(action),
            }
        return action
    except Exception:
        farm = _farm(obs, _seat(obs))
        return {
            "farmer": ["PASS"],
            "hands": [
                ["PASS"]
                for _ in (_get(farm, "hands", []) or [])
            ],
            "market": [],
        }

_RES_DATA = 'c-rlq30zd=+Q5$tE~yEY-Zb~EFtz3Cr)6?pAk$J&5J3S~P*4z;w2S64lcu?pT55~7P+HmM(ycU84#Et%<(_u0n%L(pGb{9Frj~u@o#8#qob#TU>2RKD=KDSTe*Q)fU*&(EdERG#%Bl&%U?I{XjQsS$cAwNDd!lb7g7RS_O9u9L`#gr+x8#3C_g|my-5V``pIG}?n;!H#+7FEomlj`&W`ASo(qfVQzV@*-(MyXTjs9V-zh|!Dp1F3?cFma|Kh;G!^M~tY%AbD~_nAmPKa|~(40^RLY4pfFqTu%N+YSGauGC8-*S1)thi)H3-dj*yxIeK!`R?Okh0_X#k{9CA$&R->k{wf97mi&0Fgcia3u*M~Ph#|2HOb$OpNy`)_EECC<$XlZe8dp?Gq`>ULS&d=+kk{&3Aaq-68`(r!Cq;s?|oWB*!49nVM<Q^zUb`<gH3yC>`Z?MFBx{ThVU(SS*6~aMmP!D@9jmhKd&xD?H)j;UCfnk{32H&Ov&H1q7V7zSQlyF2bn}m*yet2#s8&}a1&XE+xMKfC5!YPGQorJ`x87r*AgBjx_;_7=j-{zdu2lXlz%O{_F(1rRMsddUuUxal}yg>GoN1Ak|Rg1kJ%CR38hSBSp8@A->p*3dRe67V-uu7Ym>>*EAtCaf8LMun!jH>-KsgUS(3=LrrpSY7g?qI&!v$LFSjG<$Nv-EynU)ve|0(uzhWhM%^$4zKik}YE)U|y2^*mS@zjEyu&gDDn)l>siMT;2rs+)fj`sgdbF~Cd4?B*`mNJruD_VlS4yoBsqa}K_dRTh4k4rzN-!POkoOy#<54&j!ce)i?!XnsqKERXVSH_R@N`wA%Y8st8|C18w!Q@X(W6E&z&wN(wPRf3M+WGY<`__68rk`gnzQmQ`i+@<9`I~acrtn$P$zO+(??*f)wQDn+oa<YM+z>HYWHNmIt=Uq$+C!ZBck}xV6+QgfS5{K`W;Mdmy>4IgMi_zy#8V3e!tZhkfA#kXrqc-jE-#>j%YMF*=n)<y6CR&CmfRjYOv>*#ko3&yAmyA(bZUW4J69`&cSKmFTS~Qr8<e>d_Rta@)|x(H2pSMiEd&S)e8MM34>yfQ`=Lvn-oe_J(o8?|hUNEj3De)xU;n%FdoJPa`&>8O?=tD~x~s`^^~Xu$Iu3Rc?7inhg)p@-s6G7Lj}}trr^aO6OXcFZxlPH#$E{@T&EYB=g8p*%IBX*I>6SdevnA%uPw-0PeBu_bwgm6q_jP6<ZHcfQR_Rh=hSQ^1-t=MeN9PlTnGplXsDmA)=iVKo*b-Z8<D_TKCXiQGofj7zzfH%M@bog=Z3>yN@VFtuMrc4hwNM~Dg-cjkpJ+N^h%=26rtygM>Z3@vt&0m6Zs@Ie&6N1B502Cj-jx4}Sd`Sm3t@N4NH}nW=}ni*z3JY4VYun{KE#<u?cp=>4fo(P;}oy?(vA^Q+wYP!HyyJjPR;#Q{4uIE#~zL$o{=9<%1Ag6gu8PILs(W27N8zs`ukQzu_OqrHDO6{)gnLs>r9AfQm{vUDB+!4!W+v5nNAquOrwMs{W9Abf&Zk{G%4rXA>`F&ZKW5wCAx05M{+eej^d_$#NM~|B8^x6EWVU=3(@8{JmM0{*N|`^2*;N22%o>&&ug@t{p9Q&O?Bj!=JVX5<;Ogt<&=o8Gq*Ia&Z7E$pLvfIrJR}Y(-Gy*({}ugTza!Md8>I%F5$+_Tv~!zYfMWVy&Na4%*s{>)6c1vSQpWXTwb(7{BlB`6x(<xiM@3O`P+`p#4~%ujldfuY=j2HQws&cnOwpUSxboQs!=Twz)YyHxP)h|mAv(+X_gg@H_-22_u8YT+rytf8^g8M=-24ylrqgVtF5)U717Hx|0#9GC6bp<m2Ucb8YNB6-m_D&*5p^Iu+sqY<9ByUucl>^8lC5ec~A9qv)0s+OHaF)5?;zB++yWKukUD<p`>;x`|0I(w_<7WvX-wOnCMp~R6g79Gc$%0HyIx3A;bNXEV}ma><YqHr(`>|1j~eeKlV3q^q^nFJ~7#(_1$44lFX9I7p9QJ<fdd_wS8jO$6HA0<!PkP6)Tyw?bm2eYfT{P+6jHa5Huj3S_lxftt&yV8PID+!T})sA(t@3tpss<dLvA4IX%LGyy<=^!CW(7CRCR&=9<kT9AW1XekN<Y=`<kDG^&S>{AiWNKA%YvuFC{l%^<CJPLz6wrRqj6FAuqi%*m@xtWQTt@lDc+TSbaW2fKS6&dNX}3`#iCA_zCxG1m;5YqmAx5-w^uz(?d~o+k1$qrsiZ$t9Q8iOd_J-T{p-_<Lrhz2JG~j0Wp9XMQui8<#MP{Ll(l9^oy`JmV59@)P%Rq;&V1Ooi~1-Fi49Kh%bJzke*rIdY#=zgIeW@!Q8LB0s#igh%A3iiH0R4Tz@}?1W`KT-3~t)vbWFm%4<py44)Q@=X`h+KzQ=a5o*z=HG?Z8l*jpgy9L>Hrg@A0UG%!_`r@eKX5fal(5~7HSmChEyBo)cFfZOW|4FWW1h}5!ooE><~ZPPIyztC0SDH=19ll8VfZcs+eimaKLDJ5V3;sYKk#$<fki0DbzuE4VEr%>h9@l899W?ZSU+r-Fji>$O}N(cT*45OyC5cvg}^khvjs>PlCVWc5K1xE44BQg2t{F~ST6xeI3ceTdqM$wLM_6`iKRGi4U};4=~A3~3D@l<6Mp^MQtYP#BpfCbe9E25*y65u(>)G|GmUy2Y3=fz)>^;xk<tfgNs5-BukA>>LYQg?YOOJkWAxT((){u69)|~Em8OWHm4O9YxP;GznJ;hc94UWEbt_LxFrSXv4x^6uRR~k^pT|s42vgY}yr8eMCg_gkBM9FfcF!Vt>SWq=+k;COf(FD>GpZ#5MVQvW-@~1bJ9FF=ziii4FE;i&mb>m5^UpLIA0Btj6(2r##42?-n5Fb_<aggAemt}#(aYx7{3)sMqkB``;=>*~Se5f|%^%*(ok9aa1LCQ9BTPGG^lE+rM%W?<3%G>E{2bHr!YqaWai-C_HCl<1xi^<Q@s?G}iXTm8U$jcO#Vbiv!!=^@+`ARR7b0d#a~;WK?umM2)`~hh)vc@&MeExk;Xn|6l1q5?9a*N+fH>1A;SN`=QnjO_$>Hl(Y0qO;XI;ebmj^kkrn>g8r4Sx<^K5Bq-@&BCi>*oe@iAh(rDw%9E!wGSFJp*jtwg2ehJ*t^*!DP=@V6VYz0z>~)SlLwFB%)|**^Tle$nn0J0#)Kiq3I%)3M4xwU%JHW_>N;-dUingQxcJOzzyv?qTM8&D{;y!%(rcqBb+7_zOdw_Aa%Dnb)kghnd&R>|t%>$DOFwgQkQ>8zO9k2E<bfcEVH-XL7X!#5)>7^Z27Bc=m80wL}N541fGOK;O{o!PAQrd+Q8o?Gx!Vf+Ov^lBRggRF*rGXDBjE>nKKL#*_WE!^qULO}xmkd!7yn2aYh+679HJA|qq6X<CB5o9Vmy%`YdJX05R^jcSRtmtEG{kj1m5=%XXZdsp(MkJHjMT?VvAX?js2Y1CRE%|2}I^qwP+mWrO%nuiYd&={0(B$qG*4Tz`ajd04;>$=ujpa|2NpD?bLIMO)D^mnwcGXpvOfYq(7F3pmb%^9R<391$L3u837<~<*NBF08_<<zZda&w*@hpdOM$MIzN>a*iakAr>OVw}Gf0?L`J($(zf<&PU&725O8&5~ZcFieT9Q5h|-^QETCKql|3ZjCLrO1tkHrmk)kITeD=pOF&&nM)Xg2E<eIhcHhM2Z}JYCBBa1X^EL}=4akdT7#!v;_#a;TSA?u+uVAB^j_ET8jpik5FV~O%twwxqmP|Aj@P*|Jb1!COqaLc=l#R4x_VaU1F0qQuDEVGb+?x+!_vS0nW2eZZrX6E$HjVy<n8n_@#nWXs3Pz&gqH<n6P_R9%JAi{&9A10IJ2sGy7=AGrCa}-s>twX6Ng9z)5d9JIA%gUae7uCUPX$awIeD&kT5u5*;<Q=Gh(e7v8*60z)J`33TkVO5{`^RuNg2dfrJAPmx$THvnA@Co@{zwb9BTbre=}Uea*Cj%AK&cxtEhacg^{s_U*CX$0)YM?pbT1hi~np*b+3VNqa)$UXCR9yi$w&aNA1p?amL8iKpD7m-@ZUl<-C_;pZGVrW1xZ(`Xi{`gN<cgJhGHzgwlxUd>lL4s~3D5oS|pw0Sy@PFupugd$;R!ZF1>!uQTJUrT&EdU8Msdz*f+pkn#~o3|Eo#wxwjV;Q+JWm(}J-G?h$!uoZr)0SW}w7cv&EPlGOGjW@a%dsIU<7<@gST11*8W2y-s0;^^@H8%Ah+7Hb_SC!S=)4qq)6tsZ=J}2PvYSqSdm2QP1|pgi^pPJ~hArGF<<mQwzjpxQOru(Y&8k`@Ym2Pz^A#CZ&%I<h4tCSg=?F_4|3kEMFV*&NrItX#kc6q0xQV-YYFX2G(>r7#&a7&u4DF1eaS7IStB(Ba*p}&<ELstP*YW9eI=)=7H9p}qi}^Gl&aCR}Rz{e<{<eFtMi0|juGDMxPFPdjii877_%_rMz*^$&63pfU#)oN+gG+eieaWU1UiD~l&{VfF8UE^UlJxxL1Vu{>$etqEQt~t%iyMmCY>(QL;>{lB&HQm@Li=;AwS?^xOrKFXI??-??C;R;_xDVrb1$FR<jUqVpN`eQvtA@N_p+Vk%R<^uM_&(RjBt9-kqhg)&%G4*TYD<4weegThLAUi_eHSFFeN;ROZe7Q^KT`HGmR47b!rwj6H1Ab6Jr&^^mF%$6rE{c+&&~G!$=sK@Ki408{aeU9nI<_A<nF7HebChV)3!bQpV-+8e4)*7A<btr*LDPRHD@qyviyh92mmWxrE<-DaCXe5N8@CY-`}U=_tVur}cMEW2Ai?YAwNTI#!XQC9F4r1_=j-Ftvvt<J!XzReTWDhDNJf163JF3D4&ehVTv`yqFO1IBW~JS|a*u^QX`GI@4`xbPs>eG&<34P4DT>EYhA^COIcOv&fHnq8*#cIOX7)9)CQSNHd{@JL1yZCfcb#+%x+w!plprG7zwj!y?!=aJ5AJxY4F>cKGMRqXW7ZiDr=WDzx`k=;7U$tkOFVj@R8LOt(mUwPK($tEy3JK|23p8u{de`?d&8Rf^($P+Ow31gC+4P6HEmaS3<XIM8$&5N8@Cym`IL<Dgoh#+~uHUNh6fESsNjy}fgLnrgzcz^~AD*~5nn-E>B7C5YQI1a3N^9Ay|#hUrar5$$0>dzccgZpUsf*lw>{++DYqlM+qeJK*cgKx&Eq_M7FLk)obIOzq>&5xJUdKCKwsSFOLEmf$^QMmWY8VIwpko?5UIZXy$|%heM7Zq7H|J1E}ykD#erYhSS!>Gs%RQhvvQ$`l&5k3(JEDr<>tB&jk_S6M&I^EN7fuTL0)2E<bfdcyKecMF#=gog{^iF+eV>FN;<l-EpWw>Gk49|vHUfvhE3*|8T1uonpl!xI+T+i{W-;H)Z{a3?#)hXHRoi%`TTy!D{@yOp<o@u;a&8P$Z{yS?bwyiF-D|J|h}*iFac5?yNDFU>2?Qf|6SJ4Q&gZcL!DwQc)fN_OsZ?mJ?sxcJ}hTire5X=;1;emhRbg`0axtu;R3g^tOl>tTp9jq2f7DsDQq>-PLxv!$(dr)u=DvUB{<=IG44c(V43Hrr~YCv$p{)O20skuW%6ixATb;}Wo5vkqa5OPCh<De7a#*{!hlaHbunAHc>Xvg|me9MD>m^>8lV;{fmuAiNl(^Cbf4aR_;K+}Z=UwFe2q??tjrv}4C2V7-KV(@nMG1P{O&DM%Qeu#Ha`cYB$%+Y1Q?U_afXcI-uh?M1R-y##E%M9amPMS}I|3O+%v8IW+K>~R#@v2z@*bDa8gM=*;7n?*vx(3#Mfuk1J-7jO=Im@x8NJ5JgMoIh+4%A*`OGZ1cOpsa@{J?P-c@XT>jO!vRmJu~Gm@#%OnJnot+*UYj=%;R9uOD4lqw&{dtngOlzQ)5!|r=-G<?oCzsbRNBQo_)<0;qG22!>}?eJj|702zi5eUwD&YZ$4cBWjLXa1E=ExPRB*Uz=Y{dm*~Jfp@5rMWj#E~fxB)2H?dlTve6EldkHxA5(&c-Zux`*=llT9`H^LK9ukHnoba{-ryl^$m#_%yHaT#cFz7a6Bn(ZsV6y|K(12=*mRlW|2?d;?Z4tJ7=D>MtfHMPSYwa)+h9$hLZ7EJ=1f0rf5gsC?I0qhZ(moP~C%i796sMGfYKienN^yG{;N~fdaNwm<-0cNQxWSrI+=vag5nCo)xSmTGf(FD>3jxBVhq;8$g$@4GTEg`;eZuV=DSyeHP?`zV^P1_+HtKj^g)og9e;zYIA)Nhrb%}N?Qm^`s<s*C$)>fv-gxh|>B@96W;;B_NE)f921(&&myBnb4>mBXu%s}elqBb*~u{BDN5~i<Fy9a0pGcCag>r_>7qCbk3XnEBTVIwpko?6fo4i|*QJ$ZzibTdCM3~{DW!Yn>awME!B!xfLCXRC*$*A8X>iJBj^c2Gs&kuWr2i(p%XgpqIv6Q*6a9eVQW)=oy|`5UG2yKc?bnez8(dZnRj;D=wZN;e5PB$CXM-k6^4oNjQsRdY@KFzX!urde01ey?;d^~0WChjGG2Xh1x*peHQfbSEC*5&k7P)AU}XH)do8%^dh+71O{jy)wWV`Jt0KdWWTI`suoVX_aozAEiw2(9ZdZA^cvtifLdn;iFu_5Huj3+Mk^-!Sr#!2wMbUKguvL;aw=hu!L=!xrDDJW|%%P2I5SkQ)qsyxarQyqz4~e;+%5O_Pb;aVf7Rm?^79FKbNYH0|~<tmT$U`kT4PsWx`>C?G-NJd+wd&)jL?<dz9$%WaIqy4t$*%NRMNB#r)wuG1<<3Iy#eT^urmNxtDbE^H*b%6vFzms(72RUGvtA5jH{t;;98YVY=0Q*#o@D&!^iHO^?7soM|-jb8U;OpH5vr{LQg0(ypW|CGtaSfoSJ=jm~q#_xs24DztU`kesnKBn(ejSi~i~BGdfp5r{L567Dp?vu=%5q|ofX<G~zF7HM1az1urPr25DrdDg!p;Xn|kUh_ikO;>Vloar7e#F<8|H8!hi!?qdHo7d8PT5I&{o8NEfWrjBI7ZMHt;c&q=9|<Gj5GG8mwYl7zZsA$;y9*)CG<wrHj<~9-n6*Z$Sn0eqr*-y7u4a;wmySi9-sVa@oXM5p15&Q(^7g_z<AWwX%(g{LPt2Ecz8&J+9TOGyg!B7)&q&bhlqra4KtA}jnj*u=r>*2r$LsDBX!zSA!jUjAVOfSpa0x@ufOu-&2z#5#7)TjL!q76@mrJ-w^(m&)fH>2rEitGfwl?-VS8sm8dfB$P?Mdgvx)0KZYG!D&?P>h@Ft3lp6(^=LjD$f6qYR@Ahd5yxTYG@(aWr@=!OwbiejmsA#4Q>ccjhF3cFItyzB~^0%BC{1-hA3uM|T;h=S$F;DRdgx{@P(=>e(iW$1(eu-t1P-I2$D#%_W>yW`4I9#F<s?SftgflrW24s%NCIjzt>9oN{2ew<$FIjzuIK0K)fi3D^G4{1^hnnPzo+vABdf0?%d!>c=JYC(t0_KoF+ZT3fCyaq9RO)9-zVGmY93tTK@89A~=>)X~enL#)yWYpNGpBF5uq;%pN}!mxy8d$<h}M#3SkC2r*sj)^rt4hC_iQNnDiJKKxId^$B@wgFI|ut0P=ZV3_&2w_=EG(^HkID`pD%330V>v5D_9B8_C;Ok7N87bcOaj;x7jR3vSEm1RXjZUSZ8?pC%_=y-B)m5)DkZ5zwmA&~$7?LpUx~<LC5<Q=sXnKV<#F<7bw8e_}Fw+t&Pp96;LHBgf&T&?u-MoFORDX54Y9EI?Rre@R3_-%sglXib23Jc=9%6naD#V#pt!`CUXww>>3-9D;BJgaYo%fm_Z4@2}LldT2;^#P?mMD92s_A=?e4W{1UashFl|gC=sukS#A~CNyTl`3@5qSquYl*0aYYNXF8%Fq@GJFkD(Tik|un`&%Pc7I9Q!Q~Ij;AHow>Ezo7{r-IwM5USJv(LCG%$7TC7ZO*w1oT`z2RyS(Vxobp)Cj!4g}#XaacbLSU)WLbRTf_@aaR@rpFK<&NLdAcxtmthG~UhdEM1YPpCRB!RGuVCO0Mfs_hf&Ej=r?Y0=JotGnRY&m7~iqXP*;6Q){XJXcH9c;0;5)&DcsfX{Aa_Are*P@j&~OQ`3qu{rQw>|s?8ooAel5^fZPgahYsP@<oGI>6~!4C$HdtWbIG-7yMb8WEz_ns>tLDKwRlAS4V;m}Zg6cc2~yyy=i|0B*YS9aYm3{@+T$s3ih%({(Jy90y>IL$-$(74x*jvmcpXJ<_LNmZ_7Js-h*%RAfTOXGA-vA3RszwHHaPCDxp`O4ZWGl7o4-kVdcmB>r&QO7ZQ^50NGwnNVJ3Yo(T0#g$=O`y|ul&DWWM)Dm<*DBZ`gb(Jf&Mr$xT&q>hi31wQsiwvtfyofpiZ;Y@J8W2w{6bQd(NDmvK0ioMNA=kW>tA}s;m-*ErFP+W}x?ZHKQ?d&eZs<*{U&l%X4<(UxFO`d3``6O+gr50Nskr>|-@R0%XyjMvMJndX@T~XEkL5y~X;g-Hotov0UebL>lrZZ>(%TbCt+)-RMtjo|f{HE@4jADhT*BwC_A`AiEyS5dcipm`GISqZbWw_O)9LM4To=)bTwb(7l)o;;JGi@Ui8kNt%5flJNW#?P_?3Ipfp`ZW1+E7EhwCGqHyx$kJiqZ@=5bKMzi|owbKnHiX+WG=)h+{OOR#Ldda|hSnN_-WVYo6$i4*xDT3gsNi-d$h30q{_y95a%;m{>aZHYQ1JX-={QUSz7g{peZ(9;j79)5r;!+%?5em(-?%&L0LvBg&D*zaSUeRKAAZ5msG?&+X$3AT^p%%K;>i%om0a~x{VS+U%ZFgRgZOAO=^UjEJ`(`i7QX;$P%Z|)_{-_3O-D|$Gp(^zTPPw9lS%Ru1l3?)bynlQcThH`JZx5CV?;#<)+cq#+$U*%bQ$>PK6dI@!9AZK5*&&i@gOK=|t;64t+gmE8--}^X(j1t_$3b^YQ2?v01CYSKZZRXYIP!g2LNFQhZnXT^ZOrwNt4Lr9+(Aswzy*zq3PFk6zt@+uM|B6_Y)PqJbrTZOeM4RKViF#cI*<8ZsK1np4FvOWg2@kvEionO-Iz!rZB~7s<^awkCXhu@c6pAwG!WRlty%5&sIFK+j;ao1^xc27H_dB1J5_Fw1Y-S*<AEsF)TS}g0rwr|+Nxxwz&mI=M%?zYI-NX`{qy#ug2?+;)@T3x)LIXJG2MGsY8rW1WVTc+th*~&3!u0oy@RDIS|7CS+Gy;!=p(_Jta;-H8%L>8*40dacZl1F7?coCnrh5kvXBs8E=$F|}ubEW_vKcAr&T+OUl*J`<yk^47f>wAONEn>(<6OcJ`3Q)-$)6?6UIUrqc%lSr-~nw3i(s3F*?h=sJ`x5dO!e^7Ts;gCEr*Ee8`Z-BjKJHLatU`jX#Twqab{I*3H3xfN_<{%maZ+4aJ{`0-z1&rZ;NpMh(W^OgsCm@ObPZi!*&_0Mr#eyS_>0|S4(gsHsH>2Bpd+3ub1GCMZhhVNEm(-tL^O)>{tY}C1iWJ409Z?wuJ2u?Dm4}r$fT<{d6&co#!>b)^MQdee}N0WF9i>r-SUxPivPiU8$GmjP%f{jLd7+o3}<^Gj^pB<~4JA^HtFwr9#^vVIwpko?0jn4(AfSVv9GO2E>_03A1g&tS6L`rZ=5>Ru!FIK6pW2(q-3Sv3Sm1I)wGNu_9q;!qnraY3JQ^o3@#6SzX#1JdvOGDy+4#U#(KxsS`-d8LRY8k7c@(MOls`x#iMmX?c>)WKm5GG0`UsK?CBcg#ck&Z7$(ok~2-G@y3kIfD)z=cwg4qrB?<>&tFb(=Hq&YrD_Ow|I#Ymo<B+<%&%@$XOKL085G@!S^`prbqS-EFi#KH;}RaX@e$K$G-^8~XtV^253|@B%jR#|aB15YOOq9!PJVSx@L)dOADvGW?ubiM5mry}aO=&t2(}2+5|A>iOBl6;X<DL)Pk8SE^P)5?^S*J#MAOgoMwoVv`_dAu%i#Q5v!$(dr)mh(s3zS!HTOh4GHXR0GOXDn(v`TOq(PZF0?(^RaqbDVHQ*9Hn3!ui4Tv+n5l)$UT~~&W{AiWNKA-8c7m1Q@S9^#;c%EaXbav%X!pU)P>VA-LKnM$s?N}KIJ4p!%L)Tt5=f>7<JC|sB91P;js>ar6>}=HWzRp_r1B+9fpLZzF(8PzgHQ&3vLqsacIdY#=zZWk)tm&syYA=y6Bw^WWwzak6BqhK}N`?vJBqjf6RYhT30x~WUj)Z{;%QsyIE@21{7s3<&v(_5B@dD;GTZEX7cAR?&I9W6t2?G;G8Acfn{rSVTJGq1*^1=}LYoj+^z;exDLXl|4ZZFsh?Veo1FT69}bixOuz-E!ke!fvR$3eFUXYS1<(-ZThoNtFXE3u=(o^XC&?->c23hjc32IPZZt0^*^eA-G5b-XURbrkUSEjs%+`f~~QPcYv*@O7r^?|N>FfYQU6-?}33jBq5GCA~2{o1E)ghujb`S&?Dc4wkA<>qnmZ(IP!{Y9uFmsp$uGlWSLecz_|oMrc4hwGbd|8^k62(aQ0r`(F@e8qFfDy)5h3qoYZU@2%3dd&enySWTGqBBeHLO#7O}u8+5n(#zew<`}}e;oR%ikT57=iy)+M2}49_AficC?FkJ;Yz+wm$JT^YJ9aFB+QT}8QHITn4-e%MhVTv`ycnZibHF?fi(nhaC0zF8R3CX^R}Og9i;exxsrfpy#k^e6og`$Qj*_Dj?dF}ECB1lIm{RkTEq)}{h`d7~+%u<xb6Z4I!!?EHj}0UIJe^16ow(=jj1x9O1LCO#J>f7RW(k+@wZsflZ#qf@;!LA@_{VEjsb;+_a#q$BgO4upIl+VFn)%ZY+;6)WkADjZgA)!Hiq@eXhSU;<38NnNo3QO;j7vbqC6F+D<Y(j-B#eYZTT8?ga|z$^z4;YTMPK-PCO>a7qrsh~6J}LadVL(sYi5L-zTv8>ns|zr%~#)gF<uBm(13VqK~FeLu-UnUPaiVB=K|tPqaMdon_bo#jR2L`U9Hp)>vb$9CO0Mfs_hdwlavHcPs3AdAYpLA7NMXNdqN?rTf>ExpCMu3`r(~;(?Q;JvX<D1)*39~qFvZ!0IP?QFeu?jS%&v<dqN?$L_ut`GP*4yP@AVB!;vuXZm%$*-~ieZuyG0DAWraroZx|k;b){29YlK=)*dcH83vVMBn+>Ii_T!D3}hdNVZzuc<0oO+r~3hAI4B9D4Esk|_L^gUvExQ;z_^4(upwb!!gohFc!bL?4)jXneBu_3ci@YLuQLM~`3c)$l`bV_Xb69GI7uQW#wvt2x1Qjf8Mx=ePsG@$uB7428#sgo&gK)>hpZ(Enj&FX!sVT~gl+AUOegH?%s>*3-#uMg`$Rg~y2@4E8uxOf)Ok*VX5$H)8R&(ux;w^Wnul@1Mrc4hwV)>~>)|_5hJ%tY%CLWgY2;^+gXeMdd~%}cb1xyzG}>h#R!mZ2(M#5`D0>#9yv~=Ry32rd$~14ED%D?|?$%{s^V(^Eguw}i3zL$OFcJ=JEn&;#5<VH3XF3gEXUg9vx@U_Z36HDjSR8)AD%~XHD3PCD^Y@FVTQw)@>Q+Yhn`T{|GqgRsz1$-{+MP1S2pgdR@zjEzaJVpXG|F&L5=I&Jk1(xUdxYz8)ObGGbdLk#Orsu0rwOiI26THc-6l*ujUhdgHPK5N5u!KUhN3pxqxPiecpRFlK;jnpLBg<vQHD{5L!Yo<<q|%BwV&zxUm(sjx>Kg8%}go&!ca0Gdx{iYl%hm_=<D5UGBuH(brG$|<wYw*`Rh`=gS*w8sH5-Bn+^#>6SfE~kuVYtb;66dgs<4*O{W2IW>t54(VMKso$=)8<v6L}p(ITNp6>b@yr3`Xvg@!|Jm)TwaJ{`0-$YGVJ@ufnb4J#~NEntd$}q}s=*#fN5(n;B1l(d7j)Z{;qYR@AhrSFq+Q}t+XHJ6Y)guia^M2;~-lx5uDgT?MR|c}1j#dN?e|ZpDd~C9mae2H#nBIJJhW7s2VPxvrCQ9UI_AwUuQP0oTR0bkpSi%-z+Rh-1URDxzQHP6O(&|;3&7XELSNd)DU}rS*wL{q&E#W<S$uxs@s+}yuNEnu|MR;g8m++_C6HO-!ai&qi*S2_e8PL}uHT#ioj&+fCC1ojux7fxxy9{b{o+G~BKUS|oTYba1*AF9MSi&g7D8r#I!yEa8AuKBh3(%b~rRs0DR{-r{Bn)j2+xAw`TJzts3dU@H0PJBT3~dh=?Bf#dbTGj*8f@AI#F<73FZyM+ld$@xd$L;(X<o7RrjxY^okA1MBJh=jHIvB&_n#37gA)!HmhDHvNI0~$gm9Qkxb}DEPbz>o(<tG_&1Op($-|u$C^Q29-N(b6la%_UkCYq_<|u@z6-TW#HvK?*)9GhHS!Ey+1|^I#j4~YhGCbrMm+)&12b!L>^mQhq$-EfIOlVrWeCbNPG-o9Wt<YvSou0=*Uo&>4=~Ses=~j9mvJ4|(Si**7*a!`Xr}qC>hLNz}GJNm9xrEPsl4!bj0CA?#n{L=8SB17rO4@ZLO_`)biLcDk5_bI1jHI3^6gTC+Qusn)D$z!M_}kNvFgW3GVbXCVjD$m5OC<cpB^-Ca{3s2?nN^MablbYPaN&mD%1!5t^gNQQ8~HhycZ+ntBTY?Mw?a@RJP8Sd5)KzOB4J>{2aqtZmI$v?$|HPoTe9giM*29jvO<7==GsZyO(Se;;L3#3i2H}r`a4O|ZNhptoqWTIMM*t~4q<`6dCDon2}l@}uthj=GnX&~4Tz^^bi#80Ww>7hBn&IVHa_9?tp}SPEr&SMsFvvYv}a`??U0GuJwS8Q(I-GR0J4e{`89gO)g+>w;K6%E!T}&GTWgJwFcJ=JEitntm+<5v=2!7SoLSY%Ky^h5?OeR@PL8I!)k|d{;gEH&fk(oygi(f3hC^S5V-mQ8<JzZ~PUC!5O3)B?9C1~o&<S?5%YaR^qmz|vDR~Ov_ZAd8CyUaGmGm2i^0xK}{7sgM3?pG!!WLogKrZ2hXU(sGf;h9PgqfCLRaI(hO}%-_yO!X}FcO9(Y!N1<B4Jn=M#9iC{L(NkVTfA^;`R&yTLK9~+Y$+jxrA3_n(rMzoLN<mgGJz3$D+DIn-OM{l=v0e+6<_h3?pG!!YIQi!=X>Oz|JL{S7!dL1aYQO!fc`)yXhF=)umZd=ZH#cjoxrH6G}->IWXMIq<vjm0tv$swg~HxFcJ=NEm3}wOL*4%=4UM-&NNDR*Qr@fkAqbPvMDs`jo7Rrg?7+vI5pba1P?()n^ef~Z%7!FaJc+`LBg;yTo(yL68=AEaFGl'


# ---- embedded conservative KNN market residual ----
import base64 as _res_b64
import math as _res_math
import struct as _res_struct
import zlib as _res_zlib

_RES_ALLOWED_DAYS = (16, 27)
_RES_K = 5
_RES_BETA = 0.5
_RES_THRESHOLD = 150.0
_RES_PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
_RES_CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
_RES_ANIMALS = ("GOOSE", "COW", "SHEEP")
_RES_SHOPS = ("BAKERY", "BRUNCH_SPOT", "FARMERS_MARKET", "ICE_CREAM_SHOP", "PET_CAFE", "PIZZA_SHOP", "SMOOTHIE_SHOP", "YARN_STORE")
_RES_BASE_PRICE = {"WHEAT":25.0,"CARROT":35.0,"TOMATO":60.0,"STRAWBERRY":120.0,"MELON":250.0,"EGG":50.0,"MILK":160.0,"WOOL":200.0,"FERTILIZER":100.0}

def _res_get(obj, key, default=None):
    return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)

def _res_num(value, default=0.0):
    try: return float(value)
    except (TypeError, ValueError): return default

def _res_seat(obs):
    return max(0, min(1, int(_res_num(_res_get(obs, "player", 0)))))

def _res_counts(farm):
    keys = ("EMPTY", "LOCKED", "WEED", "COOP", "PASTURE") + _RES_CROPS + _RES_ANIMALS
    counts = dict.fromkeys(keys, 0)
    for row in list(_res_get(farm, "tiles", []) or []):
        for tile in list(row or []):
            if tile is None: counts["EMPTY"] += 1
            elif tile == "LOCKED": counts["LOCKED"] += 1
            elif isinstance(tile, dict):
                kind = str(tile.get("kind", ""))
                if kind == "PLANT" and str(tile.get("crop", "")) in counts:
                    counts[str(tile.get("crop"))] += 1
                elif kind in counts: counts[kind] += 1
                animal = str(tile.get("animal", ""))
                if animal in counts: counts[animal] += 1
    return counts

def _res_farm_features(farm):
    counts = _res_counts(farm)
    hands = list(_res_get(farm, "hands", []) or [])
    farmer = list(_res_get(farm, "farmer", [4,4]) or [4,4])
    positions = [farmer] + hands
    xs = [_res_num(p[0]) for p in positions if len(p) >= 2]
    ys = [_res_num(p[1]) for p in positions if len(p) >= 2]
    out = [_res_math.log1p(max(0.0,_res_num(_res_get(farm,"money",0))))/12.0,
           len(hands)/16.0, _res_num(_res_get(farm,"hires_today",0))/16.0,
           len(list(_res_get(farm,"unlocked_quadrants",[]) or []))/4.0,
           _res_num(farmer[0] if len(farmer)>0 else 4)/9.0,
           _res_num(farmer[1] if len(farmer)>1 else 4)/9.0,
           (sum(xs)/max(1,len(xs)))/9.0, (sum(ys)/max(1,len(ys)))/9.0]
    for key in ("EMPTY","LOCKED","WEED","COOP","PASTURE") + _RES_CROPS + _RES_ANIMALS:
        out.append(counts[key]/100.0)
    return out

def _res_signature(obs):
    player = _res_seat(obs)
    farms = list(_res_get(obs,"farms",[]) or [])
    farms += [{}] * max(0, 2-len(farms))
    step = max(0.0,_res_num(_res_get(obs,"step",0)))
    hour = max(0.0,_res_num(_res_get(obs,"hour",step%24)))
    out = [step/719.0, _res_num(_res_get(obs,"day",step//24))/29.0, hour/23.0,
           _res_math.sin(2*_res_math.pi*hour/24), _res_math.cos(2*_res_math.pi*hour/24)]
    out.extend(_res_farm_features(farms[player])); out.extend(_res_farm_features(farms[1-player]))
    private = _res_get(obs,"private",{}) or {}; shed = _res_get(private,"shed",{}) or {}; seeds = _res_get(private,"seeds",{}) or {}
    for item in _RES_PRODUCTS: out.append(_res_math.log1p(max(0.0,_res_num(_res_get(shed,item,0))))/5.0)
    for crop in _RES_CROPS: out.append(_res_math.log1p(max(0.0,_res_num(_res_get(seeds,crop,0))))/4.0)
    market = _res_get(obs,"market",{}) or {}; inventory = _res_get(market,"inventory",{}) or {}; prices = _res_get(market,"prices",{}) or {}
    for item in _RES_PRODUCTS:
        out.append(_res_math.tanh((_res_num(_res_get(inventory,item,10000))-10000.0)/100.0))
        out.append(_res_math.log1p(max(0.0,_res_num(_res_get(prices,item,0))))/_res_math.log1p(_RES_BASE_PRICE[item]*3.0))
    active = list(_res_get(_res_get(obs,"town",{}) or {},"unlocked_shops",[]) or [])
    for shop in _RES_SHOPS: out.append(min(4,active.count(shop))/4.0)
    return out

def _res_decode():
    raw = _res_zlib.decompress(_res_b64.b85decode(_RES_DATA))
    n, dim = _res_struct.unpack_from("<IH", raw, 0); offset = 6; pools = {}
    record = _res_struct.Struct("<BBf" + "f"*dim)
    for _ in range(n):
        values = record.unpack_from(raw, offset); offset += record.size
        pools.setdefault((values[0],values[1]),[]).append((values[3:],values[2]))
    return pools

_RES_POOLS = _res_decode(); _RES_STATE = {0:{"used":False},1:{"used":False}}

def _res_allowed(obs):
    active = _res_get(_res_get(obs,"town",{}) or {},"unlocked_shops",None)
    return isinstance(active,(list,tuple)) and len(active)>=2 and not (str(active[0])=="BAKERY" and str(active[1])=="BAKERY")

def _res_score(features, day, mode):
    pool = _RES_POOLS.get((day,mode),())
    if len(pool) < _RES_K: return float("-inf")
    dim = len(features); means = [sum(row[0][i] for row in pool)/len(pool) for i in range(dim)]
    scales = []
    for i in range(dim):
        variance = sum((row[0][i]-means[i])**2 for row in pool)/len(pool)
        scales.append(_res_math.sqrt(variance) if variance >= 1e-12 else 1.0)
    ranked = sorted(pool, key=lambda row: sum(((row[0][i]-features[i])/scales[i])**2 for i in range(dim))/dim)[:_RES_K]
    values = [row[1] for row in ranked]; mean = sum(values)/len(values)
    variance = sum((v-mean)**2 for v in values)/(len(values)-1)
    return mean - _RES_BETA*_res_math.sqrt(variance/len(values))

def _res_apply(action, obs, mode):
    import copy as _res_copy
    if mode == 0: return _res_copy.deepcopy(action)
    out = _res_copy.deepcopy(action); orders = [list(x) for x in out.get("market",[]) or []]
    non = [x for x in orders if not x or x[0] != "SELL"]; sells = [x for x in orders if x and x[0] == "SELL"]
    shed = dict(_res_get(_res_get(obs,"private",{}) or {},"shed",{}) or {})
    if mode == 1: rewritten = non
    elif mode == 2: rewritten = non + [["SELL",str(x[1]),max(1,int(x[2])//2)] for x in sells if len(x)>=3 and int(x[2] or 0)>1]
    elif mode == 3: rewritten = non + [["SELL",str(x[1]),max(0,int(shed.get(str(x[1]),0) or 0))] for x in sells if len(x)>=3 and int(shed.get(str(x[1]),0) or 0)>0]
    else:
        rewritten = list(non); sold = set()
        for x in sells:
            if len(x)<3: continue
            item = str(x[1]); amount = max(0,int(shed.get(item,0) or 0))
            if amount and len(rewritten)<10: rewritten.append(["SELL",item,amount]); sold.add(item)
        prices = dict(_res_get(_res_get(obs,"market",{}) or {},"prices",{}) or {})
        omitted = sorted(((max(0,int(shed.get(item,0) or 0))*_res_num(prices.get(item,0)),item) for item in _RES_PRODUCTS if item not in sold and int(shed.get(item,0) or 0)>0),reverse=True)
        for _,item in omitted:
            if len(rewritten)>=10: break
            rewritten.append(["SELL",item,max(0,int(shed.get(item,0) or 0))])
    out["market"] = rewritten[:10]; return out

def agent(obs, config=None):
    step = max(0,int(_res_get(obs,"step",0) or 0)); player = _res_seat(obs)
    if step == 0: _RES_STATE[player] = {"used":False}
    baseline = _baseline_agent(obs, config); mode = 0
    if step%24 == 0 and step//24 in _RES_ALLOWED_DAYS and not _RES_STATE[player]["used"] and _res_allowed(obs):
        features = _res_signature(obs); scored = [(_res_score(features,step//24,m),m) for m in range(1,5)]
        score, proposal = max(scored)
        if score > _RES_THRESHOLD: mode = proposal; _RES_STATE[player]["used"] = True
    action = _res_apply(baseline,obs,mode)
    try:
        _META_STATE[player]["prev_action"] = copy.deepcopy(action)
        _ACTION_CACHE[player]["action"] = copy.deepcopy(action)
    except Exception: pass
    return action
