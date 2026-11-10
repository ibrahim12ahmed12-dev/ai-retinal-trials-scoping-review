"""Figures 2, 3. Writes PNG (300 dpi) and PDF to outputs/figures/."""
import json,re,collections,statistics as st,numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap,BoundaryNorm
from pathlib import Path
HERE=Path(__file__).resolve().parent
d=json.load(open(HERE/'data'/'extraction_and_ratings.json')); R=d['rows']; A=d['ratings']; RC=json.load(open(HERE/'outputs'/'study_coding.json'))
(HERE/'outputs'/'figures').mkdir(parents=True,exist_ok=True)
OUT=str(HERE/'outputs'/'figures')+'/'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#8a8984','xtick.color':'#52514e','ytick.color':'#0b0b0b','axes.titlesize':9,'axes.titleweight':'bold','axes.titlelocation':'left'})
TXT2='#52514e'; YES,PAR,NO='#1f5fa8','#8fb6e6','#dddcd8'
funcs=['Diagnosis and referral','Endpoint measurement','Biomarker quantification','Response prediction']
plt.rcParams.update({'axes.titleweight':'normal','axes.titlesize':8.5})
TXT2='#52514e'; YES,PAR,NO='#1f5fa8','#8fb6e6','#dddcd8'
funcs=['Diagnosis and referral','Endpoint measurement','Biomarker quantification','Response prediction']
year={k:int(re.search(r'(20\d\d)',R[k]['study']).group(1)) for k in R}
def panel(fig,ax,letter,title,dx=0.0):
    # bold panel letter and a plain title, both aligned to the left edge of the panel's label area
    bb=ax.get_position(); x=0.02+dx
    fig.text(x,bb.y1+0.035,letter,fontsize=11,fontweight='bold',va='bottom')
    fig.text(x+0.03,bb.y1+0.037,title,fontsize=8.5,va='bottom')

# ---------------- Fig 2: what the AI did, when, and where the studies came from
TIM=[('Prospective, changed trial conduct','#c4421a'),('Prospective, did not change trial conduct','#f2a07b'),('Retrospective, post hoc analysis','#2a78d6')]
def tim(k):
    if RC[k]['timing'].startswith('Prosp'): return 0 if RC[k]['influenced_trial_conduct']=='Yes' else 1
    return 2
fig=plt.figure(figsize=(7.2,7.0))
gs=fig.add_gridspec(3,1,height_ratios=[1.0,0.9,0.75],hspace=0.85,left=0.30,right=0.95,top=0.88,bottom=0.07)
# a: function, stacked by timing
ax=fig.add_subplot(gs[0])
for i,f in enumerate(funcs):
    left=0
    for j,(lab,c) in enumerate(TIM):
        v=sum(1 for k in R if RC[k]['function']==f and tim(k)==j)
        if v: ax.barh(i,v,left=left,color=c,height=0.62,edgecolor='white',lw=1)
        left+=v
    ax.text(left+0.25,i,str(left),va='center',fontsize=8)
ax.set_yticks(range(4)); ax.set_yticklabels(funcs); ax.set_ylim(3.6,-0.6); ax.set_xlim(0,14)
ax.set_xlabel('Number of studies'); ax.tick_params(axis='y',length=0)
ax.legend(handles=[Patch(color=c,label=l) for l,c in TIM],loc='lower left',bbox_to_anchor=(-0.40,1.03),ncol=3,frameon=False,fontsize=7,columnspacing=1.2,handlelength=1.2)
# b: publication year
ax2=fig.add_subplot(gs[1]); yrs=list(range(2018,2026)); v=[sum(year[k]==y for k in R) for y in yrs]
ax2.bar(yrs,v,color='#6b7785',width=0.65)
for y,n in zip(yrs,v): ax2.text(y,n+0.15,str(n),ha='center',fontsize=7.5)
ax2.set_xticks(yrs); ax2.set_ylabel('Number of studies'); ax2.set_ylim(0,8.5); ax2.set_yticks([0,2,4,6,8])
# c: programs with more than one study
prog={'HARBOR':['1','15','23','32','33'],'FILLY':['16','17','20','25','35'],'OAKS/DERBY':['5','8'],'HAWK/HARRIER':['9','18']}
ax3=fig.add_subplot(gs[2]); names=list(prog)
for i,p in enumerate(names):
    ax3.barh(i,len(prog[p]),color='#6b7785',height=0.6); ax3.text(len(prog[p])+0.1,i,str(len(prog[p])),va='center',fontsize=8)
ax3.set_yticks(range(len(names))); ax3.set_yticklabels(names); ax3.set_ylim(len(names)-0.5,-0.5); ax3.set_xlim(0,6)
ax3.set_xlabel('Number of included studies'); ax3.tick_params(axis='y',length=0)
fig.canvas.draw()
panel(fig,ax,'a','AI function, by when the AI was applied (n = 36 studies)'); fig.texts[-1].set_y(fig.texts[-1].get_position()[1]+0.035); fig.texts[-2].set_y(fig.texts[-2].get_position()[1]+0.035)
panel(fig,ax2,'b','Included studies by publication year')
panel(fig,ax3,'c','Trial programs contributing more than one study')
for e in ['png','pdf']: fig.savefig(OUT+f'Fig2_ai_use.{e}',dpi=300)

# ---------------- Fig 3: reporting completeness by study type
val={'Yes':1,'Partial':.5,'No':0}
Mst=[k for k in RC if RC[k]['appraisal_group']=='AI measurement study']
dims=[('Reproducibility',[('AI-5-i','Algorithm name and version'),('AI-4b','Place of AI in the analysis pipeline'),('AI-25','Access to code or model')]),
 ('Measurement validity',[('MV','Accuracy or agreement on trial images'),('AI-19','Error analysis'),('AI-5-iv','Human review or correction of outputs')]),
 ('Transportability',[('AI-4a-ii','Image eligibility criteria'),('AI-5-iii','Handling of poor-quality images'),('AI-5-ii','Image acquisition and device')]),
 ('Output',[('AI-5-v','Definition of AI outputs')])]
fig=plt.figure(figsize=(7.2,9.6))
gs=fig.add_gridspec(3,1,height_ratios=[1.75,0.95,0.42],hspace=0.68,left=0.37,right=0.90,top=0.93,bottom=0.05)
ax=fig.add_subplot(gs[0]); y=0; yt=[]; yl=[]; heads=[]
for dname,its in dims:
    heads.append((dname,y)); y+=1.0          # a full row for the group heading
    for it,lab in its:
        n=len(Mst)
        if it=='MV':
            yv=sum(RC[k]['measurement_validation'].startswith(('Accuracy','Agreement')) for k in Mst); p=sum(RC[k]['measurement_validation'].startswith('Outputs corrected') for k in Mst)
        else:
            rs=[A[k]['ai_items'][it]['r'] for k in Mst]; yv,p=rs.count('Yes'),rs.count('Partial')
        nn=n-yv-p
        ax.barh(y,yv/n,color=YES,height=0.62,edgecolor='white'); ax.barh(y,p/n,left=yv/n,color=PAR,height=0.62,edgecolor='white'); ax.barh(y,nn/n,left=(yv+p)/n,color=NO,height=0.62,edgecolor='white')
        ax.text(1.02,y,f'{yv}/{n}',va='center',fontsize=7.5,color=TXT2); yt.append(y); yl.append(lab); y+=1
    y+=0.5                                     # gap before the next group
for dname,y0 in heads: ax.text(-0.02,y0+0.1,dname,ha='right',va='center',fontsize=8,fontweight='bold',transform=ax.get_yaxis_transform())
ax.set_yticks(yt); ax.set_yticklabels(yl); ax.tick_params(axis='y',length=0); ax.set_ylim(y-0.4,-0.8); ax.set_xlim(0,1)
ax.set_xticks([0,.5,1]); ax.set_xticklabels(['0%','50%','100%']); ax.set_xlabel('Share of studies')
ax.text(1.02,-0.6,'Fully\nreported',fontsize=7,color=TXT2,va='center')
ax.legend(handles=[Patch(color=YES,label='Reported'),Patch(color=PAR,label='Partially reported*'),Patch(color=NO,label='Not reported')],loc='upper left',bbox_to_anchor=(-0.55,-0.09),ncol=3,frameon=False,fontsize=7.2)
TR=sorted([k for k in RC if RC[k]['appraisal_group'].startswith('Prediction')],key=int)
secs=[('Title and abstract',['1','2']),('Introduction',['3a','3b','3c','4']),('Methods',['5a','5b','6a','6b','6c','7','8a','8b','8c','9a','9b','9c','10','11','12a','12b','12c','12d','12e','12f','12g','13','14','15','16','17']),('Open science',['18a','18b','18c','18d','18e','18f']),('Patient and public involvement',['19']),('Results',['20a','20b','20c','21','22','23a','23b','24']),('Discussion',['25','26','27a','27b','27c'])]
bx=fig.add_subplot(gs[1])
for i,(s,its) in enumerate(secs):
    rs=[A[k]['full_items'][it]['r'] for k in TR for it in its]; rs=[r for r in rs if r in val]; n=len(rs)
    a,b,c=rs.count('Yes')/n,rs.count('Partial')/n,rs.count('No')/n
    bx.barh(i,a,color=YES,height=0.62,edgecolor='white'); bx.barh(i,b,left=a,color=PAR,height=0.62,edgecolor='white'); bx.barh(i,c,left=a+b,color=NO,height=0.62,edgecolor='white')
    bx.text(1.02,i,f'{len(its)} item'+('s' if len(its)>1 else ''),va='center',fontsize=7.5,color=TXT2)
bx.set_yticks(range(len(secs))); bx.set_yticklabels([s for s,_ in secs]); bx.tick_params(axis='y',length=0); bx.set_ylim(len(secs)-0.5,-0.5); bx.set_xlim(0,1)
bx.set_xticks([0,.5,1]); bx.set_xticklabels(['0%','50%','100%']); bx.set_xlabel('Share of applicable item ratings')
adh=[100*sum(val[x['r']] for x in A[k]['full_items'].values() if x['r'] in val)/sum(1 for x in A[k]['full_items'].values() if x['r'] in val) for k in TR]
cx=fig.add_subplot(gs[2]); rows=[]
for k,nm in [('2','ACCESS'),('24','RAIDERS')]:
    for part,items in [('CONSORT 2010 items',A[k]['full_items']),('AI extension items',A[k]['ai_items'])]:
        v=[val[x['r']] for x in items.values() if x['r'] in val]; rows.append((f'{nm}: {part}',100*sum(v)/len(v)))
for i,(l,v) in enumerate(rows):
    cx.barh(i,v,color=YES if 'AI ext' in l else '#8a8984',height=0.6,edgecolor='white'); cx.text(v+1.5,i,f'{v:.0f}%',va='center',fontsize=7.5)
cx.set_yticks(range(len(rows))); cx.set_yticklabels([r[0] for r in rows]); cx.tick_params(axis='y',length=0); cx.set_ylim(len(rows)-0.5,-0.5); cx.set_xlim(0,100); cx.set_xlabel('Adherence (%)')
fig.canvas.draw()
panel(fig,ax,'a','AI measurement studies (n = 22): ten domains adapted from CONSORT-AI')
panel(fig,bx,'b',f'Prediction and diagnostic model studies (n = 12): TRIPOD+AI, median adherence {st.median(adh):.0f}%')
panel(fig,cx,'c','Randomized trials of AI interventions (n = 2): CONSORT-AI')
for e in ['png','pdf']: fig.savefig(OUT+f'Fig3_reporting_by_study_type.{e}',dpi=300)
print(rows, st.median(adh))
