---
title: "Here time turns into space: Does consciousness implement the fractional Fourier transform?"
source: "https://smoothbrains.net/posts/2025-10-17-fractional-fourier-transforms.html"
author:
published: 2025-10-17
created: 2026-06-02
description:
tags:
  - "clippings"
---
I was lucky enough to be introduced to the [Fourier transform](https://en.wikipedia.org/wiki/Fourier_transform) when I was relatively young. I was an media nerd as a teenager, and as such I spent a significant amount of time editing digital images and audio using software like [Adobe Photoshop](https://www.adobe.com/products/photoshop.html) and [Ableton Live](https://www.ableton.com/). Lacking restraint, I often had a lot of fun combining the filters available in original ways – layering up excessive [*colour correction*](https://en.wikipedia.org/wiki/Color_balance) or [*convolution filters*](https://en.wikipedia.org/wiki/Kernel_\(image_processing\)) in Photoshop, or perhaps [*chorus*](https://en.wikipedia.org/wiki/Chorus_\(audio_effect\)), [*reverb*](https://en.wikipedia.org/wiki/Reverb_effect), and [*equalisation*](https://en.wikipedia.org/wiki/Audio_equalizer) in Ableton.

![](https://smoothbrains.net/images/random/frft/glass_reflections.jpg)

Self-portrait taken in 2001 using a Sony Mavica MVC-FD71. A heavy posterisation filter is applied.

My life changed when someone whispered the words [*signal theory*](https://en.wikipedia.org/wiki/Signal_processing) in my direction. This lead me to understand that audio and images were just one and two dimensional [*digital signals*](https://en.wikipedia.org/wiki/Digital_signal), and that mathematically there wasn’t much difference between the amplitude of a [*sample*](https://en.wikipedia.org/wiki/Sampling_\(signal_processing\)) and the brightness of a [*pixel*](https://en.wikipedia.org/wiki/Pixel). Additionally, many of the one dimensional transformations I was applying had two dimensional equivalents – and vice versa. An audio [*low-pass filter*](https://en.wikipedia.org/wiki/Low-pass_filter) is also a [*Gaussian blur*](https://en.wikipedia.org/wiki/Gaussian_blur) when you apply it to an image! *Got it*.

The second breakthrough came when someone else nudged me towards reading about the [*Fourier transform*](https://en.wikipedia.org/wiki/Fourier_transform). I gave a brief review of the Fourier transform in my [previous post](https://smoothbrains.net/posts/2025-10-10-the-three-marks.html#the-fourier-transform):

I found this revelatory. Suddenly I was no longer restricted to thinking about the media I worked with in the *time domain* or *spatial domain* – there was a whole new *frequency domain* I could transform signals into. It felt like I could now see the world from a vantage point in a dimension orthogonal to spacetime.

![](https://smoothbrains.net/images/random/frft/artem_kirsanov_fourier_transform.png)

Illustration of the Fourier transform. From Artem Kirsanov on YouTube.

I began to notice applications of the Fourier transform all around me; how it pervaded our technological reality and how I could use it to reason about the signals I encountered in everyday life. I now understood how the [compression codec](https://en.wikipedia.org/wiki/MP3) in my [MP3 player](https://en.wikipedia.org/wiki/Creative_Zen#ZEN_Micro) and the [pitch shifting](https://en.wikipedia.org/wiki/Pitch_shifting) algorithm in my guitar’s [DigiTech Whammy](https://digitech.com/dp/whammy/) pedal worked.

![](https://smoothbrains.net/images/random/frft/adobe_audition_spectrogram.png)

Back in 1999, the musician Aphex Twin used software called MetaSynth to hide a picture of his own face in the spectrogram of one of his songs. Viewed in Adobe Audition.

I was delighted to discover audio software like [MetaSynth](https://uisoftware.com/metasynth/) and later [Adobe Audition](https://www.adobe.com/products/audition.html), which has a spectrogram view which lets you work inside the [short-time Fourier transform](https://en.wikipedia.org/wiki/Spectrogram) directly – and even found a [two-dimensional Fourier transform](https://www.robots.ox.ac.uk/~az/lectures/ia/lect2.pdf) [plugin](https://www.3d4x.ch/Swift's-Reality/FFT-Photoshop-plugin-by-Alex-Chirokov/16,35) for [Adobe Photoshop](https://www.adobe.com/products/photoshop.html), which was so powerful that I was surprised that Photoshop did not come bundled with such a feature by default.

![](https://www.youtube.com/watch?v=yyox358zIRw)

A demonstration of how to use a two-dimensional Fourier transform plugin in Adobe Photoshop to remove a [moiré pattern](https://en.wikipedia.org/wiki/Moir%C3%A9_pattern) from a scanned image. By [VSXD Tutorials](https://www.youtube.com/@VSXD) on YouTube.

Later in life I would often find excuses to work frequency domain processing into various [creative coding](https://en.wikipedia.org/wiki/Creative_coding) projects, as I found that I could often derive much more original and surprising effects than what was achievable otherwise.

Even later, I find myself involved with [consciousness research](https://qri.org/). I’ve described it better [elsewhere](https://smoothbrains.net/posts/2025-07-31-is-consciousness-holographic.html#what-is-it-like-to-be-a-hologram) – but in brief, I regard this as a process of [reverse engineering](https://en.wikipedia.org/wiki/Reverse_engineering), which involves observing phenomenology in both sober and [altered](https://en.wikipedia.org/wiki/Altered_state_of_consciousness) states of consciousness, and discussing which mathematical tools are most appropriate for modelling its dynamics.

Frequency domain analysis is incredibly useful, so it would be surprising to me if evolution did not find a way of implementing it too. For example, it can be used in [object recognition](https://en.wikipedia.org/wiki/Object_detection) to recognise frequency domain invariants of a given object independent of [translation, rotation, and scale](https://en.wikipedia.org/wiki/Affine_transformation). Perhaps it would be fruitful to consider how a biological analogue of the Fourier transform might be implemented – and if so, might we also recognise its phenomenological signature?

![](https://smoothbrains.net/images/random/frft/ft_pairs.png)

Pairs of common functions and their freque ncy domain spectra. Note how the cosine function corresponds to a spike in the frequency domain, and so on. Consider that such values will remain invariant independent of where the original signal is located in time. From Feature Extraction and Image Processing for Computer Vision (Nixon and Aguado, 2002).

In this post, I’m going to discuss how the brain may implement something like the Fourier transform. Specifically, I believe it may use something called the [*fractional* Fourier transform](https://en.wikipedia.org/wiki/Fractional_Fourier_transform) – a generalisation of the regular Fourier transform which is amenable to implementation using wave dynamics.

[Firstly](#what-is-the-fractional-fourier-transform), I’ll explain what the fractional Fourier transform is and show how it can appear naturally in a variety of physical systems. [Secondly](#does-the-fractional-fourier-transform-show-up-in-subjective-experience), I’ll then discuss what kind of phenomenological signature we might expect the fractional Fourier transform to leave behind – namely, the characteristic [*ringing artifacts*](https://en.wikipedia.org/wiki/Ringing_artifacts) which arise in the visual field during psychedelic experiences. [Thirdly](#how-might-the-fractional-fourier-transform-show-up-in-the-brain), I’ll explore how the brain might implement such a transform using travelling waves in cortical structures. Then [finally](#what-is-the-computational-utility-of-the-fractional-fourier-transform), I’ll discuss why this would be computationally advantageous – it would provide a means of implementing the kind of massively parallel pattern recognition operations which would be prohibitively expensive to implement any other way.

## What is the fractional Fourier transform?

I’m looking for a *biologically plausible* implementation, so I was pleased to discover the *fractional* Fourier transform exists – a continuous domain transform which can smoothly interpolate from time domain or spatial domain to the frequency domain and back again.

![](https://smoothbrains.net/images/random/frft/formula_fractional_fourier_transform.svg)

The fractional Fourier transform function.

Crucially, the fractional Fourier transform can be implemented in wave-based systems – for example, in optics via [Fresnel diffraction](https://en.wikipedia.org/wiki/Fresnel_diffraction), or speculatively cortical travelling waves. We’ll get into how that works in a moment, but first I’m going to explain the fractional Fourier transform. We’ll work in two dimensions, as I think that’s more illustrative. We’ll start by looking at the regular two-dimensional Fourier transform:

![](https://smoothbrains.net/images/random/frft/2d_frft_1.png)

A demonstration of the two-dimensional Fourier transform using the Lena test image. The spatial domain signal is on the left and the frequency domain right. Red, green, and blue channels are transformed separately. Only the complex magnitude is shown.

Note that the [lowest frequencies](https://en.wikipedia.org/wiki/DC_bias) are at the origin, while the [highest frequencies](https://en.wikipedia.org/wiki/Nyquist_frequency) are at the border. In this case, the presence of low frequencies generates the bright central [cusp](https://en.wikipedia.org/wiki/Cusp_\(singularity\)). We also see a pair of diagonal streaks indicating the presence of broadband diagonal spatial frequencies in the original signal.

![](https://smoothbrains.net/images/random/frft/2d_frft_1b.png)

A demonstration of the two-dimensional Fourier transform using a more abstract test image – a tilted square grid. The significant frequency domain components are visible on the right as the cross-shaped cusps aligned perpendicular to their originating waves.

The fractional Fourier transform can be considered to be a *rotation* in the [time-frequency plane](https://en.wikipedia.org/wiki/Time%E2%80%93frequency_analysis), and as such the relevant free parameter is known as the *angle* *α*, which is a value in the range 0 to 2 *π*. Though sometimes we use the *order* *a*, which is in the range 0 to 4. This is the fractional Fourier transform at four different orders:

![](https://smoothbrains.net/images/random/frft/2d_frft_2.png)

The two-dimensional fractional Fourier transform for orders a ∈ {0, ⅓, ⅔, 1}.

Isn’t that neat. I think the [*ringing artifacts*](https://en.wikipedia.org/wiki/Ringing_artifacts) at *a* = ⅓ are particularly curious. The integer values of *a* are useful to understand:

0. The signal
1. The Fourier transformed signal
2. The inverse signal
3. The inverse Fourier transformed signal
4. The signal

The fractional Fourier transform loops back on itself at *a* = 4:

![](https://smoothbrains.net/images/random/frft/2d_frft_3.png)

The fractional Fourier transform can be understood as a rotation in phase space.

Perhaps an animated version should be more illustrative:

<video controls=""><source src="https://smoothbrains.net/images/random/frft/frft_lena_1024.mp4" type="video/mp4"></video>

The two-dimensional fractional Fourier transform cycling through the range a ∈ \[0, 4). I suspect consciousness may be doing something akin to this, forty times per second – but we’ll come back to that later.

Isn’t this mysterious. If you have noticed the aesthetic resemblance with [diffraction patterns](https://en.wikipedia.org/wiki/Diffraction), that’s not a coincidence. The fractional Fourier transform can be implemented using a [coherent light source](https://en.wikipedia.org/wiki/Laser) and a pair of lenses – and analog frequency domain filters can even be implemented by inserting a mask at the focal plane:

<video controls=""><source src="https://smoothbrains.net/images/random/frft/hans_chiu_lens_transform.mp4" type="video/mp4"></video>

Demonstration of the optical Fourier transform. Note how the first lens, focal plane, and second lens correspond to fractional orders 0, 1, and 2 respectively. By Hans Chiu on Twitter.

### Quantum systems and fractional revivals

The fractional Fourier transform can also be implemented using the [Schrödinger wave equation](https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation) from quantum mechanics. In fact, the Fourier equation and the Schrödinger equation are very deeply related to one another. The Schrödinger wave function is usually expressed in [*position space*](https://en.wikipedia.org/wiki/Position_and_momentum_spaces#Position_space) *ψ* (*x*, *t*), but to obtain the wavefunction in [*momentum space*](https://en.wikipedia.org/wiki/Position_and_momentum_spaces#Momentum_space) *ϕ* (*p*, *t*) you simply apply the Fourier transform. This also shows why the [Heisenberg uncertainty principle](https://en.wikipedia.org/wiki/Uncertainty_principle) is mathematically equivalent to the [Fourier uncertainty principle](https://smoothbrains.net/posts/2025-10-10-the-three-marks.html).

Anyway, to compute the time evolution of a Schrödinger wave function, it’s natural to move into momentum space – so this is where the Fourier transform comes in. So, the time evolution of the wave function of a [particle in free space](https://en.wikipedia.org/wiki/Free_particle) is equivalent to the [Fresnel transform](https://en.wikipedia.org/wiki/Fresnel_diffraction), which is itself equivalent to the fractional Fourier transform except that it spreads out in space as time goes on. For a [particle in a quadratic potential well](https://en.wikipedia.org/wiki/Quantum_harmonic_oscillator), the time evolution is *exactly* the fractional Fourier transform. Other potential wells are more complicated, but may also be approximated locally by similar Fourier-type transformations.

<video controls=""><source src="https://smoothbrains.net/images/random/frft/qm1d_larger_sharp.mp4" type="video/mp4"></video>

A quantum mechanical simulation of the behaviour of a particle in an infinite one dimensional potential well. The probability distribution of the particle’s position is at the top and the probability distribution of the particle’s momentum is at the bottom. Note that the pattern repeats itself as the video loops. Generated using Paul Falstad ’s 1D quantum states applet.

Such systems may return to their original states periodically, despite undergoing complicated spreading and self-interference along the way. The period on which they repeat themselves is known as the [*revival time*](https://en.wikipedia.org/wiki/Quantum_revival), and in some systems, the wave function passes through exact fractional Fourier transforms of the original signal along the way. In other systems, fractional revivals may instead produce multiple smaller copies of the original wave packet rather than a simple Fourier relation.

<video controls=""><source src="https://smoothbrains.net/images/random/frft/qm2dbox_looping.mp4" type="video/mp4"></video>

A quantum mechanical simulation of the behaviour of a particle in an infinite two dimensional potential well. Notice the fractional revivals where a smaller version of the original wave function tiles the potential well. Generated using Paul Falstad ’s 2D quantum box modes applet.

Revivals are a generic wave phenomenon and are not unique to quantum systems – they show up in classical optical and acoustic systems as well. I found this to be an encouraging prospect – suddenly the class of systems which could implement the fractional Fourier transform became much broader. I began experiencing imaginal visions, of the structure of the universe reflecting and repeating itself [all the way down](https://en.wikipedia.org/wiki/Huayan#/media/File%3AIndrasnet.jpg), dispersing and reviving on an eternal loop, at every scale, forever…

### Talbot carpets and whispering gallery modes

Another way of viewing the fractional Fourier transform is to think of its *order* as corresponding to the propagation distance in free-space diffraction. For a [plane wave](https://en.wikipedia.org/wiki/Plane_wave) passing through a [periodic grating](https://en.wikipedia.org/wiki/Diffraction_grating), the field at distance *z* is given by the fractional Fourier transform of the grating’s transmission function at some order *a* proportional to *z*. Plotting the field intensity as a function of position and distance then gives you a pattern known as a [Talbot carpet](https://en.wikipedia.org/wiki/Talbot_effect):

![](https://smoothbrains.net/images/random/frft/talbot_carpet.png)

The optical Talbot effect for a diffraction grating. Full or fractional revivals of the original pattern appear at propagation distances that are rational fractions of the Talbot distance, forming the intricate interference pattern of the Talbot carpet. From Wikipedia.

These patterns are of real concern when one considers the [whispering gallery modes](https://en.wikipedia.org/wiki/Whispering-gallery_wave) that arise close to the surface of [fiber optics](https://en.wikipedia.org/wiki/Optical_fiber):

![](https://smoothbrains.net/images/random/frft/talbot_carpet_whispering_gallery_modes.jpg)

Whispering gallery modes used to implement a one-to-eight beam splitter in a cylindrical waveguide. From Talbot interference of whispering gallery modes (Eriksson et al., 2025). Found via outside five sigma on Twitter. Even more unusual beam splitters are possible with differently shaped fibers.

Mostly I am highlighting Talbot carpets here because they round out our tour of the fractional Fourier transform’s ubiquity. From the quantum revivals in potential wells to the interference patterns in fiber optics, it seems that the fractional Fourier transform is kind of just lying around in nature, waiting to be noticed – not as some exotic mathematical object, but as a fundamental organisational principle underlying the evolution of wave systems in time.

## Does the fractional Fourier transform show up in subjective experience?

We think that it’s fairly straightforward to make the case that the plain Fourier transform shows up in subjective experience. I presented an example of frequency domain attentional modulation in my [previous post](https://smoothbrains.net/posts/2025-10-10-the-three-marks.html#time-frequency-and-uncertainty):

> ![](https://smoothbrains.net/images/random/frft/tristable_stimulus.png)
> 
> Perhaps this image is a good example of how phenomena can have spectral components. Consider texture – just as I can focus my attention like a spotlight at a different locations in space, I find I can also use it to tune in to different spectral qualities of a given object. This stimulus is constructed from three sine waves – can you isolate each one in turn? From The dynamics of perceptual rivalry in bistable and tristable perception (Wallis and Ringelhan, 2013).

[We believe this becomes easier to observe in altered states](https://x.com/algekalipso/status/1774575626131013831). Have you ever taken a small amount of LSD and found yourself engrossed in a pattern on the wallpaper or carpet? Consider what frequency domain transform that might correspond to – are specific spectral peaks being stabilised or amplified, while spatial precision is reduced? Andrés explored [*uncertainty principle qualia*](https://x.com/algekalipso/status/1779961694909030624) in great detail on [The DemystifySci Podcast](https://www.youtube.com/@DemystifySci_Podcast) last year:

> ![](https://www.youtube.com/watch?v=46Zf-JEpFhQ)
> 
> What I have found is that there is something akin to the [Heisenberg uncertainty principle](https://en.wikipedia.org/wiki/Uncertainty_principle) going on, having to do with what kind of patterns you can perceive. And essentially there’s a trade-off between having more information about the spatial domain – like the *position* of things – versus having more information about the frequency domain – like the *frequencies* and *vibrations*, and the *spectrum*, like what’s happening in different time scales.
> 
> And so one extreme – this happens in high dose LSD, but it’s also a [*jhāna*](https://astralcodexten.substack.com/p/nick-cammarata-on-jhana) effect – on the one extreme you can concentrate all the information into *position*, and when that happens you collapse into one point. It’s a very strange experience – you just become one point, you’re not a person anymore, it feels as if all of your attention is just one point. That’s a real state of consciousness – the Buddhists talk about it – it’s very peculiar.
> 
> But then also, the complete opposite – you can concentrate all of the information, or all of the sampling into *frequency*. So when you do that, you turn into a *vibe*. You stop being anywhere and you’re just a vibration. You’re just a wave – it’s very emotional, it’s a very different type of experience.
> 
> So, my guess is that these are the extremes. So when you’re hyper-concentrated, you can do *this* or you can do *that* – I think normal states of consciousness are a mixture. Like we have several attentional centers, and they’re sampling both spatial and temporal information – both *momentum* and *position* – and the precise balance that you choose between them corresponds to your personality and your state of consciousness. In a way, your way of being is intimately related with how you sample the world. There’s always going to be something you’re missing – because if you just focus on frequency you’re gonna lose the spatial information, and vice versa. So I wonder if that is connected – no entity can actually know a space fully – it has to do a trade-off, and there’s no way around it.

However, I am interested in looking for signatures of the *fractional* Fourier transform, which is a little more specific and complicated. I’ve shown a handful of people the visuals I generated for this post, and in the process of doing so I’ve received some amount of [positive feedback](https://x.com/cube_flipper/status/1892640495026708568).

![](https://smoothbrains.net/images/random/frft/symmetric_comments_crop.png)

Raimonds ’ initial reaction when I showed him the renderings I made for this post.

People have compared these renderings to a variety of unusual phenomena, including [k-holes](https://en.wikipedia.org/wiki/K-hole), [LSD](https://en.wikipedia.org/wiki/LSD), [meditative cessations](https://www.youtube.com/watch?v=Wo_cGIViy4Y), and even [the arising and passing of *consciousness frames*](https://blankhorizons.com/2021/03/02/shinzen-youngs-10-step-model-for-experiencing-the-eternal-now/). I find this encouraging, although the states described tend to be quite extreme – only accessible through high doses of drugs or extensive training in meditation. I also don’t think this kind of informal phenomenology is *repeatable* enough to stake any strong claims on – I’m more interested in finding *accessible*, low level, simple phenomena which are amenable to study using [psychophysics](https://en.wikipedia.org/wiki/Psychophysics) experiments.

<video controls=""><source src="https://smoothbrains.net/images/random/frft/3blue1brown_holography_7.mp4" type="video/mp4"></video>

A few people have recognised the distinctive shifting noise patterns in the background of the fractional Fourier transform as the kind of thing they observe while on psychedelics or dissociatives. I think they are quite similar to the speckle patterns that occur when a coherent light source scatters off a rough surface. Animation from How are holograms possible? by 3Blue1Brown on YouTube.

### Fresnel fringes and ringing artifacts

In the fractional Fourier transform demonstration earlier, did you notice the distinctive [*ringing artifacts*](https://en.wikipedia.org/wiki/Ringing_artifacts) around the edges of objects? These are known as [*Fresnel fringes*](https://www.jeol.com/words/emterms/20121023.093457.php). Characteristically, the spacing of these fringes decreases with distance from the edge, such that the fringes become progressively finer. This pattern arises from the *quadratic phase* terms underlying the [Fresnel diffraction](https://en.wikipedia.org/wiki/Fresnel_diffraction) formalism, which also underpins optical implementations of the fractional Fourier transform.

![](https://smoothbrains.net/images/random/frft/fresnel_fringes.png)

Fresnel fringes seen in a transmission electron microscope image.

These show up in any wave based media in which Fresnel diffraction applies – not just in optics, but also in acoustic and quantum wave systems. Ringing artifacts also show up in my [visual field](https://en.wikipedia.org/wiki/Visual_field) when I’m on a moderate dose of a serotonergic psychedelic – for instance one or two grams of [psilocybin mushrooms](https://en.wikipedia.org/wiki/Psilocybin_mushroom). You might also call these *auras* or *haloes*.

<video controls=""><source src="https://smoothbrains.net/images/random/frft/frft_shape_star_3_1024.mp4" type="video/mp4"></video>

The two-dimensional fractional Fourier transform for a star. Note the ringing artifacts close to the edges of the star just after the transform begins.

I’ve spent some time looking at ringing artifacts while on psychedelics, and I have found that – at least at low doses – [some psychedelics generate coarser or finer ringing artifacts than others](https://x.com/cube_flipper/status/1876393927022121337). In order from coarse to fine, 2C-B, LSD and psilocybin generate progressively tighter ringing artifacts.

The key aspect is whether or not the fringes become finer with *distance from the edge*. If this is the case, then I believe this would be a strong argument that dynamics analogous to Fresnel optics are somehow playing out within the brain – which would mean that the brain may provide a viable substrate for analog computations like the fractional Fourier transform. By comparison, if the visual cortex was exclusively operating as a [convolutional neural network](https://en.wikipedia.org/wiki/Convolutional_neural_network), then we would have no reason to expect to see these particular artifacts.

I’ve shown these animations to some friends who have confirmed that the ringing artifacts that they see while on psychedelics resemble the ones in these renderings – and that the fringes do indeed become finer with distance from the edge.

Personally, it’s been some time since I last took a decent dose of psychedelics – and the last time I did so, I wasn’t keeping an eye on the ringing artifacts. I’ll have to set some time aside to take a couple grams of mushrooms and check for myself soon whether they resemble Fresnel fringes. If I find this is the case, then I should be motivated to construct some kind of questionnaire or psychophysics tool which could be used to verify whether other people also see the fingerprint of Fresnel diffraction in their subjective experience.

## How might the fractional Fourier transform show up in the brain?

There’s a baseline assumption which so far I’ve neglected to address, which is that representations in the mind are structurally similar to the objects in the world which they represent – sufficiently so at least that a transformation of some kind on one can approximate a transformation on the other.

There have been a [number](https://www.biorxiv.org/content/10.1101/2024.06.19.599691v1.full) [of](https://openaccess.thecvf.com/content/CVPR2023/papers/Takagi_High-Resolution_Image_Reconstruction_With_Latent_Diffusion_Models_From_Human_Brain_CVPR_2023_paper.pdf) [recent](https://www.sciencedirect.com/science/article/pii/S0893608023006470) [successes](https://www.nature.com/articles/s41586-023-06377-x) in reading video and speech representations from the brain, but generally this involves an intermediary decoding layer where machine learning techniques are used to interpret neuroimaging signals. I might be opinionated here when I claim that these results are simultaneously impressive and unsatisfying. Perhaps [interpretability researchers](https://www.goodfire.ai/) might sympathise when I say I think the assumption that neural representations will be forever inscrutable – requiring essentially a neural network to read a neural network – is an overly pessimistic assumption, and the fact that we haven’t uncovered the *true* representations yet is more a factor of insufficient neuroimaging fidelity than the result of [messy, illegible complexity](https://x.com/cube_flipper/status/1958597872397828590) at every layer in the stack. Why should illegibility be the default assumption, when there are computational benefits to well-structured representations?

<video controls=""><source src="https://smoothbrains.net/images/random/frft/mouse_visual_cortex_trimmed.mp4" type="video/mp4"></video>

From the paper, Movie reconstruction from mouse visual cortex activity (Bauer et al., 2024)

### Travelling waves and spatiotemporal dynamics

A recent paper from the [Kempner Institute](https://kempnerinstitute.harvard.edu/) makes the case that the spatiotemporal dynamics of [*traveling waves*](https://en.wikipedia.org/wiki/Periodic_travelling_wave) could provide a reasonable basis for neural representations, as these dynamics can be recruited to encode the symmetries of the world as conserved quantities. From [A Spacetime Perspective on Dynamical Computation in Neural Information Processing Systems](https://arxiv.org/abs/2409.13669) (Keller et al., 2024):

> There is now substantial evidence for traveling waves and other structured spatiotemporal recurrent neural dynamics in cortical structures; but these observations have typically been difficult to reconcile with notions of topographically organized selectivity and feedforward receptive fields. We introduce a new ‘spacetime’ perspective on neural computation in which structured selectivity and dynamics are not contradictory but instead are complimentary. We show that spatiotemporal dynamics may be a mechanism by which natural neural systems encode approximate visual, temporal, and abstract symmetries of the world as conserved quantities, thereby enabling improved generalization and long-term working memory.

Keller argues that rather than simply learning features that are invariant to transformations, the brain may be explicitly learning the symmetries themselves:

> To begin to understand the relationship between spatiotemporally structured dynamics and symmetries in neural representations, it is helpful take a step back and understand more generally what makes a ‘good’ representation. Consider a natural image – a full megapixel array representing an image is very high dimensional, but the parts of the image that need to be extracted are generated by a much lower dimensional process. For example, imagine a puppet that is controlled by nine strings (one to each leg, one to each hand, one to each shoulder, one to each ear for head movements, and one to the base of the spine for bowing); the state of the puppet could be transmitted to another location by the time course of nine parameters, which could be reconstructed in another puppet. It is therefore more efficient to represent the world in terms of these lower-dimensional factors in order to be able to reduce the correlated structural redundancies in the very high-dimensional data.
> 
> At a high level, one can understand the goal of ‘learning’ with deep neural networks as attempting to construct these useful factors that are abstractions of the high-resolution degrees of freedom in sensory inputs, exactly like inferring the control strings of the universal puppet master. This is similar to the way that the [renormalization group](https://en.wikipedia.org/wiki/Renormalization_group) procedure in physics compresses irrelevant degrees of freedom by coarse graining to reveal new physical regularities at larger spatiotemporal scales, and is a model for how new laws emerge at different spatial and temporal scales. As agents in the complex natural world, we seek to represent our surroundings in terms of useful abstract concepts that can help us predict and manipulate the world to enhance our survival.
> 
> One early idealized view of how the brain might be computing such representations is by learning features that are *invariant* to a variety of natural transformations. This view was motivated by the clear ability of humans to rapidly recognize objects despite their diverse appearance at the pixel level while undergoing a variety natural geometric transformations, and further by the early findings of [Gross et al.](https://doi.org/10.1152/jn.1972.35.1.96) (1973) that individual neurons in higher levels of the visual hierarchy responded selectively to specific objects irrespective of their position, size, and orientation.

Another Kempner Institute preprint puts these ideas into practice, demonstrating that travelling waves can be used to discover spectral signatures which are useful for shape classification. From [Traveling Waves Integrate Spatial Information Through Time](https://arxiv.org/abs/2502.06034v4) (Jacobs et al., 2025):

> Traveling waves of neural activity are widely observed in the brain, but their precise computational function remains unclear. One prominent hypothesis is that they enable the transfer and integration of spatial information across neural populations. However, few computational models have explored how traveling waves might be harnessed to perform such integrative processing.
> 
> Drawing inspiration from the famous “ [Can one hear the shape of a drum?](https://en.wikipedia.org/wiki/Hearing_the_shape_of_a_drum)” problem – which highlights how normal modes of wave dynamics encode geometric information – we investigate whether similar principles can be leveraged in artificial neural networks. Specifically, we introduce convolutional recurrent neural networks that learn to produce traveling waves in their hidden states in response to visual stimuli, enabling spatial integration. By then treating these wave-like activation sequences as visual representations themselves, we obtain a powerful representational space that outperforms local feed-forward networks on tasks requiring global spatial context.

As the travelling waves dissipate, each neuron has the opportunity to accumulate spectral information about the shape of the structure it is contained within. Perhaps an animation will be illustrative – from the authors’ [GitHub page](https://github.com/anonymous123-user/Wave_Representations):

> ![](https://smoothbrains.net/images/random/frft/wave_hexagon.gif)
> 
> Figure 3: Waves propagate differently inside and outside shapes, integrating global shape information to the interior. Sequence of hidden states of an oscillator model trained to classify pixels of polygon images based on the number of sides using only local encoders and recurrent connections. We see the model has learned to use differing natural frequencies inside and outside the shape to induce soft boundaries, causing reflection, thereby yielding different internal dynamics based on shape.

In this manner, every part may accumulate a representation of the whole, and the accumulated spectral qualities can be used to infer what shape the part is contained within:

> ![](https://smoothbrains.net/images/random/frft/polygons_fft_seq_smaller.png)
> 
> Figure 4: Wave-based models learn to separate distinct shapes in frequency space. ( Left ) Plot of predicted semantic segmentation and a select set of frequency bins for each pixel of a given test image. ( Right ) The full frequency spectrum for dataset. We see that different shapes have qualitatively different frequency spectra, allowing for >99% pixel-wise classification accuracy on a test set.

I recommend checking out [Mozes Jacobs](https://x.com/mozesjacobs) ’ video presentation, as he has even generated sounds representative of each shape being classified. Incredibly cool:

![](https://www.youtube.com/watch?v=twBIvDaaMOY)

This is extremely speculative, but I feel that there’s something analogous to a wave based implementation of the fractional Fourier transform going on here – only, what’s being calculated is not so much the spectral qualities of the *signal* as the spectral qualities of the *resonant cavity* it is contained within. I currently lack the mathematical background necessary to explore a reconciliation between these two ideas.

### Entorhinal cortex and visual cortex

I did also search for other literature presenting evidence for the Fourier transform in neural processes. [Orchard et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3858727/) (2013) propose that the [grid cells](https://en.wikipedia.org/wiki/Grid_cell) in the [entorhinal cortex](https://en.wikipedia.org/wiki/Entorhinal_cortex) and [place cells](https://en.wikipedia.org/wiki/Place_cell) in the [hippocampus](https://en.wikipedia.org/wiki/Hippocampus) reconstruct a spatial map of an animal’s environment using an inverse Fourier transform – but most fascinating to me was a very old electrode study on cats and macaque monkeys proposing that neurons in the [visual cortex](https://en.wikipedia.org/wiki/Visual_cortex) actually respond to the *spectral* components of visual stimuli. As always, I have a soft spot for weird old neuroscience papers, so I include it here. From [Responses of striate cortex cells to grating and checkerboard patterns](https://pubmed.ncbi.nlm.nih.gov/113531/) (De Valois et al., 1979), various visual stimuli and their two-dimensional Fourier spectra:

> ![](https://smoothbrains.net/images/random/frft/gratings_and_checkerboards_1.png)
> 
> Fig. 1. Stimulus patterns and their two-dimensional Fourier spectra. In the left column are photographs of the oscilloscope displays of the various stimuli. The right column depicts the two-dimensional spectra (out to the fifth harmonic) corresponding to each of the patterns on the left. Frequency is represented on the radial dimension, orientation on the angular dimension, and the areas of the filled circles represent the magnitudes of the Fourier components. A, a square-wave grating; B, a 1/1 (check height/check width) checkerboard; C, a 0.5/1 checkerboard; D, a plaid pattern. The Fourier spectra of the various patterns are discussed in some detail in the text.

Note how the harmonics for the square wave grating are arranged at 0° to the origin, whereas the harmonics for the checkerboard are arranged at 45° to the origin. The authors propose that if [orientation selective](https://en.wikipedia.org/wiki/Orientation_selectivity) neurons actually respond to a spectral basis rather than orientation alone, then we would expect neurons which fire when presented with a grating rotated by 0° to also fire when presented with a checkerboard rotated by 45°. Well, that is exactly what they found:

> ![](https://smoothbrains.net/images/random/frft/gratings_and_checkerboards_2.png)
> 
> Fig. 3. Orientation tuning of cortical cells to a grating and a 1/1 checkerboard. Angles 0-180° represent movement down and/or to the right; angles 180-360° represent movement up and/or to the left. The orientations plotted for both gratings (■—■) and checkerboards (▲⋯▲) are the orientations of the edges. Note that the optimum orientations for the checkerboard are shifted 45° from those for the grating. Panel A shows responses recorded from a simple cell of a cat. Panel B illustrates responses of a monkey complex cell.

The consensus in modern neuroscience is that neurons in the visual cortex actually respond to [Gabor wavelet](https://en.wikipedia.org/wiki/Gabor_wavelet) [receptive fields](https://en.wikipedia.org/wiki/Receptive_field), *not* spectral components. A [Gabor function](https://en.wikipedia.org/wiki/Gabor_filter) is constructed by multiplying a [Gaussian function](https://en.wikipedia.org/wiki/Gaussian_function) by a [sine wave](https://en.wikipedia.org/wiki/Sine_wave) – and represents the ideal trade-off between spatial and spectral domain [uncertainty](https://en.wikipedia.org/wiki/Fourier_transform#Uncertainty_principle). In other words, Gabor wavelet receptive fields are *already* performing a kind of Fourier analysis, extracting information about both the spatial and frequency domain qualities of visual features simultaneously.

![](https://smoothbrains.net/images/random/frft/gabor_functions.png)

An ensemble of odd and even Gabor filters. From Image Representation Using 2D Gabor Wavelets (Lee, 1996)

The important difference between the Fourier transform model and the Gabor receptive field model is as follows: In the Fourier model, neurons would respond to frequency components *regardless* of where they appear in the visual field, whereas in the Gabor model, neurons would respond to frequency components *at a specific location*. The grating and checkerboard experiments described above suggest that the visual system may track the *global* frequency decomposition of a scene, not just *local* frequency patches. I’m not sure how to reconcile this with mainstream understanding or why the findings of this paper are not more widely known. Did nobody ever repeat this experiment – do all modern studies use gratings alone?

If something like the Fourier transform model does turn out to be the case, I’d be inclined to wonder if other sensory cortices may be performing analogous transforms on incoming sensory information – and maybe [the entire brain is composed of an complex hierarchy of such structures](https://qualiacomputing.com/2025/09/13/indras-net-via-nonlinear-optics-dmt-phenomenology-as-evidence-for-beamsplitter-holography-and-recursive-harmonic-compression/)? The [auditory cortex](https://en.wikipedia.org/wiki/Auditory_cortex) is the obvious candidate for analysis – but perhaps this could also explain the [mysterious gaps found on our representation of the somatosensory homunculus](https://www.nature.com/articles/s41586-023-05964-2#Fig4)?

## What is the computational utility of the fractional Fourier transform?

Alright, so what is all this *for*? As I have written [previously](https://smoothbrains.net/posts/2025-07-31-is-consciousness-holographic.html#what-does-it-mean-to-be-a-hologram), I think a big part of what consciousness is doing is performing a massively parallel analogue [self-convolution](https://en.wikipedia.org/wiki/Autocorrelation) on the contents of awareness, scouring sensory information for any patterns it can find in the pursuit of reifying a parsimonious world model in which every part still has an influence on the whole. To understand why this would be expensive to implement, consider what convolution actually does. For every point in a signal, you have to compare it with every other point – which adds up to *O* (*n* <sup>2</sup>) operations in total. For a high resolution visual field with millions of “points”, this quickly becomes intractable.

The [*convolution theorem*](https://en.wikipedia.org/wiki/Convolution_theorem) tells us that the *convolution* of two time or spatial domain signals is the same as their *product* in the frequency domain. So, we first take the Fourier transform our signal, multiply the frequency components together, and then take the inverse Fourier transform to convert it back. The multiplication operation only requires *O* (*n*) operations, but the Fourier transforms require *O* (*n* log *n*). This is a sizeable improvement, but it’s still computationally demanding, and evolution would still need to find some way to hard code the point-to-point wiring required to implement the Fourier transform into our genomes. This is why the *fractional* Fourier transform is so appealing – it can be implemented using simple wave dynamics without requiring any hard-wired connections. The waves just do their thing, and the Fourier transform arises naturally from the physics.

Additionally, if [reports from the meditators I know](https://smoothbrains.net/posts/2023-10-28-attention-and-awareness.html#what-might-the-exact-refresh-rate-be) are to be believed, upon investigation it appears that consciousness refreshes itself at a rate of around *40 Hz*. This isn’t just idle speculation – experienced meditators across multiple contemplative traditions who have cultivated high sensory clarity often report being able to perceive the discrete, flickering nature of conscious experience arising and passing away, often at a rate of roughly forty times per second.

![](https://smoothbrains.net/images/random/frft/activity_of_the_source.png)

For a thorough dissection of what a consciousness refresh cycle looks like, I highly recommend Kenneth Shinozuka ’s writeup, Shinzen Young’s 10-Step Model for Experiencing the Eternal Now.

[Is one consciousness frame equivalent to one cycle of the fractional Fourier transform?](https://x.com/cube_flipper/status/1945551347614445877) If this is the case, it would suggest that each moment or “frame” of experience corresponds to a complete rotation through the time-frequency plane and back again. How might we falsify such a hypothesis? Might certain drugs alter the refresh rate in observable or measurable ways?

If this turns out to be true, and if one is willing to put an estimate on the size of the contents of awareness – then we can start putting a lower bound on the number of operations required in order to process the contents of awareness digitally. This said – does it even make sense to talk of computational complexity when discussing [analogue computers](https://en.wikipedia.org/wiki/Analog_computer)? In any case, I believe that the fractional Fourier transform offers a plausible mechanism by which this computationally expensive process can be implemented using wave dynamics.

<video controls=""><source src="https://smoothbrains.net/images/random/frft/frft_fourier_1024.mp4" type="video/mp4"></video>

Joseph Fourier, as seen rotated through the frequency plane.

---

## Open questions

As usual, I have a handful of excess tangents which don’t quite fit into the body of the post, but which I’d still like to explore briefly before concluding the post entirely. Here goes:

### How would you use the fractional Fourier transform to implement higher order pattern recognition?

Let’s use a musical example. Imagine I take the Fourier transform of a single sine wave – the note [A4](https://en.wikipedia.org/wiki/A_\(musical_note\)#Designation_by_octave), which would cause a single spike in the frequency spectrum at *440 Hz*. This is all fine if we just want to recognise individual notes, but what if we’d like to recognise [*intervals*](https://en.wikipedia.org/wiki/Interval_\(music\)) on top of that? If I then play a [C5](https://en.wikipedia.org/wiki/C_\(musical_note\)#Designation_by_octave), that would cause a spike at *660 Hz*, a [perfect fifth](https://en.wikipedia.org/wiki/Perfect_fifth) above the other note – a ratio of *3:2*. If we’d like to be able to recognise perfect fifths at any frequency – we’re going to need a secondary transform or convolution operation on top of this one.

I have a weird intuition that in addition to using [a hierarchy of such optical elements](https://qualiacomputing.com/2025/09/13/indras-net-via-nonlinear-optics-dmt-phenomenology-as-evidence-for-beamsplitter-holography-and-recursive-harmonic-compression/), either the intermediary orders in the fractional Fourier transform or [nonlinear optical](https://en.wikipedia.org/wiki/Nonlinear_optics) effects can be recruited to perform the desired recursive pattern recognition. I still need to explore this idea fully – but helpfully, it seems that such [Indra’s net](https://smoothbrains.net/posts/2025-07-31-is-consciousness-holographic.html#conversation-with-wystan) effects get stronger when under the influence of psychedelics, making this amenable to phenomenological study.

### If consciousness is implementing the fractional Fourier transform, why do we only experience the initial spatial order, and not the other fractional frequency orders?

Perhaps we normally *do* only experience the spatial order (*a* = 0), but it’s possible to dial attention into other stages, or we simply don’t remember them. When this happens is when we experience the weird [ringing artifacts](#fresnel-fringes-and-ringing-artifacts) – or [other, much stranger effects](https://x.com/algekalipso/status/1774575626131013831).

As for the upside down spatial order (*a* = 2), perhaps it’s impossible to tell the difference? Or, as [Steven Lehar proposed](http://slehar.com/wwwRel/ConstructiveAspect/ConstructiveAspect.html), nonlinear optical effects could also be used to create [phase conjugate mirrors](https://en.wikipedia.org/wiki/Nonlinear_optics#Optical_phase_conjugation), which would bounce the waves right back to where they came from. This is speculative, but this would mean that we would only ever experience fractional orders in the range 0 to 1.

I’m also not sure whether to expect that we would experience this process *cycling* – rather, due to the [path integral](https://smoothbrains.net/posts/2025-06-01-path-integrals-and-orbifolds.html) nature of optics, perhaps we’d experience the entire process all at once.

### How does nonlinear optics fit into this picture?

For energy to leave such a wave system or for it to have memory, you effectively need *some* kind of nonlinear effect – the waves need to have some kind of persistent effect on their substrate, for instance modifying the properties of an underlying neuron where they form a high-amplitude cusp.

Nonlinear optical effects can get quite weird, however – this is a topic that is extraordinarily broad and dense. Consider the [Kerr self-focusing effect](https://en.wikipedia.org/wiki/Self-focusing) – related to the *third nonlinear coefficient*, *χ* <sup>(3)</sup> – where if the amplitude of the radiation increases above a certain value it changes the refractive index of the medium, focusing more radiation into the same location in a feedback loop. I believe this can be a real problem in high-power fiber optics.

I wanted to simulate what happens when I experimented with *χ* <sup>(3)</sup>, as I suspect that [this is what 5-HT2A receptor agonists do](https://www.science.org/doi/10.1126/sciadv.adj6102). The results [very quickly went haywire](https://x.com/cube_flipper/status/1903549066728104145):

<video controls=""><source src="https://smoothbrains.net/images/random/frft/frft_nonlinear_chi3_gaussian.mp4" type="video/mp4"></video>

The effect of slowly increasing χ (3) for a Gaussian masked coherent light source propagating from left to right. The complex magnitude is displayed at the top and the full complex value at the bottom. This simulation may have issues with precision or numerical instabilities or simply be entirely incorrect – I’m not quite sure yet.

[Weston Beecroft](https://x.com/westoncb) has published a great [nonlinear optical sandbox](https://github.com/westoncb/nonlinear-optics-sandbox) which can be fun to play around with. Over the coming months, I’d like to spend more time wrapping my head around what is possible using nonlinear optics.