<!-- src/components/common/CrudModal.vue -->
<script setup lang="ts">
import { ref, reactive, onMounted, watch, computed } from 'vue'
import type { FormConfig, FormField } from '@/config/form-config'
import MediaPicker from '@/components/common/MediaPicker.vue'
import {
    postCreateConfig, postUpdateConfig,
    postCategoryCreateConfig, postCategoryUpdateConfig,
    postTagCreateConfig, postTagUpdateConfig,
    dexEntryCreateConfig, dexEntryUpdateConfig,
    dexGenreCreateConfig, dexGenreUpdateConfig,
    mediaTagCreateConfig, mediaTagUpdateConfig,
    mediaCreateConfig, mediaUpdateConfig,
} from '@/config/form-config'

const props = defineProps<{
    module: string
    mode: 'create' | 'update'
    initialData?: any
}>()

const emit = defineEmits(['success', 'close'])

// 根据 module 和 mode 获取对应配置
const config = computed<FormConfig<any>>(() => {
    const configMap: Record<string, Record<'create' | 'update', FormConfig<any>>> = {
        posts: {
            create: postCreateConfig, update: postUpdateConfig
        },
        postCategories: {
            create: postCategoryCreateConfig, update: postCategoryUpdateConfig
        },
        postTags: {
            create: postTagCreateConfig, update: postTagUpdateConfig
        },
        dexs: {
            create: dexEntryCreateConfig, update: dexEntryUpdateConfig
        },
        dexGenres: {
            create: dexGenreCreateConfig, update: dexGenreUpdateConfig
        },
        mediaTags: {
            create: mediaTagCreateConfig, update: mediaTagUpdateConfig
        },
        medias: {
            create: mediaCreateConfig, update: mediaUpdateConfig
        }
    }

    // 安全检查
    const moduleConfig = configMap[props.module]
    if (!moduleConfig) {
        throw new Error(`找不到模块配置: ${props.module}`)
    }

    return moduleConfig[props.mode]
})

const loading = ref(false)
const errorMsg = ref('')

// 表单数据
const form = reactive<any>({})

// 选项缓存
const optionsMap = ref<Record<string, any[]>>({})

// 初始化表单
function initForm() {
    // 清空表单
    Object.keys(form).forEach(key => delete form[key])

    if (props.mode === 'update' && props.initialData) {
        Object.assign(form, props.initialData)

        // ✅ 关键修复：手动映射关联字段
        // if (props.module === 'posts') {
        //     if (props.initialData.category && !form.categoryId) {
        //         form.categoryId = props.initialData.category.id
        //     }
        //     if (props.initialData.tags && !form.tagIds) {
        //         form.tagIds = props.initialData.tags.map((t: any) => t.id)
        //     }
        // }

        // if (props.module === 'dexs') {
        //     if (props.initialData.genres && !form.genreIds) {
        //         form.genreIds = props.initialData.genres.map((g: any) => g.id)
        //     }
        // }

        // 原有类型修正逻辑
        config.value.fields.forEach(field => {
            if (field.type === 'select' || field.type === 'multiSelect') {
                if (field.type === 'multiSelect') {
                    if (!Array.isArray(form[field.key])) {
                        form[field.key] = form[field.key] ? [form[field.key]] : []
                    }
                } else if (field.type === 'select' && !form[field.key]) {
                    form[field.key] = ''
                }
            } else if (field.type === 'switch') {
                form[field.key] = Boolean(form[field.key])
            }
        })
    } else {
        // 创建模式：设置默认值（根据字段类型）
        config.value.fields.forEach(field => {
            if (field.type === 'switch') {
                form[field.key] = false
            } else if (field.type === 'multiSelect') {
                form[field.key] = []
            } else if (field.type === 'number') {
                form[field.key] = 0
            } else {
                form[field.key] = ''
            }
        })
    }
}

// 加载选项
async function loadOptions() {
    for (const field of config.value.fields) {
        if (field.optionsGetter) {
            try {
                optionsMap.value[field.key] = await field.optionsGetter()
            } catch (error) {
                console.error(`加载 ${field.label} 选项失败:`, error)
                optionsMap.value[field.key] = []
            }
        }
    }
}

onMounted(async () => {
    await loadOptions()  // 先加载选项
    initForm()           // 再初始化表单
})

// 监听 initialData 变化，重新初始化表单
watch(() => props.initialData, () => {
    initForm()
}, { deep: true })

// 提交
async function handleSubmit() {
    loading.value = true
    errorMsg.value = ''
    console.log('Form data:', form)
    try {
        if (props.mode === 'create') {
            await config.value.saveApi(form)
        } else {
            await config.value.saveApi(form, props.initialData.id)
        }
        emit('success')
    } catch (err: any) {
        errorMsg.value = err.message || '操作失败'
    } finally {
        loading.value = false
    }
}

const uploadingFiles = reactive<Record<string, boolean>>({})

async function handleFileUpload(field: FormField, event: Event) {
    const input = event.target as HTMLInputElement
    if (!input.files?.length) return

    const file = input.files[0]
    if (!field.uploadApi) {
        console.error('缺少上传API')
        return
    }

    uploadingFiles[field.key] = true
    errorMsg.value = ''

    try {
        const res = await field.uploadApi(file)

        if (typeof res === 'string') {
            form[field.key] = res
        }
        else if (res && typeof res === 'object') {
            // 填充文件路径
            form[field.key] = res.filePath

            // 自动填充其他字段（这些是后端自动分析的，不需要用户填写）
            form['filePath'] = res.filePath
            form['fileSize'] = res.fileSize
            form['mimeType'] = res.mimeType
            form['mediaType'] = res.mediaType
            form['extension'] = res.extension

            // 自动填充元数据（如果有的话）
            if (res.metadata && Object.keys(res.metadata).length > 0) {
                form['metaData'] = res.metadata
            }
        }
    } catch (err: any) {
        errorMsg.value = err.message || '文件上传失败'
    } finally {
        uploadingFiles[field.key] = false
    }
}
</script>

<template>
    <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-white border-4 border-black w-full max-w-3xl max-h-[90vh] overflow-y-auto pixel-card">
            <!-- Header -->
            <div class="p-6 border-b-4 border-black">
                <h2 class="pixel-text text-xl">
                    {{ mode === 'create' ? '➕ 新建' : '✏️ 编辑' }} {{ module }}
                </h2>
            </div>

            <!-- Body -->
            <form @submit.prevent="handleSubmit" class="p-6 space-y-6">
                <div v-for="field in config.fields" :key="field.key">
                    <label class="block mb-2 pixel-text text-sm">
                        {{ field.label }}
                        <span v-if="field.required" class="text-red-500">*</span>
                    </label>

                    <!-- Text / Number -->
                    <input v-if="['text', 'number'].includes(field.type)" v-model="form[field.key]"
                        class="w-full p-3 border-4 border-black focus:outline-none focus:ring-2 focus:ring-sky"
                        :type="field.type" :placeholder="field.placeholder" :required="field.required" />

                    <!-- Textarea -->
                    <textarea v-else-if="field.type === 'textarea'" v-model="form[field.key]"
                        class="w-full p-3 border-4 border-black focus:outline-none focus:ring-2 focus:ring-sky"
                        :rows="field.rows || 4" :placeholder="field.placeholder"></textarea>

                    <!-- Select -->
                    <select v-else-if="field.type === 'select'" v-model="form[field.key]"
                        class="w-full p-3 border-4 border-black bg-white" :required="field.required">
                        <option disabled value="">请选择 {{ field.label }}</option>
                        <option v-for="opt in optionsMap[field.key]" :key="opt.value" :value="opt.value">
                            {{ opt.label }}
                        </option>
                    </select>

                    <!-- Multi Select -->
                    <div v-else-if="field.type === 'multiSelect'" class="flex flex-wrap gap-2">
                        <label v-for="opt in optionsMap[field.key]" :key="opt.value"
                            class="flex items-center gap-2 px-3 py-2 border-2 border-black cursor-pointer hover:bg-gray-50">
                            <input type="checkbox" :value="opt.value" v-model="form[field.key]" />
                            {{ opt.label }}
                        </label>
                    </div>

                    <!-- Switch -->
                    <label v-else-if="field.type === 'switch'" class="inline-flex items-center cursor-pointer">
                        <input type="checkbox" v-model="form[field.key]" class="w-5 h-5 border-2 border-black" />
                        <span class="ml-2 pixel-text text-sm">
                            {{ form[field.key] ? '已发布' : '未发布' }}
                        </span>
                    </label>

                    <div v-else-if="field.type === 'file'" class="space-y-2">
                        <input type="file" :accept="field.accept" @change="(e) => handleFileUpload(field, e)"
                            class="w-full p-3 border-4 border-black focus:outline-none focus:ring-2 focus:ring-sky"
                            :disabled="uploadingFiles[field.key]" />

                        <!-- 上传进度/状态 -->
                        <div v-if="uploadingFiles[field.key]" class="text-sm text-blue-600">
                            ⏳ 上传中...
                        </div>

                        <!-- 显示已上传的文件 -->
                        <div v-if="form[field.key]" class="text-sm text-green-600">
                            ✅ 已上传: {{ form[field.key] }}
                        </div>
                    </div>
                    <!-- Media Picker -->
                    <div v-else-if="field.type === 'mediaPicker'" class="space-y-2">
                        <MediaPicker v-model="form[field.key]" />
                    </div>
                </div>

                <!-- Error -->
                <div v-if="errorMsg" class="text-red-500 pixel-text text-sm">
                    ❌ {{ errorMsg }}
                </div>

                <!-- Footer -->
                <div class="flex justify-end gap-4 pt-4 border-t-4 border-black">
                    <button type="button" @click="emit('close')" class="pixel-btn bg-gray-300">
                        取消
                    </button>
                    <button type="submit" :disabled="loading" class="pixel-btn bg-sky ">
                        {{ loading ? '保存中...' : '保存' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>