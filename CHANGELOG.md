# Changelog

## Unreleased

### Breaking changes

* Standardize repository text and code on American English, including the `qubitization` package, `qubitized_phase_estimation` module, `discretize_distribution`, and `labeled` ladder helpers. Update imports and call sites to the American spellings.

* Function names now use `cntrl` in place of `controlled` or `control`, preserving word order (for example, `pauli_to_controlled_gate` → `pauli_to_cntrl_gate`). Update imports and call sites; no compatibility aliases are retained. Plural `controls` becomes `cntrls`, and `uncontrolled` becomes `uncntrl`.

Renamed the controlled structs (update imports and type references):

* `ControlledLCU` → `LCUCntrl`.
* `ControlledQubitization` → `QubitizationCntrl`.
* `ControlledReflection` → `ReflectionCntrl`.
* `ControlledSelectTHC` → `SelectTHCCntrl`.
* `ControlledSelectTHCRegs` → `SelectTHCCntrlRegs`.

## [0.3.0](https://github.com/quantinuum-dev/guppy-algorithms/compare/v0.2.0...v0.3.0) (2026-08-13)


### ⚠ BREAKING CHANGES

* utils endianness ([#413](https://github.com/quantinuum-dev/guppy-algorithms/issues/413))
* alias sampling rework ([#386](https://github.com/quantinuum-dev/guppy-algorithms/issues/386))
* add comparators and ripple carry inverse ([#374](https://github.com/quantinuum-dev/guppy-algorithms/issues/374))

### Features

* add comparators and ripple carry inverse ([#374](https://github.com/quantinuum-dev/guppy-algorithms/issues/374)) ([eddd3bf](https://github.com/quantinuum-dev/guppy-algorithms/commit/eddd3bf36c2d3fe00878527a9c151409b5217e94))
* Add indirect averaging for real Pauli observables ([#385](https://github.com/quantinuum-dev/guppy-algorithms/issues/385)) ([3cad3dd](https://github.com/quantinuum-dev/guppy-algorithms/commit/3cad3dd92624fa5a908cb4cb2ba349fcd0074aa2))
* alias sampling rework ([#386](https://github.com/quantinuum-dev/guppy-algorithms/issues/386)) ([767b1b3](https://github.com/quantinuum-dev/guppy-algorithms/commit/767b1b303d18a8b4967862b4b61afa6369303cd9))
* cnx with conditionally clean ancillas ([#401](https://github.com/quantinuum-dev/guppy-algorithms/issues/401)) ([cf5276d](https://github.com/quantinuum-dev/guppy-algorithms/commit/cf5276d3e143a3251312dbb13b14cf24c3de2969))
* LAQCC parity circuits ([#381](https://github.com/quantinuum-dev/guppy-algorithms/issues/381)) ([c0c1698](https://github.com/quantinuum-dev/guppy-algorithms/commit/c0c169858a8ee76c3e66a66b1d1fef42fbcda13d))
* multiplexor state prep ([#410](https://github.com/quantinuum-dev/guppy-algorithms/issues/410)) ([70b1111](https://github.com/quantinuum-dev/guppy-algorithms/commit/70b111121ec9a9ab087da2b4b39a3566868dc659))
* O(1) Toffoli depth CnToffoli ([#274](https://github.com/quantinuum-dev/guppy-algorithms/issues/274)) ([b3e5c44](https://github.com/quantinuum-dev/guppy-algorithms/commit/b3e5c4403ddb543001d13e1366e5e84288c3f6d1))
* phase gradient rotations ([#261](https://github.com/quantinuum-dev/guppy-algorithms/issues/261)) ([0cb540f](https://github.com/quantinuum-dev/guppy-algorithms/commit/0cb540f0bb1d8e97c38bf4e8533204b8032943ed))
* prepare and measure QAE ([#357](https://github.com/quantinuum-dev/guppy-algorithms/issues/357)) ([589d045](https://github.com/quantinuum-dev/guppy-algorithms/commit/589d045e8bb92b804695bed8b0dcf24817bd75d8))
* reflection box based on CnZ  ([#375](https://github.com/quantinuum-dev/guppy-algorithms/issues/375)) ([842e4d4](https://github.com/quantinuum-dev/guppy-algorithms/commit/842e4d41f82279d406b14ecbbe13baadfa710c72))
* SwapUp register ([#362](https://github.com/quantinuum-dev/guppy-algorithms/issues/362)) ([68680b2](https://github.com/quantinuum-dev/guppy-algorithms/commit/68680b2c1f4c419220c9f5893e8e6e613535e952))


### Bug Fixes

* 418 qae make tests deterministic ([#419](https://github.com/quantinuum-dev/guppy-algorithms/issues/419)) ([eacdf0c](https://github.com/quantinuum-dev/guppy-algorithms/commit/eacdf0c332c90ab5a2efa73c1d9ad362f46477b0))


### Miscellaneous Chores

* utils endianness ([#413](https://github.com/quantinuum-dev/guppy-algorithms/issues/413)) ([202ac2f](https://github.com/quantinuum-dev/guppy-algorithms/commit/202ac2fc3b7362110d2b9dc175f305bdb7503082))

## [0.2.0](https://github.com/quantinuum-dev/guppy-algorithms/compare/v0.1.2...v0.2.0) (2026-07-15)


### ⚠ BREAKING CHANGES

* Update to guppylang v1rc0
* update to 312 generic syntax ([#295](https://github.com/quantinuum-dev/guppy-algorithms/issues/295))

### Features

* add single register equality test ([#282](https://github.com/quantinuum-dev/guppy-algorithms/issues/282)) ([499a279](https://github.com/quantinuum-dev/guppy-algorithms/commit/499a27985524cb02334e749a020fb7a7260e390f))
* adding decrementer ([#321](https://github.com/quantinuum-dev/guppy-algorithms/issues/321)) ([8aa8001](https://github.com/quantinuum-dev/guppy-algorithms/commit/8aa8001227e3db1effe1e01f6b7217c89d407c66))
* adding n-2 ancilla algorithm for computing cnx ([#304](https://github.com/quantinuum-dev/guppy-algorithms/issues/304)) ([3ea34db](https://github.com/quantinuum-dev/guppy-algorithms/commit/3ea34db0ebfbd57a0a46f868730011a3febc630d))
* angle finders for fourier and chebyshev functions ([#138](https://github.com/quantinuum-dev/guppy-algorithms/issues/138)) ([cde9dfd](https://github.com/quantinuum-dev/guppy-algorithms/commit/cde9dfd656869526680468d0fe8fcb2c084eaf16))
* controlled gidney Adder ([#260](https://github.com/quantinuum-dev/guppy-algorithms/issues/260)) ([c4ae187](https://github.com/quantinuum-dev/guppy-algorithms/commit/c4ae1875b37f9f6eb0c78958c16996f82e9ad897))
* Controlled unary iteration ([#267](https://github.com/quantinuum-dev/guppy-algorithms/issues/267)), closes [#174](https://github.com/quantinuum-dev/guppy-algorithms/issues/174) ([6983dd6](https://github.com/quantinuum-dev/guppy-algorithms/commit/6983dd694a3b69c278792f2f14e929343b827b6e))
* guarded accumulator and test ([#242](https://github.com/quantinuum-dev/guppy-algorithms/issues/242)) ([22ebe7e](https://github.com/quantinuum-dev/guppy-algorithms/commit/22ebe7eee933ec6fe98fb12fc63fc4613c829da5))
* Hadamard Test ([#358](https://github.com/quantinuum-dev/guppy-algorithms/issues/358)) ([b5eadb5](https://github.com/quantinuum-dev/guppy-algorithms/commit/b5eadb57640581ef8994b8331c2434d6492ce6a4))
* hamming weight calculation ([#249](https://github.com/quantinuum-dev/guppy-algorithms/issues/249)) ([59b243d](https://github.com/quantinuum-dev/guppy-algorithms/commit/59b243d0846b9d0377e3d52c879c090110d98b44))
* hamming weight phasing ([#250](https://github.com/quantinuum-dev/guppy-algorithms/issues/250)) ([8b4ac76](https://github.com/quantinuum-dev/guppy-algorithms/commit/8b4ac76250d59be42acf7660fc95be843996ea7f))
* linear depth incrementer ([#306](https://github.com/quantinuum-dev/guppy-algorithms/issues/306)) ([7ff3391](https://github.com/quantinuum-dev/guppy-algorithms/commit/7ff3391c0f4c7f5ffc4e3c978c9d2e89a17a32bc))
* quantum teleportation with tests ([#339](https://github.com/quantinuum-dev/guppy-algorithms/issues/339)) ([6a75cde](https://github.com/quantinuum-dev/guppy-algorithms/commit/6a75cde6874f5568a5e0ef8bb91e014c9189ada2))


### Bug Fixes

* Make QPE and QFT little endian ([#299](https://github.com/quantinuum-dev/guppy-algorithms/issues/299)) ([edbb44d](https://github.com/quantinuum-dev/guppy-algorithms/commit/edbb44dca5cab01efd52cc4a074ff5aa4a62f1bf))
* substate projection ([#265](https://github.com/quantinuum-dev/guppy-algorithms/issues/265)) ([305f283](https://github.com/quantinuum-dev/guppy-algorithms/commit/305f283147805d85dc53d8813f2ac32770014974))


### Miscellaneous Chores

* update to 312 generic syntax ([#295](https://github.com/quantinuum-dev/guppy-algorithms/issues/295)) ([7b3eb97](https://github.com/quantinuum-dev/guppy-algorithms/commit/7b3eb971c9532a41af851b1c9584d27ff0a46599))

## [0.1.2](https://github.com/quantinuum-dev/guppy-algorithms/compare/v0.1.1...v0.1.2) (2026-05-19)


### Features

* add Guppy runtime math utilities for rotation algorithm ([#216](https://github.com/quantinuum-dev/guppy-algorithms/issues/216)) ([296e7f7](https://github.com/quantinuum-dev/guppy-algorithms/commit/296e7f7c20e620250188dd6ee519f485eb598d91))
* add updated Gidney adder from my old branch ([#199](https://github.com/quantinuum-dev/guppy-algorithms/issues/199)) ([2fa6847](https://github.com/quantinuum-dev/guppy-algorithms/commit/2fa684754e0deda3adbcb9671cfc0be0fa338879))
* bit adders ([#248](https://github.com/quantinuum-dev/guppy-algorithms/issues/248)) ([3016bc6](https://github.com/quantinuum-dev/guppy-algorithms/commit/3016bc67ebfc48625ad74a79549ca223830091a0))
* cnx single ancilla ([#134](https://github.com/quantinuum-dev/guppy-algorithms/issues/134)) ([26c9b2d](https://github.com/quantinuum-dev/guppy-algorithms/commit/26c9b2de61b5e24b9d16ed92a6440b31869c4e5f))
* phase gradient state preparation ([#234](https://github.com/quantinuum-dev/guppy-algorithms/issues/234)) ([0c99eb7](https://github.com/quantinuum-dev/guppy-algorithms/commit/0c99eb74e7737e3087b04e2b649f474246c4532e))
* register incremented rotations  ([#231](https://github.com/quantinuum-dev/guppy-algorithms/issues/231)) ([400028f](https://github.com/quantinuum-dev/guppy-algorithms/commit/400028f727a7d85d1d818dcc897fef3af2d235a5))
* single-qubit rotation algorithm with logarithmic Toffoli count and gate depth ([#220](https://github.com/quantinuum-dev/guppy-algorithms/issues/220)) ([537bb1f](https://github.com/quantinuum-dev/guppy-algorithms/commit/537bb1f56ef9a408dc0c67117c8da37843dedcf9))
* statevector projection on multiple registers with better API ([#159](https://github.com/quantinuum-dev/guppy-algorithms/issues/159)) ([ef633dc](https://github.com/quantinuum-dev/guppy-algorithms/commit/ef633dc4d6c8bd3e754967b34493e4cce43199b3))
* Trotterized phase estimation ([#213](https://github.com/quantinuum-dev/guppy-algorithms/issues/213)) ([d2132d8](https://github.com/quantinuum-dev/guppy-algorithms/commit/d2132d8d015c6d1dc7e03e12eec7f633d51cd104))

## [0.1.1](https://github.com/quantinuum-dev/guppy-algorithms/compare/v0.1.0...v0.1.1) (2026-04-13)


### Features

* add accumulator unary iteration primitive and tests ([#132](https://github.com/quantinuum-dev/guppy-algorithms/issues/132)) ([bd1da4b](https://github.com/quantinuum-dev/guppy-algorithms/commit/bd1da4b616b44a9df7fdfb82c5116d8ebe51b649))
* Add QFT, iQFT, canonical phase estimation and its inverse ([#143](https://github.com/quantinuum-dev/guppy-algorithms/issues/143)) ([ca23abe](https://github.com/quantinuum-dev/guppy-algorithms/commit/ca23abec2fe1d26b4d063c520738c19a307df912))
* added an artificial slicing to traversal ([#66](https://github.com/quantinuum-dev/guppy-algorithms/issues/66)) ([67e5d09](https://github.com/quantinuum-dev/guppy-algorithms/commit/67e5d09643a082bf238423f5db8a0f8c3d6bb86d))
* alias sampling module ([#105](https://github.com/quantinuum-dev/guppy-algorithms/issues/105)) ([9858eb5](https://github.com/quantinuum-dev/guppy-algorithms/commit/9858eb5ef772c097107a057fad91f6003510f512))
* approximate multi-controlled X gate ([#123](https://github.com/quantinuum-dev/guppy-algorithms/issues/123)) ([fe9ace7](https://github.com/quantinuum-dev/guppy-algorithms/commit/fe9ace7c53eabc874be6e1629aaff670b5b334ae))
* ccu decompositions ([#63](https://github.com/quantinuum-dev/guppy-algorithms/issues/63)) ([370bc3d](https://github.com/quantinuum-dev/guppy-algorithms/commit/370bc3dde08724deea55caf0c1bdef0a8aab6b0d))
* First order trotterized Hamiltonian simulation ([#96](https://github.com/quantinuum-dev/guppy-algorithms/issues/96)) ([f4fe6a8](https://github.com/quantinuum-dev/guppy-algorithms/commit/f4fe6a88b6f576cb2458701cb4428ddd63d92eb0))
* fixing cascade up unary iteration index ([#160](https://github.com/quantinuum-dev/guppy-algorithms/issues/160)) ([1d2c4d5](https://github.com/quantinuum-dev/guppy-algorithms/commit/1d2c4d522602770502df1a65c939564d2f8258f9))
* generic cx ladder implementations up to n_max_qubits ([#71](https://github.com/quantinuum-dev/guppy-algorithms/issues/71)) ([331bf29](https://github.com/quantinuum-dev/guppy-algorithms/commit/331bf29459e1b4614e297adfbe4f10755206d1a6))
* Implement unary iteration QROM and AND operation utilities ([#76](https://github.com/quantinuum-dev/guppy-algorithms/issues/76)) ([cadf7a5](https://github.com/quantinuum-dev/guppy-algorithms/commit/cadf7a5f434c73723490448ad1e848379a196230))
* Measurement based QROM uncomputation ([#133](https://github.com/quantinuum-dev/guppy-algorithms/issues/133)) ([2ff8b2e](https://github.com/quantinuum-dev/guppy-algorithms/commit/2ff8b2e88f5bc5a86cc0e3da3614e2d1b9a91dcd))
* Pauli exponential gadget ([#89](https://github.com/quantinuum-dev/guppy-algorithms/issues/89)) ([15a6f38](https://github.com/quantinuum-dev/guppy-algorithms/commit/15a6f38bb90034021fb98c9fe3852241f5a70876))
* pauli select ([#84](https://github.com/quantinuum-dev/guppy-algorithms/issues/84)) ([23899e2](https://github.com/quantinuum-dev/guppy-algorithms/commit/23899e28e4910fdcc5c51f64e5f89bcb1473bd15))
* repeat-until-success Rz rotation with arbitrary angles ([#116](https://github.com/quantinuum-dev/guppy-algorithms/issues/116)) ([dd00ee4](https://github.com/quantinuum-dev/guppy-algorithms/commit/dd00ee4b6f7515579a957924cd9f9560ee91f03f))
* ripple carry adder, substractor, and compare ([a1e0b5c](https://github.com/quantinuum-dev/guppy-algorithms/commit/a1e0b5c9bcfb10fac8b320c90f0407e69ccaa9e8))
* ripple carry adder, substractor, and compare ([a1e0b5c](https://github.com/quantinuum-dev/guppy-algorithms/commit/a1e0b5c9bcfb10fac8b320c90f0407e69ccaa9e8))
* ripple carry adder, subtractor, and compare ([be7b78b](https://github.com/quantinuum-dev/guppy-algorithms/commit/be7b78b2a411485b8956b9de9b97937a4c2891c4))
* ripple carry adder, subtractor, and compare ([be7b78b](https://github.com/quantinuum-dev/guppy-algorithms/commit/be7b78b2a411485b8956b9de9b97937a4c2891c4))
* ripple carry based adder, subtractor, and comparator ([#94](https://github.com/quantinuum-dev/guppy-algorithms/issues/94)) ([be7b78b](https://github.com/quantinuum-dev/guppy-algorithms/commit/be7b78b2a411485b8956b9de9b97937a4c2891c4))
* uniform state preparation for arbitrary number of non zero amplitudes ([a1e0b5c](https://github.com/quantinuum-dev/guppy-algorithms/commit/a1e0b5c9bcfb10fac8b320c90f0407e69ccaa9e8))
* unitary projection pre select ([#69](https://github.com/quantinuum-dev/guppy-algorithms/issues/69)) ([aedd8e7](https://github.com/quantinuum-dev/guppy-algorithms/commit/aedd8e7532b631f20d2f93403377e00d64d14493))


### Bug Fixes

* cx_ladder_impl signature was generic for fixed cx_indices ([#65](https://github.com/quantinuum-dev/guppy-algorithms/issues/65)) ([b98e743](https://github.com/quantinuum-dev/guppy-algorithms/commit/b98e7432e336bda0314bdcf5e8bf21cff56851ff))
* qrom indexing error ([#127](https://github.com/quantinuum-dev/guppy-algorithms/issues/127)) ([ac086a4](https://github.com/quantinuum-dev/guppy-algorithms/commit/ac086a40e49e3c5d8d2457bf4260b797aed3b7e3))


### Documentation

* abstract guppy function construction example notebook ([#87](https://github.com/quantinuum-dev/guppy-algorithms/issues/87)) ([783eb21](https://github.com/quantinuum-dev/guppy-algorithms/commit/783eb2152209a93ac9c08ce33dbae06924dc2a66))
* embed notebook examples as html pages ([#126](https://github.com/quantinuum-dev/guppy-algorithms/issues/126)) ([a01fb17](https://github.com/quantinuum-dev/guppy-algorithms/commit/a01fb1762f2d2a4afaf1293edbe5ff745ccb08b8))
* Generate docs and fix docstring formatting ([#114](https://github.com/quantinuum-dev/guppy-algorithms/issues/114)) ([6aa1c13](https://github.com/quantinuum-dev/guppy-algorithms/commit/6aa1c132b8aa0c1b13a1b17bfd9dacff89e7dd90))
* Trigger documentation build and deployment after release completion ([#74](https://github.com/quantinuum-dev/guppy-algorithms/issues/74)) ([e1f3071](https://github.com/quantinuum-dev/guppy-algorithms/commit/e1f30713b4f9fa0fc207388d2847ad8a9d3604a4))

## 0.1.0 (2025-08-13)


### ⚠ BREAKING CHANGES

* Fix compare unitary tests ([#53](https://github.com/quantinuum-dev/guppy-algorithms/issues/53))

### Features

* cx ladder and ghz and uniform state preparations ([#34](https://github.com/quantinuum-dev/guppy-algorithms/issues/34)) ([a80d46c](https://github.com/quantinuum-dev/guppy-algorithms/commit/a80d46c28caa497e78f23ebfd498fc10b2e4ed83))
* get unitary ([#46](https://github.com/quantinuum-dev/guppy-algorithms/issues/46)) ([ade8d5e](https://github.com/quantinuum-dev/guppy-algorithms/commit/ade8d5ed23dc4d1a40db3179d7169752ede4c1af))
* get unitary projection ([#48](https://github.com/quantinuum-dev/guppy-algorithms/issues/48)) ([142d230](https://github.com/quantinuum-dev/guppy-algorithms/commit/142d230fda77e95a9a7fa26bf5eb86b01900e819))
* LCU Mulitplexor ([#51](https://github.com/quantinuum-dev/guppy-algorithms/issues/51)) ([8e1c919](https://github.com/quantinuum-dev/guppy-algorithms/commit/8e1c919279737728e067745a1efc9f9f3a52be4d))
* update utils and add statevector projection test helpers ([#43](https://github.com/quantinuum-dev/guppy-algorithms/issues/43)) ([c6fcc26](https://github.com/quantinuum-dev/guppy-algorithms/commit/c6fcc26dbbf9db59238f2ab999880a73562c00de))


### Bug Fixes

* remove wheel installation tests from publish workflow ([#36](https://github.com/quantinuum-dev/guppy-algorithms/issues/36)) ([1020ccc](https://github.com/quantinuum-dev/guppy-algorithms/commit/1020ccc488facbefdd581371eac4ce0f53a69f85))


### Tests

* Fix compare unitary tests ([#53](https://github.com/quantinuum-dev/guppy-algorithms/issues/53)) ([dc7bcbb](https://github.com/quantinuum-dev/guppy-algorithms/commit/dc7bcbb07a858e58fcf6b971576a7c4ff8d1cf14))
