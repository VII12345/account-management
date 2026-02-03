// veaury-env.d.ts

declare module 'veaury/vite/index.js' {
    import type { Plugin } from 'vite'

    interface VeauryOptions {
        type?: 'vue' | 'react'
        vueOptions?: any
        reactOptions?: any
        // 可以根据需要添加更多配置项定义，或者直接用 any
        [key: string]: any
    }

    function veauryVitePlugins(options: VeauryOptions): Plugin[]
    export default veauryVitePlugins
}

declare module 'veaury' {
    import { Component } from 'vue'
    import { ComponentType } from 'react'

    export function applyPureReactInVue(reactComponent: ComponentType<any>): Component
    export function applyVueInReact(vueComponent: Component): ComponentType<any>
}